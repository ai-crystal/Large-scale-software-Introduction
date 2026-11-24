# -*- coding: utf-8 -*-
"""模式篇插图的共用画法。

图一律交给 Graphviz 自动布局，避免手工坐标造成文字压线。
两件事在这里统一处理：

1. 版式比例。图在书里占满 132mm 栏宽，太高的图会被压小，太宽的图
   会缩成一条细带。这里先在 LR / TB 之间挑一个，再按需要的宽度收
   紧节点间距。
2. 字号。缩放到 132mm 之后，图里的字要和正文（9pt）接近，实测换算
   后落在 7~9pt 之间。

图内不写标题，标题由 Markdown 的图片说明承担。
"""
import os
import subprocess
import sys
import tempfile

from PIL import Image

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..",
                                "common", "figstyle"))
from figstyle import DOT, dot_graph  # noqa: E402

DPI = 200
COLUMN_MM = 132.0
TARGET_MM = 148.0     # 原图宽度目标：略宽于栏宽，缩一点刚好
MIN_RATIO = 1.25


def _render(body, rankdir, fontsize, ranksep, nodesep, out_path):
    with tempfile.TemporaryDirectory() as tmp:
        dot_path = os.path.join(tmp, "fig.dot")
        with open(dot_path, "w", encoding="utf-8") as fh:
            fh.write(dot_graph(body, rankdir=rankdir, fontsize=fontsize,
                               ranksep=ranksep, nodesep=nodesep))
        subprocess.run([DOT, "-Tpng", f"-Gdpi={DPI}", "-o", out_path, dot_path],
                       check=True, capture_output=True)
    w, h = Image.open(out_path).size
    return w, h


def _mm(px):
    return px / DPI * 25.4


def _probe(body, rankdir, fontsize=10.0):
    with tempfile.TemporaryDirectory() as tmp:
        w, h = _render(body, rankdir, fontsize, 0.42, 0.28, os.path.join(tmp, "p.png"))
    return w / h


def _fit_layout(body):
    """先保证图别太瘦长，再让比例靠近 2。"""
    cands = [(rd, _probe(body, rd)) for rd in ("LR", "TB")]
    ok = [(rd, r) for rd, r in cands if r >= MIN_RATIO]
    pool = ok or sorted(cands, key=lambda c: -c[1])[:1]
    return min(pool, key=lambda c: abs(c[1] - 2.0))[0]


def render_roles(body, out_path, rankdir="auto", fontsize=10.0):
    if rankdir == "auto":
        rankdir = _fit_layout(body)

    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    # 第一遍：默认间距，看原图多宽
    with tempfile.TemporaryDirectory() as tmp:
        w, h = _render(body, rankdir, fontsize, 0.42, 0.28, os.path.join(tmp, "p.png"))
    width_mm = _mm(w)

    # 太宽就收紧间距，太窄就放宽，字号在窄图里适当减小免得字撑破框
    scale = max(0.16, min(1.0, TARGET_MM / width_mm))
    ranksep = max(0.10, 0.42 * scale)
    nodesep = max(0.08, 0.28 * scale)

    w, h = _render(body, rankdir, fontsize, ranksep, nodesep, out_path)
    width_mm = _mm(w)
    if width_mm < COLUMN_MM * 0.8 and fontsize > 8.0:
        # 图本身很窄，说明内容少，缩小字号让方框与文字比例正常
        fontsize *= max(0.72, width_mm / (COLUMN_MM * 0.8))
        w, h = _render(body, rankdir, fontsize, ranksep, nodesep, out_path)
        width_mm = _mm(w)

    shown = fontsize * COLUMN_MM / width_mm
    print("wrote %-52s %4.0fx%-4.0f %5.1fmm x %5.1fmm  比例 %.2f  显示字号 %.1fpt"
          % (os.path.relpath(out_path), w, h, width_mm, _mm(h), w / h, shown))
    return out_path
