# -*- coding: utf-8 -*-
"""第 4 章插图。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "common"))
from figstyle import (canvas, box, text, arrow, line, save,
                      BLUE, BLUE_L, GOLD, GOLD_L, GRAY, GRAY_L, INK, GREEN, GREEN_L)

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def fig_4_1_flow():
    fig, ax = canvas(132, 84)

    text(ax, 30, 79, "宿主", size=7.6, weight="bold", color=BLUE)
    text(ax, 99, 79, "插件", size=7.6, weight="bold", color=GREEN)
    line(ax, 66, 4, 66, 76, color="#d5dbe2", lw=0.8, ls=(0, (5, 4)))

    steps_left = [
        (68, "1  建一张空表"),
        (58, "2  准备工具箱 PluginApi"),
        (48, "3  调用 plugin_init，递工具箱"),
        (22, "5  注册函数被调用，收到命令"),
        (12, "6  复制进表"),
        (2, "7  用户输入 hello，查表调用 run_hello"),
    ]
    for y, label in steps_left:
        box(ax, 6, y, 54, 7.5, label, fc="white", ec=BLUE, size=5.9)

    box(ax, 72, 35, 54, 9, "4  从工具箱取出注册函数", fc=GREEN_L, ec=GREEN, size=5.9)

    arrow(ax, (33, 68), (33, 65.5), color=GRAY, shrink=0.2)
    arrow(ax, (33, 58), (33, 55.5), color=GRAY, shrink=0.2)
    arrow(ax, (60, 51.5), (72, 41), color=GOLD, shrink=0.2)
    text(ax, 64, 55, "交给", size=5.4, color=GOLD)
    arrow(ax, (72, 38), (60, 25.5), color=GOLD, shrink=0.2)
    text(ax, 70, 32, "回调", size=5.4, color=GOLD)
    arrow(ax, (33, 22), (33, 19.5), color=GRAY, shrink=0.2)
    arrow(ax, (33, 12), (33, 9.5), color=GRAY, shrink=0.2)

    save(fig, os.path.join(ROOT, "images", "04", "fig4-1-flow.png"))


def fig_4_2_layout():
    fig, ax = canvas(132, 54)

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
    text(ax, 4, 12, "sizeof(PluginApi) = 24 字节，插件用 size 判断宿主提供了哪些字段", size=6.0, color=GRAY, ha="left")
    text(ax, 4, 7, "四个字段按声明顺序排列，两个函数指针各占 8 字节", size=6.0, color=GRAY, ha="left")

    save(fig, os.path.join(ROOT, "images", "04", "fig4-2-layout.png"))


if __name__ == "__main__":
    fig_4_1_flow()
    fig_4_2_layout()
