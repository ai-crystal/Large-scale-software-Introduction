# -*- coding: utf-8 -*-
"""第 4 章插图。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "common"))
from figstyle import canvas, box, text, save, BLUE, BLUE_L, GOLD, GOLD_L, GRAY, GRAY_L, INK

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def fig_4_1():
    fig, ax = canvas(132, 54)

    total = 112
    parts = [
        (4, 14, "size", "4 字节", GOLD_L, GOLD),
        (18, 14, "version", "4 字节", GOLD_L, GOLD),
        (32, 42, "register_command", "8 字节", BLUE_L, BLUE),
        (74, 42, "log_info", "8 字节", BLUE_L, BLUE),
    ]
    for x, w, name, note, fill, edge in parts:
        box(ax, x, 26, w, 14, name, fc=fill, ec=edge, size=6.0)
        text(ax, x + w / 2, 21, note, size=5.6, color=GRAY)

    text(ax, 4, 46, "PluginApi 在内存里的样子（64 位程序）", size=6.6, color=INK, ha="left")
    text(ax, 4, 12, "sizeof(PluginApi) = 24 字节，宿主用 size 判断插件结构体有多大", size=6.0, color=GRAY, ha="left")
    text(ax, 4, 7, "两个 64 位指针各自占 8 字节，四个字段按声明顺序排列", size=6.0, color=GRAY, ha="left")

    save(fig, os.path.join(ROOT, "images", "04", "fig4-1-layout.png"))


if __name__ == "__main__":
    fig_4_1()
