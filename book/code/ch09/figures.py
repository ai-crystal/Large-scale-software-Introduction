# -*- coding: utf-8 -*-
"""第 9 章插图。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "common"))
from figstyle import canvas, box, text, arrow, save, BLUE, BLUE_L, GOLD, GOLD_L, GRAY, INK, GREEN, GREEN_L

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def fig_9_1():
    fig, ax = canvas(132, 50)

    rows = [
        (32, "单元测试", "只跑逻辑，几百毫秒", GREEN, GREEN_L),
        (18, "假宿主", "加载插件、看注册，几秒", BLUE, BLUE_L),
        (4, "真实宿主", "完整流程，分钟级", GOLD, GOLD_L),
    ]
    for y, name, note, edge, fill in rows:
        box(ax, 6, y, 30, 11, name, fc=fill, ec=edge, size=6.8, weight="bold")
        text(ax, 42, y + 5.5, note, size=6.0, color=INK, ha="left")

    arrow(ax, (60, 37), (60, 16), color=GRAY, shrink=0.2)
    text(ax, 62, 26, "越往下越接近真实，也越慢", size=5.8, color=GRAY, ha="left")

    save(fig, os.path.join(ROOT, "images", "09", "fig9-1-loop.png"))


if __name__ == "__main__":
    fig_9_1()
