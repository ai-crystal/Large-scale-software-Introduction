# -*- coding: utf-8 -*-
"""第 5 章插图。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "common"))
from figstyle import canvas, box, text, arrow, save, BLUE, BLUE_L, GOLD, GOLD_L, GRAY, GRAY_L, INK, GREEN, GREEN_L

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def fig_5_1():
    fig, ax = canvas(132, 64)

    box(ax, 4, 40, 26, 12, "hello 插件", fc=GREEN_L, ec=GREEN, size=6.8)
    box(ax, 4, 16, 26, 12, "notes 插件", fc=GREEN_L, ec=GREEN, size=6.8)

    box(ax, 44, 8, 52, 50, "", fc="white", ec=BLUE, lw=1.0)
    text(ax, 48, 53, "命令表", size=7.2, weight="bold", color=BLUE, ha="left")

    rows = [
        ("hello", "owner = hello", 44, BLUE_L),
        ("note", "owner = notes", 31, BLUE_L),
        ("help", "owner = core", 18, GRAY_L),
    ]
    for name, owner, y, fill in rows:
        box(ax, 48, y, 20, 9, name, fc=fill, ec=GRAY, size=5.8)
        text(ax, 72, y + 4.5, owner, size=5.4, color=GRAY, ha="left")

    box(ax, 106, 28, 22, 12, "执行命令", fc=GOLD_L, ec=GOLD, size=6.6)
    arrow(ax, (30, 46), (48, 48), color=GREEN, shrink=0.2)
    arrow(ax, (30, 22), (48, 36), color=GREEN, shrink=0.2)
    arrow(ax, (96, 34), (106, 34), color=GOLD, shrink=0.2)

    text(ax, 66, 4, "每条记录都带 owner，卸载时按 owner 一次清干净", size=5.8, color=GRAY)
    save(fig, os.path.join(ROOT, "images", "05", "fig5-1-registry.png"))


if __name__ == "__main__":
    fig_5_1()
