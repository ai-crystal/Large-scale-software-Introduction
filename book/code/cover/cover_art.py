# -*- coding: utf-8 -*-
"""生成封面背景图（纯代码绘制，不含文字，文字由排版层叠加）。"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
from matplotlib.lines import Line2D

W, H = 170, 240
DPI = 150
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))), "build", "assets", "cover", "cover.png")

BG = "#08111a"
GRID = "#132233"
BLUE = "#4f9dc0"
ORANGE = "#d08a3e"
SLATE = "#26405a"


fig = plt.figure(figsize=(W / 25.4, H / 25.4), dpi=DPI)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W)
ax.set_ylim(0, H)
ax.axis("off")
fig.patch.set_facecolor(BG)

for x in range(0, W + 1, 10):
    ax.add_line(Line2D([x, x], [0, H], color=GRID, lw=0.4, alpha=0.5, zorder=0))
for y in range(0, H + 1, 10):
    ax.add_line(Line2D([0, W], [y, y], color=GRID, lw=0.4, alpha=0.5, zorder=0))

for cx, cy, r in [(120, 190, 55), (50, 160, 40)]:
    for k in range(14, 0, -1):
        ax.add_patch(Circle((cx, cy), r * k / 14, color="#102030", alpha=0.035, lw=0, zorder=0))

# 起点：一个小程序
ax.add_patch(FancyBboxPatch((18, 148), 16, 16, boxstyle="round,pad=0,rounding_size=2",
                            linewidth=1.1, edgecolor=ORANGE, facecolor="#121c26", zorder=3))
ax.add_line(Line2D([22, 30], [156, 156], color=ORANGE, lw=1.2, alpha=0.9, zorder=4))
ax.add_line(Line2D([22, 27], [152, 152], color=ORANGE, lw=1.0, alpha=0.6, zorder=4))

# 中间：拆成几个模块
mods = [(44, 166, 18, 13), (44, 149, 18, 13), (44, 132, 18, 13)]
for (x, y, w, h) in mods:
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=1.4",
                                linewidth=0.8, edgecolor=SLATE, facecolor="#101b28", zorder=3))
    ax.add_line(Line2D([x + 3, x + 11], [y + h - 3.5, y + h - 3.5],
                       color=BLUE, lw=0.9, alpha=0.5, zorder=4))

ax.add_patch(FancyArrowPatch((34, 158), (43, 170), arrowstyle="-|>", mutation_scale=7,
                             linewidth=0.8, color=ORANGE, alpha=0.75, zorder=4))
ax.add_patch(FancyArrowPatch((34, 156), (43, 156), arrowstyle="-|>", mutation_scale=7,
                             linewidth=0.9, color=ORANGE, alpha=0.9, zorder=4))
ax.add_patch(FancyArrowPatch((34, 154), (43, 140), arrowstyle="-|>", mutation_scale=7,
                             linewidth=0.8, color=ORANGE, alpha=0.75, zorder=4))

# 外壳：大框
ax.add_patch(FancyBboxPatch((80, 126), 54, 62, boxstyle="round,pad=0,rounding_size=3",
                            linewidth=1.2, edgecolor="#3c5a78", facecolor="#0b1622", zorder=2))
ax.add_patch(FancyBboxPatch((84, 132), 46, 7, boxstyle="round,pad=0,rounding_size=1.2",
                            linewidth=0.8, edgecolor=ORANGE, facecolor="#121a20", zorder=3))
ax.add_line(Line2D([87, 99], [135.5, 135.5], color=ORANGE, lw=1.2, alpha=0.9, zorder=4))

for (x, y, w, h) in [(85, 146, 18, 14), (107, 146, 21, 14),
                     (85, 164, 18, 14), (107, 164, 21, 14)]:
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=1.2",
                                linewidth=0.7, edgecolor="#3f6386", facecolor="#101d2b",
                                alpha=0.95, zorder=3))
    ax.add_line(Line2D([x + 3, x + 10], [y + h - 4, y + h - 4],
                       color=BLUE, lw=0.9, alpha=0.5, zorder=4))

for (x1, y1, x2, y2) in [(62, 172, 79, 170), (62, 155, 79, 155), (62, 138, 79, 142)]:
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=7,
                                 linewidth=0.9, color=BLUE, alpha=0.85, zorder=4))

# 插件：虚线框接入外壳
for (x, y, color) in [(140, 156, ORANGE), (140, 134, BLUE)]:
    ax.add_patch(FancyBboxPatch((x, y), 12, 12, boxstyle="round,pad=0,rounding_size=1.4",
                                linewidth=0.9, edgecolor=color, facecolor="none",
                                linestyle=(0, (3, 2)), alpha=0.9, zorder=4))
    ax.add_patch(FancyArrowPatch((140, y + 6), (134, y + 6), arrowstyle="-|>", mutation_scale=7,
                                 linewidth=0.9, color=color, alpha=0.85, zorder=4))
    ax.add_patch(Circle((134, y + 6), 0.9, facecolor=BG, edgecolor=color, linewidth=0.9, zorder=5))

os.makedirs(os.path.dirname(OUT), exist_ok=True)
fig.savefig(OUT, dpi=DPI, facecolor=BG)
plt.close(fig)
print("wrote", OUT)
