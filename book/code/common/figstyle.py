# -*- coding: utf-8 -*-
"""统一的插图样式与绘图工具。

约定：
- 画布按毫米计算，宽度 132mm，正好等于 A5 正文栏宽。
- 图内不写标题，标题由 Markdown 的图片说明承担。
- 文字一律用微软雅黑，避免中文缺字。
"""
import os
import subprocess
import tempfile
import textwrap

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle, Circle, Polygon
from matplotlib.lines import Line2D

FONT = "Microsoft YaHei"
INK = "#1b2733"
BLUE = "#1f3a5f"
BLUE_L = "#e8eef6"
GOLD = "#b08a2e"
GOLD_L = "#f6efdd"
GRAY = "#6b7280"
GRAY_L = "#f1f3f5"
RED = "#9b3b32"
RED_L = "#f7e9e7"
GREEN = "#2f6b4f"
GREEN_L = "#e8f2ec"

DOT = r"D:/DevTools/Graphviz-15.0.0-win32/bin/dot.exe"

plt.rcParams["font.family"] = FONT
plt.rcParams["axes.unicode_minus"] = False


def canvas(width_mm=132, height_mm=60, dpi=220):
    fig = plt.figure(figsize=(width_mm / 25.4, height_mm / 25.4), dpi=dpi)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, width_mm)
    ax.set_ylim(0, height_mm)
    ax.axis("off")
    fig.patch.set_facecolor("white")
    return fig, ax


def text(ax, x, y, s, size=7.4, color=INK, weight="normal", ha="center", va="center",
         rotation=0, wrap=None, lh=1.35):
    if wrap:
        s = "\n".join(textwrap.wrap(s, wrap))
    return ax.text(x, y, s, fontsize=size, color=color, fontweight=weight,
                   ha=ha, va=va, rotation=rotation, linespacing=lh, zorder=6)


def box(ax, x, y, w, h, label="", fc="white", ec=BLUE, lw=1.0, size=7.2,
        color=INK, weight="normal", rounding=1.2, ls="solid", wrap=None, pad=0.6):
    patch = FancyBboxPatch((x, y), w, h,
                           boxstyle=f"round,pad=0,rounding_size={rounding}",
                           linewidth=lw, edgecolor=ec, facecolor=fc,
                           linestyle=ls, zorder=3)
    ax.add_patch(patch)
    if label:
        text(ax, x + w / 2, y + h / 2, label, size=size, color=color,
             weight=weight, wrap=wrap)
    return (x, y, w, h)


def edge_point(b, tx, ty):
    """从矩形中心指向 (tx,ty) 的射线与矩形边界的交点。"""
    x, y, w, h = b
    cx, cy = x + w / 2, y + h / 2
    dx, dy = tx - cx, ty - cy
    if dx == 0 and dy == 0:
        return cx, cy
    sx = (w / 2) / abs(dx) if dx else float("inf")
    sy = (h / 2) / abs(dy) if dy else float("inf")
    s = min(sx, sy)
    return cx + dx * s, cy + dy * s


def arrow(ax, src, dst, label="", color=GRAY, lw=1.0, style="-|>", both=False,
          rad=0.0, size=6.4, label_offset=(0, 0), shrink=0.6, zorder=2, ls="solid"):
    sx, sy = src
    dx, dy = dst
    if isinstance(src, tuple) and len(src) == 4:
        sx, sy = edge_point(src, dx, dy)
    if isinstance(dst, tuple) and len(dst) == 4:
        dx, dy = edge_point(dst, sx, sy)
    patch = FancyArrowPatch((sx, sy), (dx, dy),
                            arrowstyle=("<|-|>" if both else style),
                            mutation_scale=7.5, linewidth=lw, color=color,
                            connectionstyle=f"arc3,rad={rad}", zorder=zorder, linestyle=ls,
                            shrinkA=shrink * 2, shrinkB=shrink * 2)
    ax.add_patch(patch)
    if label:
        mx, my = (sx + dx) / 2 + label_offset[0], (sy + dy) / 2 + label_offset[1]
        ax.text(mx, my, label, fontsize=size, color=color, ha="center", va="center",
                bbox=dict(boxstyle="round,pad=0.16", fc="white", ec="none", alpha=0.92),
                zorder=8)


def line(ax, x1, y1, x2, y2, color=GRAY, lw=0.8, ls="solid", zorder=1):
    ax.add_line(Line2D([x1, x2], [y1, y2], color=color, lw=lw, ls=ls, zorder=zorder))


def save(fig, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fig.savefig(path, dpi=fig.dpi, facecolor="white", bbox_inches=None)
    plt.close(fig)
    print("wrote", path)


def render_dot(source, out_path, dpi=200):
    """用 Graphviz 渲染，自动布局，避免手工坐标造成的遮挡。"""
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        dot_path = os.path.join(tmp, "fig.dot")
        with open(dot_path, "w", encoding="utf-8") as fh:
            fh.write(source)
        subprocess.run([DOT, "-Tpng", f"-Gdpi={dpi}", "-o", out_path, dot_path],
                       check=True, capture_output=True)
    print("wrote", out_path)


def dot_graph(body, rankdir="TB", nodesep=0.28, ranksep=0.42, fontsize=10, node_width=None):
    """包一层统一的 Graphviz 样式。body 里用 node/edge 语句。"""
    return f'''digraph G {{
  graph [rankdir={rankdir}, bgcolor="white", nodesep={nodesep}, ranksep={ranksep},
         pad=0.12, fontname="{FONT}"];
  node [shape=box, style="rounded,filled", fillcolor="{BLUE_L}", color="{BLUE}",
        penwidth=1.0, fontname="{FONT}", fontsize={fontsize}, fontcolor="{INK}",
        margin="0.16,0.09"{", width=" + str(node_width) if node_width else ""}];
  edge [color="{GRAY}", penwidth=1.0, arrowsize=0.7, fontname="{FONT}",
        fontsize={fontsize - 1.2}, fontcolor="{GRAY}"];
{body}
}}
'''
