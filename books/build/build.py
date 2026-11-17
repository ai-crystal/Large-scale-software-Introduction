# -*- coding: utf-8 -*-
"""
把 books/<册名>/ 下的书稿编译成 PDF。

一册一个目录，目录里有 book.json（元数据）和 structure.json（章节顺序）。
构建脚本由参数 --book 指定编哪一册，共用的样式、资源、检查脚本放 books/common/。

流程：Markdown -> HTML -> Chrome 打印 PDF -> 算标题页码 -> 排目录
      -> 合并封面/扉页/版权页/目录/正文/封底 -> 写书签
      -> 插图转 JPEG -> 字体子集化 -> 20 MiB 体积保护

用法：
    python books/build/build.py --book books/vol1-basics
    python books/build/build.py --book books/vol1-basics --keep
    python books/build/build.py --book books/vol1-basics --no-opt
    python books/build/build.py --all
"""
import os
import re
import sys
import json
import glob
import shutil
import subprocess
import html as htmlmod

import markdown
from pygments.formatters import HtmlFormatter

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BOOKS = os.path.join(ROOT, "books")
COMMON = os.path.join(BOOKS, "common")
ASSETS = os.path.join(COMMON, "assets")
OUTPUT = os.path.join(ROOT, "output")

# 由 --book 决定的变量，在 load_book() 里填
BOOK = None
BUILD = None
META = {}
STRUCT = {}


# ---------- 0. 读取一册的配置 ----------
def load_book(book_dir):
    global BOOK, BUILD, META, STRUCT
    BOOK = os.path.abspath(book_dir)
    if not os.path.isdir(BOOK):
        raise SystemExit("目录不存在：%s" % book_dir)

    meta_path = os.path.join(BOOK, "book.json")
    struct_path = os.path.join(BOOK, "structure.json")
    if not os.path.exists(meta_path):
        raise SystemExit("缺少 book.json：%s" % meta_path)
    if not os.path.exists(struct_path):
        raise SystemExit("缺少 structure.json：%s" % struct_path)

    with open(meta_path, encoding="utf-8") as f:
        META = json.load(f)
    with open(struct_path, encoding="utf-8") as f:
        STRUCT = json.load(f)

    # 每册单独一个临时目录，交替构建时不会互相覆盖
    BUILD = os.path.join(ROOT, "_private", "build", META["name"])
    os.makedirs(BUILD, exist_ok=True)
    os.makedirs(OUTPUT, exist_ok=True)


def meta(key, default=""):
    return META.get(key, default)


# ---------- 1. 资源检查 ----------
def ensure_assets():
    katex = os.path.join(ASSETS, "katex")
    if not os.path.exists(os.path.join(katex, "katex.min.js")):
        raise SystemExit("缺少 books/common/assets/katex，无法排版公式")


# ---------- 2. 按 structure.json 读入章节 ----------
def load_chapters():
    parts = []

    front = os.path.join(BOOK, "front")
    for name in STRUCT.get("front", []):
        path = os.path.join(front, name)
        if os.path.exists(path):
            parts.append(path)

    # 章之前的篇首
    part_before = {}
    for item in STRUCT.get("parts", []):
        part_before[item["before"]] = item["file"]

    chapters_dir = os.path.join(BOOK, "chapters")
    for name in STRUCT.get("chapters", []):
        part_name = part_before.get(name)
        if part_name:
            part_path = os.path.join(front, part_name)
            if os.path.exists(part_path):
                parts.append(part_path)
        path = os.path.join(chapters_dir, name)
        if os.path.exists(path):
            parts.append(path)

    appendix_dir = os.path.join(BOOK, "appendix")
    for name in STRUCT.get("appendix", []):
        path = os.path.join(appendix_dir, name)
        if os.path.exists(path):
            parts.append(path)

    if not parts:
        raise SystemExit("%s 下没有找到任何章节" % BOOK)

    texts = []
    for path in parts:
        with open(path, encoding="utf-8") as fh:
            texts.append(fh.read().strip())
    return texts


MD_EXT = ["extra", "def_list", "sane_lists", "toc", "md_in_html", "admonition",
          "codehilite", "pymdownx.arithmatex", "pymdownx.tilde",
          "pymdownx.smartsymbols", "legacy_attrs"]
MD_CFG = {
    "pymdownx.arithmatex": {"generic": True},
    "codehilite": {"guess_lang": False, "css_class": "codehilite", "use_pygments": True},
    "toc": {"permalink": False},
}


def md2html(text):
    return markdown.markdown(text, extensions=MD_EXT, extension_configs=MD_CFG)


# ---------- 3. 图片压缩与图题 ----------
HEAD_RE = re.compile(r"<h([12])\s+id=\"([^\"]*)\">(.*?)</h\1>", re.S)
IMG_P_RE = re.compile(r"<p>\s*(<img[^>]*>)\s*</p>", re.S)
ALT_RE = re.compile(r'alt="([^"]*)"')
SRC_RE = re.compile(r'src="([^"]+)"')


def jpeg_images(body, max_width=1500, quality=88):
    """把正文引用的 PNG 转成构建用 JPEG，避免 PDF 直接嵌入大 PNG。"""
    from PIL import Image
    out_dir = os.path.join(BUILD, "images")
    images_dir = os.path.join(BOOK, "images")
    chapters_dir = os.path.join(BOOK, "chapters")
    count = 0

    def repl(match):
        nonlocal count
        src = match.group(1)
        if src.startswith(("http://", "https://", "file://", "data:")):
            return match.group(0)
        source = os.path.normpath(os.path.join(chapters_dir, src))
        if not os.path.isfile(source):
            print("  ! 图片不存在：", src)
            return match.group(0)
        rel = os.path.relpath(source, images_dir)
        target = os.path.join(out_dir, os.path.splitext(rel)[0] + ".jpg")
        os.makedirs(os.path.dirname(target), exist_ok=True)

        im = Image.open(source)
        dpi = (im.info.get("dpi") or (96, 96))[0] or 96
        design_mm = im.width / dpi * 25.4
        if design_mm >= 120:
            disp = 134.0
        else:
            disp = min(134.0, design_mm * 1.15)
        if disp * im.height / im.width > 172:
            disp = 172 * im.width / im.height

        if not os.path.exists(target) or os.path.getmtime(target) < os.path.getmtime(source):
            if im.mode in ("RGBA", "LA"):
                bg = Image.new("RGB", im.size, "white")
                bg.paste(im, mask=im.getchannel("A"))
                im = bg
            else:
                im = im.convert("RGB")
            if im.width > max_width:
                h = round(im.height * max_width / im.width)
                im = im.resize((max_width, h), Image.Resampling.LANCZOS)
            im.save(target, "JPEG", quality=quality, subsampling=0,
                    optimize=True, progressive=True)
            count += 1
        return 'src="file:///%s" style="width:%.1fmm"' % (target.replace(os.sep, "/"), disp)

    result = SRC_RE.sub(repl, body)
    if count:
        print("· 转换 PDF 插图 JPEG：%d 张 ..." % count)
    return result


def process_body(body):
    body = jpeg_images(body)

    def repl(m):
        tag = m.group(1)
        alt = ALT_RE.search(tag)
        cap = alt.group(1) if alt else ""
        tag = re.sub(r'\s*alt="[^"]*"', "", tag)
        cap_html = '<figcaption>%s</figcaption>' % cap if cap else ""
        return "<figure>" + tag + cap_html + "</figure>"

    return IMG_P_RE.sub(repl, body)


# ---------- 4. 目录 ----------
def build_toc(body):
    heads = []
    for m in HEAD_RE.finditer(body):
        lvl = int(m.group(1))
        hid = m.group(2)
        txt = re.sub(r"<[^>]+>", "", m.group(3))
        heads.append((lvl, hid, txt))

    # toc_sections=False 时目录只列到章，小节不单列
    if not meta("toc_sections", False):
        heads_for_toc = [h for h in heads if h[0] == 1 or not h[2].startswith("第")]
    else:
        heads_for_toc = heads

    rows = []
    for lvl, hid, txt in heads:
        if not meta("toc_sections", False) and lvl == 2:
            continue
        rows.append(
            '<div class="toc-item lv%d"><span class="t">%s</span>'
            '<span class="dots"></span><span class="pg" data-hid="%s"></span></div>'
            % (lvl, htmlmod.escape(txt), hid)
        )
    return heads, "\n".join(rows)


# ---------- 5. HTML 壳 ----------
def page(title, body_html):
    katex = os.path.join(ASSETS, "katex").replace(os.sep, "/")
    chapters_dir = os.path.join(BOOK, "chapters").replace(os.sep, "/")
    style = os.path.join(COMMON, "style.css").replace(os.sep, "/")
    return """<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<base href="file:///%s/">
<title>%s</title>
<link rel="stylesheet" href="file:///%s/katex.min.css">
<link rel="stylesheet" href="file:///%s">
<style>%s
.codehilite { background: #f7f7f5; }
</style>
<script src="file:///%s/katex.min.js"></script>
<script src="file:///%s/contrib/auto-render.min.js"></script>
</head><body>%s
<script>
document.addEventListener("DOMContentLoaded", function () {
  renderMathInElement(document.body, {
    delimiters: [
      {left: "$$", right: "$$", display: true},
      {left: "\\\\[", right: "\\\\]", display: true},
      {left: "\\\\(", right: "\\\\)", display: false},
      {left: "$", right: "$", display: false}
    ],
    throwOnError: false,
    ignoredTags: ["script", "noscript", "style", "textarea", "pre", "code"]
  });
  window.__mathDone = true;
});
</script></body></html>""" % (
        chapters_dir, title, katex, style,
        HtmlFormatter(style="xcode").get_style_defs(".codehilite"),
        katex, katex, body_html)


def render(html_path, pdf_path, footer=False, margin=None):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = None
        for ch in ("chrome", "msedge", None):
            try:
                if ch:
                    browser = p.chromium.launch(channel=ch, args=["--font-render-hinting=none"])
                else:
                    browser = p.chromium.launch(args=["--font-render-hinting=none"])
                break
            except Exception:
                continue
        if browser is None:
            raise SystemExit("找不到浏览器：请安装 Chrome/Edge，或运行 playwright install chromium")
        pg = browser.new_page(viewport={"width": 900, "height": 1200})
        pg.goto("file:///" + html_path.replace(os.sep, "/"), wait_until="load")
        pg.wait_for_function("window.__mathDone === true", timeout=120000)
        pg.evaluate("document.fonts.ready")
        pg.wait_for_timeout(1000)
        opts = dict(path=pdf_path, width="170mm", height="240mm",
                    print_background=True,
                    margin=margin or {"top": "19mm", "bottom": "17mm",
                                      "left": "19mm", "right": "17mm"},
                    prefer_css_page_size=False)
        if footer:
            opts["display_header_footer"] = True
            opts["header_template"] = "<div></div>"
            opts["footer_template"] = (
                '<div style="width:100%;font-size:7.6pt;color:#666;font-family:serif;'
                'text-align:center;margin-top:4mm;"><span class="pageNumber"></span></div>')
        pg.pdf(**opts)
        browser.close()


# ---------- 6. 目录页码回填 ----------
def norm(s):
    s = re.sub(r"\s+", "", s)
    s = re.sub(r"[，。、：；！？“”‘’（）()《》〈〉·—\-\.\,\:\;\"']", "", s)
    return s


def find_pages(pdf_path, heads):
    import fitz
    doc = fitz.open(pdf_path)
    texts = [norm(doc[i].get_text()) for i in range(len(doc))]
    pages, ptr, missing = {}, 0, []
    for lvl, hid, txt in heads:
        key = norm(txt)
        found = None
        for L in (16, 12, 8, 6):
            k = key[:L]
            for i in range(ptr, len(texts)):
                if k and k in texts[i]:
                    found = i + 1
                    break
            if found:
                break
        if found:
            pages[hid] = found
            ptr = found - 1
        else:
            pages[hid] = pages.get(heads[max(0, len(pages) - 1)][1], 1)
            missing.append(txt)
    doc.close()
    return pages, missing


# ---------- 7. 封面、扉页、版权页、封底 ----------
def cover_art_path():
    name = meta("cover_bg", "cover.jpg")
    path = os.path.join(ASSETS, "cover", name)
    if not os.path.exists(path):
        found = glob.glob(os.path.join(ASSETS, "cover", "*"))
        if found:
            return found[0].replace(os.sep, "/")
    return path.replace(os.sep, "/")


COVER = """
<div style="position:relative;width:170mm;height:240mm;overflow:hidden;background:#070b12;">
  <img src="file:///{cover}" style="position:absolute;left:0;top:0;width:170mm;height:240mm;
       object-fit:cover;">
  <div style="position:absolute;left:0;top:0;width:170mm;height:240mm;
       background:linear-gradient(180deg,rgba(7,11,18,0.55) 0%,rgba(7,11,18,0.18) 38%,
       rgba(7,11,18,0.72) 68%,rgba(7,11,18,0.97) 100%);"></div>
  <div style="position:absolute;left:13mm;top:13mm;width:144mm;height:214mm;
       border:0.5pt solid rgba(255,255,255,0.16);"></div>
  <div style="position:absolute;left:21mm;top:24mm;font-family:'Microsoft YaHei',sans-serif;
       font-size:7.6pt;letter-spacing:0.42em;color:{accent};">{series}</div>
  <div style="position:absolute;left:21mm;top:32mm;width:18mm;height:0.9pt;background:{accent};"></div>
  <div style="position:absolute;left:21mm;bottom:104mm;width:132mm;
       font-family:'SimSun',serif;font-size:34pt;font-weight:700;line-height:1.3;
       letter-spacing:0.06em;color:#ffffff;">{title}</div>
  <div style="position:absolute;left:21mm;bottom:92mm;width:128mm;
       font-family:'Microsoft YaHei',sans-serif;font-size:13pt;line-height:1.6;
       letter-spacing:0.12em;color:{accent};">{volume}</div>
  <div style="position:absolute;left:21mm;bottom:78mm;width:128mm;
       font-family:'Microsoft YaHei',sans-serif;font-size:9.6pt;line-height:1.8;
       letter-spacing:0.06em;color:#cfd8e3;">{subtitle}</div>
  <div style="position:absolute;left:21mm;bottom:66mm;width:24mm;height:1.2pt;background:{accent};"></div>
  <div style="position:absolute;left:21mm;bottom:44mm;width:124mm;
       font-family:'SimSun',serif;font-size:9pt;line-height:2.15;color:#a9b6c6;">
       {blurb}
  </div>
  <div style="position:absolute;left:21mm;bottom:24mm;font-family:'Microsoft YaHei',sans-serif;
       font-size:11pt;letter-spacing:0.12em;color:#eef3f9;">{author}</div>
  <div style="position:absolute;right:21mm;bottom:24mm;font-family:'Microsoft YaHei',sans-serif;
       font-size:8.2pt;letter-spacing:0.2em;color:#7f8ea3;">{year}</div>
</div>
"""

TITLEPAGE = """
<div style="width:170mm;height:240mm;padding:0;box-sizing:border-box;background:#ffffff;">
  <div style="padding:62mm 24mm 0 24mm;">
    <div style="font-family:'Microsoft YaHei',sans-serif;font-size:8pt;letter-spacing:0.38em;
         color:{accent_dark};">{series}</div>
    <div style="margin-top:10mm;font-family:'SimSun',serif;font-size:31pt;font-weight:700;
         line-height:1.35;letter-spacing:0.06em;color:#111;">{title}</div>
    <div style="margin-top:4mm;font-family:'Microsoft YaHei',sans-serif;font-size:15pt;
         letter-spacing:0.14em;color:{accent_dark};">{volume}</div>
    <div style="margin-top:6mm;font-family:'Microsoft YaHei',sans-serif;font-size:11pt;
         line-height:1.9;color:#333;">{subtitle}</div>
    <div style="margin-top:9mm;width:26mm;height:1.4pt;background:{accent};"></div>
    <div style="margin-top:42mm;font-family:'SimSun',serif;font-size:11pt;
         color:#222;">{author}</div>
    <div style="margin-top:3mm;font-family:'Microsoft YaHei',sans-serif;font-size:9pt;
         letter-spacing:0.16em;color:#777;">{year}</div>
  </div>
</div>
"""

COPYRIGHT = """
<div style="width:170mm;height:240mm;box-sizing:border-box;background:#ffffff;">
  <div style="position:relative;height:100%;padding:122mm 24mm 0 24mm;box-sizing:border-box;">
    <div style="font-family:'Microsoft YaHei',sans-serif;font-size:8.4pt;line-height:2.05;color:#555;">
      <div style="font-weight:700;color:#111;margin-bottom:3mm;">{title}　{volume}</div>
      <div>{subtitle}</div>
      <div style="margin-top:6mm;">作者　{author}</div>
      <div>版本　{version}　·　{year} 年</div>
      <div style="margin-top:10mm;max-width:108mm;">{intro}</div>
      <div style="margin-top:10mm;max-width:108mm;">本书采用 CC BY-NC-SA 4.0 许可协议。</div>
      <div style="margin-top:2mm;">https://creativecommons.org/licenses/by-nc-sa/4.0/</div>
    </div>
  </div>
</div>
"""

BACK = """
<div style="position:relative;width:170mm;height:240mm;overflow:hidden;background:#070b12;">
  <div style="position:absolute;left:13mm;top:13mm;width:144mm;height:214mm;
       border:0.5pt solid rgba(255,255,255,0.14);"></div>
  <div style="position:absolute;left:21mm;top:26mm;font-family:'Microsoft YaHei',sans-serif;
       font-size:7.6pt;letter-spacing:0.36em;color:{accent};">关于本册</div>
  <div style="position:absolute;left:21mm;top:40mm;width:128mm;
       font-family:'SimSun',serif;font-size:13pt;line-height:1.95;color:#f3f7fb;">
       {back_lead}
  </div>
  <div style="position:absolute;left:21mm;top:74mm;width:128mm;
       font-family:'SimSun',serif;font-size:9.2pt;line-height:2.05;color:#b9c7d7;">
       {back_text}
  </div>
  <div style="position:absolute;left:21mm;top:126mm;width:128mm;
       font-family:'Microsoft YaHei',sans-serif;font-size:8.2pt;line-height:2.4;color:#8c9db2;">
       {back_tags}
  </div>
  <div style="position:absolute;left:21mm;top:152mm;width:26mm;height:0.8pt;
       background:{accent_line};"></div>
  <div style="position:absolute;left:21mm;bottom:24mm;font-family:'Microsoft YaHei',sans-serif;
       font-size:10.2pt;letter-spacing:0.1em;color:#eef4fb;">{author}</div>
</div>
"""


def build_special(name, html_body, out_pdf, title, zero_margin=True):
    path = os.path.join(BUILD, name + ".html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(page(title, html_body))
    margin = {"top": "0mm", "bottom": "0mm", "left": "0mm", "right": "0mm"} if zero_margin else None
    render(path, out_pdf, footer=False, margin=margin)
    return out_pdf


def cover_fields():
    accent = meta("cover_color", "#c9a227")
    return {
        "cover": cover_art_path(),
        "accent": accent,
        "accent_dark": meta("accent_dark", "#8a6d1f"),
        "accent_line": accent + "a6" if len(accent) == 7 else "rgba(201,162,39,0.65)",
        "series": meta("series", "LARGE-SCALE SOFTWARE"),
        "title": meta("title", ""),
        "volume": meta("volume", ""),
        "subtitle": meta("subtitle", ""),
        "blurb": meta("cover_blurb", ""),
        "back_lead": meta("back_lead", ""),
        "back_text": meta("back_text", ""),
        "back_tags": meta("back_tags", ""),
        "intro": meta("intro", ""),
        "author": meta("author", ""),
        "year": meta("year", ""),
        "version": meta("version", ""),
    }


# ---------- 8. 主流程 ----------
def build(no_opt=False):
    ensure_assets()
    chapters = load_chapters()
    raw = chr(10).join(chapters)
    body = process_body(md2html(raw))
    heads, toc_rows = build_toc(body)

    title = meta("title", "")
    full_title = meta("full_title", title)
    fields = cover_fields()

    # 1. 正文单独排版，页码从 1 开始
    p1 = os.path.join(BUILD, "body.html")
    with open(p1, "w", encoding="utf-8") as f:
        f.write(page(title, body))
    body_pdf = os.path.join(BUILD, "body.pdf")
    print("· 排版正文 ...")
    render(p1, body_pdf, footer=True)

    print("· 计算目录页码 ...")
    pages, missing = find_pages(body_pdf, heads)
    if missing:
        print("  未能定位的标题：", missing[:8])

    def fill(m):
        hid = m.group(1)
        return '<span class="pg" data-hid="%s">%s</span>' % (hid, pages.get(hid, ""))

    toc_rows_filled = re.sub(r'<span class="pg" data-hid="([^"]*)"></span>', fill, toc_rows)
    toc_html = (
        '<div class="toc"><h1 style="break-before:auto">目录</h1>'
        '<div class="toc-list">%s</div></div>' % toc_rows_filled
    )
    ptoc = os.path.join(BUILD, "toc.html")
    with open(ptoc, "w", encoding="utf-8") as f:
        f.write(page(title, toc_html))
    toc_pdf = os.path.join(BUILD, "toc.pdf")
    print("· 排版目录 ...")
    render(ptoc, toc_pdf, footer=False)

    print("· 生成封面与辅文 ...")
    cover = build_special("cover", COVER.format(**fields),
                          os.path.join(BUILD, "cover.pdf"), title)
    titlepage = build_special("titlepage", TITLEPAGE.format(**fields),
                              os.path.join(BUILD, "titlepage.pdf"), title)
    copyright_pdf = build_special("copyright", COPYRIGHT.format(**fields),
                                  os.path.join(BUILD, "copyright.pdf"), title)
    back = build_special("back", BACK.format(**fields),
                         os.path.join(BUILD, "back.pdf"), title)

    print("· 合并并写入书签 ...")
    import fitz
    out = fitz.open()
    out.insert_pdf(fitz.open(cover))
    out.insert_pdf(fitz.open(titlepage))
    out.insert_pdf(fitz.open(copyright_pdf))
    toc_doc = fitz.open(toc_pdf)
    out.insert_pdf(toc_doc)
    body_doc = fitz.open(body_pdf)
    out.insert_pdf(body_doc)
    out.insert_pdf(fitz.open(back))

    offset = 3 + len(toc_doc)
    toc = [[1, full_title, 1]]
    for lvl, hid, txt in heads:
        toc.append([lvl, re.sub(r"<[^>]+>", "", txt), pages.get(hid, 1) + offset])
    out.set_toc(toc)
    out.set_metadata({
        "title": full_title,
        "author": meta("author", ""),
        "subject": meta("subtitle", ""),
        "keywords": meta("keywords", ""),
    })
    try:
        out.subset_fonts(verbose=False)
    except Exception as exc:
        print("· 字体子集化警告：", exc)

    target = os.path.join(OUTPUT, meta("pdf", META["name"] + ".pdf"))
    tmp = target + ".tmp"
    try:
        out.save(tmp, garbage=3, deflate=True)
        try:
            os.replace(tmp, target)
        except PermissionError:
            alt = target[:-4] + "-new.pdf"
            os.replace(tmp, alt)
            print("提示：%s 正被占用（可能开着阅读器），这次先存为 %s" % (target, alt))
            target = alt
    except Exception as e:
        out.close()
        raise SystemExit("保存 PDF 失败：%s，多半是文件正被阅读器占用，关掉后重试。" % e)
    if os.path.exists(tmp):
        try:
            os.remove(tmp)
        except OSError:
            pass
    page_count = len(out)
    out.close()

    guard = os.path.join(COMMON, "checks", "pdf_size_guard.py")
    if os.path.exists(guard):
        result = subprocess.run([sys.executable, guard, target])
        if result.returncode != 0:
            raise SystemExit("PDF 体积检查未通过；请压缩插图后重试。")

    print("完成：%s  共 %d 页" % (target, page_count))

    if "--keep" not in sys.argv:
        for name in ("body.html", "toc.html"):
            path = os.path.join(BUILD, name)
            if os.path.exists(path):
                try:
                    os.remove(path)
                except OSError:
                    pass


def all_books():
    result = []
    for name in sorted(os.listdir(BOOKS)):
        path = os.path.join(BOOKS, name)
        if os.path.isdir(path) and os.path.exists(os.path.join(path, "book.json")):
            result.append(path)
    return result


def main():
    args = sys.argv[1:]
    if "--all" in args:
        books = all_books()
        if not books:
            raise SystemExit("books/ 下没有找到任何一册")
        for path in books:
            print("=" * 50)
            print("构建：", os.path.relpath(path, ROOT))
            load_book(path)
            build()
        return

    if "--book" not in args:
        raise SystemExit(
            "用法：python books/build/build.py --book books/<册名>\n"
            "      python books/build/build.py --all")

    path = args[args.index("--book") + 1]
    load_book(path)
    build()


if __name__ == "__main__":
    main()
