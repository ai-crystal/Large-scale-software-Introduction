# -*- coding: utf-8 -*-
"""
把 book/ 下的书稿编译成 PDF。

流程：Markdown -> HTML -> Chrome 打印 PDF -> 扫描标题页码回填目录
      -> 二次打印 -> 合并封面/扉页/版权页/封底 -> 写书签
      -> 插图转 JPEG -> 字体子集化 -> 20 MiB 体积保护

用法：python book/build/build.py
      python book/build/build.py --keep      保留中间文件
      python book/build/build.py --out xxx.pdf
"""
import os
import re
import sys
import glob
import subprocess
import html as htmlmod

import markdown
from pygments.formatters import HtmlFormatter

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BUILD = os.path.join(ROOT, "_private", "build")
BOOK = os.path.join(ROOT, "book")
ASSETS = os.path.join(BOOK, "build", "assets")
OUTPUT = os.path.join(ROOT, "output")
OUT_PDF = os.path.join(OUTPUT, "book.pdf")
STYLE = os.path.join(BOOK, "build", "style.css")

TITLE = "大型软件是怎么长出来的"
SUBTITLE = "用 C++ 从二十行代码到一个插件系统"
AUTHOR = "Dr. Dezeming"
YEAR = "2026"
VERSION = "1.0"

os.makedirs(BUILD, exist_ok=True)
os.makedirs(OUTPUT, exist_ok=True)


# ---------- 1. 资源检查 ----------
def ensure_assets():
    katex = os.path.join(ASSETS, "katex")
    if not os.path.exists(os.path.join(katex, "katex.min.js")):
        raise SystemExit("缺少 book/build/assets/katex，无法排版公式")


# ---------- 2. 读入章节 ----------
FRONT_ORDER = ["preface.md"]


def load_chapters():
    files = []
    front = os.path.join(BOOK, "front")
    preface = os.path.join(front, "preface.md")
    if os.path.exists(preface):
        files.append(preface)

    chapters = sorted(glob.glob(os.path.join(BOOK, "chapters", "*.md")))
    part_before = {1: "part1.md", 4: "part2.md", 8: "part3.md", 12: "part4.md"}
    for index, path in enumerate(chapters, 1):
        part_name = part_before.get(index)
        if part_name:
            part_path = os.path.join(front, part_name)
            if os.path.exists(part_path):
                files.append(part_path)
        files.append(path)

    files.extend(sorted(glob.glob(os.path.join(BOOK, "appendix", "*.md"))))
    if not files:
        raise SystemExit("book/ 下没有找到 .md 文件")

    parts = []
    for path in files:
        with open(path, encoding="utf-8") as fh:
            parts.append(fh.read().strip())
    return parts


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


def jpeg_images(body):
    """把正文引用的 PNG 转成构建用 JPEG，避免 PDF 直接嵌入大 PNG。"""
    from PIL import Image
    out_dir = os.path.join(BUILD, "images")
    count = 0

    def repl(match):
        nonlocal count
        src = match.group(1)
        if src.startswith(("http://", "https://", "file://", "data:")):
            return match.group(0)
        source = os.path.normpath(os.path.join(BOOK, "chapters", src))
        if not os.path.isfile(source):
            print("  ! 图片不存在：", src)
            return match.group(0)
        rel = os.path.relpath(source, os.path.join(BOOK, "images"))
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
            if im.width > 1500:
                h = round(im.height * 1500 / im.width)
                im = im.resize((1500, h), Image.Resampling.LANCZOS)
            im.save(target, "JPEG", quality=88, subsampling=0,
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
        cap_html = f'<figcaption>{cap}</figcaption>' if cap else ""
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
    rows = []
    for lvl, hid, txt in heads:
        rows.append(
            '<div class="toc-item lv%d"><span class="t">%s</span>'
            '<span class="dots"></span><span class="pg" data-hid="%s"></span></div>'
            % (lvl, htmlmod.escape(txt), hid)
        )
    return heads, "\n".join(rows)


# ---------- 5. HTML 壳 ----------
def page(title, body_html):
    katex = os.path.join(ASSETS, "katex").replace(os.sep, "/")
    chapter_root = os.path.join(BOOK, "chapters").replace(os.sep, "/")
    style = STYLE.replace(os.sep, "/")
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
        chapter_root, title, katex, style,
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
    start = 0
    for i, t in enumerate(texts):
        if "〖BODY〗" in t:
            start = i
            break
    pages, ptr, missing = {}, start, []
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
    return pages, missing, start


# ---------- 7. 封面、扉页、版权页、封底 ----------
COVER_ART = os.path.join(ASSETS, "cover", "cover.png").replace(os.sep, "/")

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
       font-size:7.6pt;letter-spacing:0.42em;color:#c9a227;">PLUGIN ARCHITECTURE</div>
  <div style="position:absolute;left:21mm;top:32mm;width:18mm;height:0.9pt;background:#c9a227;"></div>
  <div style="position:absolute;left:21mm;bottom:96mm;width:132mm;
       font-family:'SimSun',serif;font-size:38pt;font-weight:700;line-height:1.3;
       letter-spacing:0.08em;color:#ffffff;">{title}</div>
  <div style="position:absolute;left:21mm;bottom:80mm;width:128mm;
       font-family:'Microsoft YaHei',sans-serif;font-size:10.4pt;line-height:1.8;
       letter-spacing:0.08em;color:#cfd8e3;">{subtitle}</div>
  <div style="position:absolute;left:21mm;bottom:68mm;width:24mm;height:1.2pt;background:#c9a227;"></div>
  <div style="position:absolute;left:21mm;bottom:46mm;width:124mm;
       font-family:'SimSun',serif;font-size:9pt;line-height:2.15;color:#a9b6c6;">
       从一段只会打印命令的程序开始<br>
       拆函数、拆文件、装插件、建契约，一步步长出可扩展的外壳
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
         color:#8a6d1f;">PLUGIN ARCHITECTURE</div>
    <div style="margin-top:10mm;font-family:'SimSun',serif;font-size:31pt;font-weight:700;
         line-height:1.35;letter-spacing:0.06em;color:#111;">{title}</div>
    <div style="margin-top:7mm;font-family:'Microsoft YaHei',sans-serif;font-size:12pt;
         line-height:1.9;color:#333;">{subtitle}</div>
    <div style="margin-top:9mm;width:26mm;height:1.4pt;background:#c9a227;"></div>
    <div style="margin-top:46mm;font-family:'SimSun',serif;font-size:11pt;
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
      <div style="font-weight:700;color:#111;margin-bottom:3mm;">{title}</div>
      <div>{subtitle}</div>
      <div style="margin-top:6mm;">作者　{author}</div>
      <div>版本　{VERSION}　·　{year} 年</div>
      <div style="margin-top:10mm;max-width:108mm;">本书从一段二十行的 C++ 程序开始，逐步拆函数、拆文件、加载动态库、建立契约、
      处理事件与故障，最后做成一个可打包、可更新的插件系统。</div>
      <div style="margin-top:10mm;max-width:108mm;">书中代码示例采用 C++17 编写，只依赖标准库；
      平台相关的部分会分别给出 Windows 与 Linux 的写法。</div>
      <div style="margin-top:10mm;">本书采用 CC BY-NC-SA 4.0 许可协议。</div>
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
       font-size:7.6pt;letter-spacing:0.36em;color:#c9a227;">关于本书</div>
  <div style="position:absolute;left:21mm;top:40mm;width:128mm;
       font-family:'SimSun',serif;font-size:13pt;line-height:1.95;color:#f3f7fb;">
       一个程序长大的过程，<br>就是不断把“改动”关进边界里的过程。
  </div>
  <div style="position:absolute;left:21mm;top:72mm;width:128mm;
       font-family:'SimSun',serif;font-size:9.2pt;line-height:2.05;color:#b9c7d7;">
       从二十行 C++ 代码讲起，每章只加一个概念，每个概念都落到能编译、能运行的例子里。
       不假设你懂 Java，也不假设你学过操作系统；遇到进程、链接、动态库这些词，先用日常经验讲明白。
       读完你应该能自己写出一个带插件、能隔离、能打包的最小外壳。
  </div>
  <div style="position:absolute;left:21mm;top:122mm;width:128mm;
       font-family:'Microsoft YaHei',sans-serif;font-size:8.2pt;line-height:2.5;color:#8c9db2;">
       函数与文件　·　动态库与函数指针　·　契约与版本<br>
       事件与钩子　·　进程与管道　·　模板与分发生态
  </div>
  <div style="position:absolute;left:21mm;top:148mm;width:26mm;height:0.8pt;
       background:rgba(201,162,39,0.65);"></div>
  <div style="position:absolute;left:21mm;bottom:24mm;font-family:'Microsoft YaHei',sans-serif;
       font-size:10.2pt;letter-spacing:0.1em;color:#eef4fb;">{author}</div>
</div>
"""


def build_special(name, html_body, out_pdf, zero_margin=True):
    path = os.path.join(BUILD, name + ".html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(page(TITLE, html_body))
    margin = {"top": "0mm", "bottom": "0mm", "left": "0mm", "right": "0mm"} if zero_margin else None
    render(path, out_pdf, footer=False, margin=margin)
    return out_pdf


# ---------- 8. 主流程 ----------
def main():
    ensure_assets()
    chapters = load_chapters()
    raw = "\n\n".join(chapters)
    body = process_body(md2html(raw))
    heads, toc_rows = build_toc(body)

    toc_html = (
        '<div class="toc"><h1 style="break-before:auto">目录</h1>'
        '<div class="toc-list">%s</div></div>' % toc_rows
    )
    full = toc_html + body

    p1 = os.path.join(BUILD, "body_pass1.html")
    with open(p1, "w", encoding="utf-8") as f:
        f.write(page(TITLE, full))
    pdf1 = os.path.join(BUILD, "body_pass1.pdf")
    print("· 第一次排版 ...")
    render(p1, pdf1, footer=True)

    print("· 计算目录页码 ...")
    pages, missing, start = find_pages(pdf1, heads)
    if missing:
        print("  未能定位的标题：", missing[:8])

    def fill(m):
        hid = m.group(1)
        return '<span class="pg" data-hid="%s">%s</span>' % (hid, pages.get(hid, ""))

    full2 = re.sub(r'<span class="pg" data-hid="([^"]*)"></span>', fill, full)
    p2 = os.path.join(BUILD, "body.html")
    with open(p2, "w", encoding="utf-8") as f:
        f.write(page(TITLE, full2))
    pdf2 = os.path.join(BUILD, "body.pdf")
    print("· 第二次排版 ...")
    render(p2, pdf2, footer=True)

    print("· 生成封面与辅文 ...")
    cover = build_special("cover", COVER.format(cover=COVER_ART, title=TITLE,
                                                subtitle=SUBTITLE, author=AUTHOR, year=YEAR),
                          os.path.join(BUILD, "cover.pdf"))
    titlepage = build_special("titlepage", TITLEPAGE.format(title=TITLE, subtitle=SUBTITLE,
                                                            author=AUTHOR, year=YEAR),
                              os.path.join(BUILD, "titlepage.pdf"))
    copyright_pdf = build_special("copyright", COPYRIGHT.format(title=TITLE, subtitle=SUBTITLE,
                                                                author=AUTHOR, year=YEAR,
                                                                VERSION=VERSION),
                                  os.path.join(BUILD, "copyright.pdf"))
    back = build_special("back", BACK.format(author=AUTHOR), os.path.join(BUILD, "back.pdf"))

    print("· 合并并写入书签 ...")
    import fitz
    out = fitz.open()
    out.insert_pdf(fitz.open(cover))
    out.insert_pdf(fitz.open(titlepage))
    out.insert_pdf(fitz.open(copyright_pdf))
    body_doc = fitz.open(pdf2)
    out.insert_pdf(body_doc)
    out.insert_pdf(fitz.open(back))

    offset = 3
    toc = [[1, TITLE, 1]]
    for lvl, hid, txt in heads:
        toc.append([lvl, re.sub(r"<[^>]+>", "", txt), pages.get(hid, 1) + offset])
    out.set_toc(toc)
    out.set_metadata({"title": TITLE, "author": AUTHOR, "subject": SUBTITLE,
                      "keywords": "C++, 插件系统, 动态库, 事件总线, 钩子, 组件化"})
    try:
        out.subset_fonts(verbose=False)
    except Exception as exc:
        print("· 字体子集化警告：", exc)

    target = OUT_PDF
    if "--out" in sys.argv:
        target = os.path.join(ROOT, sys.argv[sys.argv.index("--out") + 1])
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
        raise SystemExit("保存 PDF 失败：%s\n多半是文件正被阅读器占用，关掉后重试。" % e)
    if os.path.exists(tmp):
        try:
            os.remove(tmp)
        except OSError:
            pass
    page_count = len(out)
    out.close()

    guard = os.path.join(BOOK, "build", "checks", "pdf_size_guard.py")
    if os.path.exists(guard):
        result = subprocess.run([sys.executable, guard, target])
        if result.returncode != 0:
            raise SystemExit("PDF 体积检查未通过；请压缩插图后重试。")

    print("完成：%s  共 %d 页" % (target, page_count))

    if "--keep" not in sys.argv:
        for name in ("body_pass1.html", "body_pass1.pdf", "body.html"):
            path = os.path.join(BUILD, name)
            if os.path.exists(path):
                try:
                    os.remove(path)
                except OSError:
                    pass


if __name__ == "__main__":
    main()
