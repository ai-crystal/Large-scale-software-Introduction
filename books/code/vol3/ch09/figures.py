# -*- coding: utf-8 -*-
"""第 9 章插图：一次保存的追踪树，日志与指标的采集去向。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "common", "figstyle"))
from figstyle import canvas, box, text, arrow, line, save, INK, BLUE, BLUE_L, GOLD, GOLD_L, GRAY, GRAY_L, RED, RED_L, GREEN, GREEN_L

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))), "vol3-engineering")


def fig_9_1():
    fig, ax = canvas(132, 92)

    rows = [
        (0, None, "save_document", "145ms", BLUE_L, BLUE, False),
        (1, 0, "hook.before_save", "17ms", BLUE_L, BLUE, False),
        (2, 1, "tools", "2ms", "white", BLUE, False),
        (2, 1, "formatter", "15ms", RED_L, RED, True),
        (1, 0, "write_file", "8ms", BLUE_L, BLUE, False),
        (1, 0, "event.file_saved", "120ms", BLUE_L, BLUE, False),
        (2, 5, "indexer", "118ms", RED_L, RED, True),
    ]
    widths = [62, 52, 42]

    geo = {}
    y = 82
    for i, (level, parent, name, ms, fc, ec, slow) in enumerate(rows):
        x = 6 + level * 13
        w = widths[level]
        box(ax, x, y, w, 7.6, name, fc=fc, ec=ec, size=5.8)
        text(ax, x + w + 3, y + 3.8, ms, size=5.4, color=RED if slow else GRAY, ha="left")
        geo[i] = (x, y, w, y + 3.8)
        y -= 10.5

    children = {}
    for i, (level, parent, *_rest) in enumerate(rows):
        if parent is not None:
            children.setdefault(parent, []).append(i)

    for parent, kids in children.items():
        px, py, pw, pcy = geo[parent]
        bx = px - 3.5
        cy_first = geo[kids[0]][3]
        cy_last = geo[kids[-1]][3]
        line(ax, bx, pcy, bx, cy_last, color=GRAY, lw=0.7)
        line(ax, bx, pcy, px, pcy, color=GRAY, lw=0.7)
        for kid in kids:
            kx = geo[kid][0]
            line(ax, bx, geo[kid][3], kx, geo[kid][3], color=GRAY, lw=0.7)

    text(ax, 66, 4.5, "整条链路 145ms，其中 118ms 花在 indexer 上，前四个钩子加起来不到二十毫秒",
         size=5.8, color=GRAY)

    save(fig, os.path.join(ROOT, "images", "09", "fig9-1.png"))


def fig_9_2():
    fig, ax = canvas(132, 62)

    box(ax, 4, 24, 26, 14, "插件 A / B / C\nlog · metric · span", fc=BLUE_L, ec=BLUE, size=5.8)
    box(ax, 42, 24, 30, 14, "宿主收集器\n补归属 · 加时间 · 采样", fc=GOLD_L, ec=GOLD, size=5.8)

    box(ax, 88, 42, 40, 11, "日志文件\n按大小轮转，有配额", fc="white", ec=BLUE, size=5.4)
    box(ax, 88, 25, 40, 11, "内存环形缓冲\n崩溃时随报告带走", fc="white", ec=BLUE, size=5.4)
    box(ax, 88, 8, 40, 11, "诊断面板与上报\n用户能看，开发者能查", fc="white", ec=BLUE, size=5.4)

    arrow(ax, (30, 31), (42, 31), color=GRAY, shrink=0.2)
    arrow(ax, (72, 31), (88, 47), color=GRAY, shrink=0.2)
    arrow(ax, (72, 31), (88, 30), color=GRAY, shrink=0.2)
    arrow(ax, (72, 31), (88, 13), color=GRAY, shrink=0.2)

    save(fig, os.path.join(ROOT, "images", "09", "fig9-2.png"))


if __name__ == "__main__":
    fig_9_1()
    fig_9_2()
