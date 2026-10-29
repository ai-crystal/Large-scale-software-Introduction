# -*- coding: utf-8 -*-
"""第 2 章插图。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "common"))
from figstyle import (canvas, box, text, arrow, line, save, render_dot, dot_graph,
                      BLUE, BLUE_L, GOLD, GOLD_L, GRAY, GRAY_L, INK, GREEN, GREEN_L)

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def fig_2_1():
    fig, ax = canvas(132, 58)

    box(ax, 4, 34, 26, 11, "main.cpp", fc="white", ec=BLUE, size=6.6)
    box(ax, 4, 16, 26, 11, "commands.cpp", fc="white", ec=BLUE, size=6.6)
    box(ax, 42, 34, 24, 11, "main.obj", fc=GRAY_L, ec=GRAY, size=6.6)
    box(ax, 42, 16, 24, 11, "commands.obj", fc=GRAY_L, ec=GRAY, size=6.6)
    box(ax, 78, 24, 22, 14, "链接器", fc=GOLD_L, ec=GOLD, size=7.2, weight="bold")
    box(ax, 108, 24, 20, 14, "app.exe", fc=GREEN_L, ec=GREEN, size=7.0, weight="bold")

    arrow(ax, (30, 39.5), (42, 39.5), color=BLUE, shrink=0.2)
    arrow(ax, (30, 21.5), (42, 21.5), color=BLUE, shrink=0.2)
    arrow(ax, (66, 39.5), (78, 35), color=GRAY, shrink=0.2)
    arrow(ax, (66, 21.5), (78, 27), color=GRAY, shrink=0.2)
    arrow(ax, (100, 31), (108, 31), color=GRAY, shrink=0.2)

    text(ax, 36, 43, "编译", size=6.0, color=BLUE)
    text(ax, 71, 46, "链接", size=6.0, color=GRAY)
    text(ax, 66, 8, "编译一次处理一个源文件，链接器负责把符号接上", size=5.8, color=GRAY)

    save(fig, os.path.join(ROOT, "images", "02", "fig2-1-build.png"))


def fig_2_2():
    fig, ax = canvas(132, 66)

    # 静态库
    text(ax, 32, 60, "静态库", size=7.6, weight="bold", color=BLUE)
    box(ax, 4, 36, 60, 18, "", fc=BLUE_L, ec=BLUE, size=6.4)
    text(ax, 10, 49, "app.exe", size=6.6, weight="bold", color=BLUE, ha="left")
    for i, name in enumerate(["main.obj", "cmd.obj", "库代码"]):
        box(ax, 8 + i * 18, 39, 16, 7, name, fc="white", ec=GRAY, size=5.2)
    text(ax, 4, 30, "链接时复制进程序，体积大，更新要重新链接", size=5.6, color=GRAY, ha="left")

    # 动态库
    text(ax, 100, 60, "动态库", size=7.6, weight="bold", color=GOLD)
    box(ax, 70, 36, 30, 12, "app.exe", fc=GREEN_L, ec=GREEN, size=6.4)
    box(ax, 104, 36, 24, 12, "plugin.dll", fc=GOLD_L, ec=GOLD, size=5.4)
    arrow(ax, (100, 42), (104, 42), color=GOLD, shrink=0.2)
    text(ax, 70, 30, "运行时才加载，多个程序共用，更新只换库文件", size=5.6, color=GRAY, ha="left")

    line(ax, 4, 20, 128, 20, color="#dde3ea", lw=0.8)
    text(ax, 66, 12, "插件系统依赖动态库：不重新编译主程序，也能增加功能", size=6.2, color=INK)

    save(fig, os.path.join(ROOT, "images", "02", "fig2-2-libs.png"))


if __name__ == "__main__":
    fig_2_1()
    fig_2_2()
