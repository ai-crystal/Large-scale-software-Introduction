# -*- coding: utf-8 -*-
"""第 8 章插图。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "common"))
from figstyle import canvas, box, text, line, save, BLUE, BLUE_L, GOLD, GOLD_L, GRAY, GRAY_L, INK, GREEN, GREEN_L

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def fig_8_1():
    fig, ax = canvas(132, 62)

    box(ax, 4, 24, 28, 11, "my-plugin", fc=BLUE_L, ec=BLUE, size=7.0, weight="bold")

    rows = [
        (48, "CMakeLists.txt", "构建说明"),
        (38, "plugin.json", "清单"),
        (28, "README.md", "用法说明"),
        (18, "include/plugin_api.h", "接口头文件"),
        (8, "src/plugin.cpp", "命令与初始化"),
    ]
    for y, name, note in rows:
        box(ax, 44, y, 44, 8, name, fc="white", ec=GRAY, size=5.8)
        text(ax, 92, y + 4, note, size=5.6, color=GRAY, ha="left")
        line(ax, 32, 29, 38, y + 4, color="#c3cad3", lw=0.8)
        line(ax, 38, y + 4, 44, y + 4, color="#c3cad3", lw=0.8)

    text(ax, 66, 58, "生成后直接能编译、能加载，作者只填业务", size=6.0, color=INK)

    save(fig, os.path.join(ROOT, "images", "08", "fig8-1-template.png"))


if __name__ == "__main__":
    fig_8_1()
