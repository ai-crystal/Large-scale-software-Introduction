# -*- coding: utf-8 -*-
"""第 7 章插图。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "common"))
from figstyle import canvas, box, text, arrow, line, save, BLUE, BLUE_L, GOLD, GOLD_L, GRAY, GRAY_L, INK, GREEN, GREEN_L, RED

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def fig_7_1():
    fig, ax = canvas(132, 64)

    box(ax, 4, 12, 44, 40, "", fc=BLUE_L, ec=BLUE, lw=1.0)
    text(ax, 8, 46, "宿主进程", size=7.4, weight="bold", color=BLUE, ha="left")
    text(ax, 8, 38, "主循环 · 注册表", size=6.0, color=INK, ha="left")
    text(ax, 8, 31, "超时计时", size=6.0, color=INK, ha="left")
    text(ax, 8, 24, "插件管理器", size=6.0, color=INK, ha="left")

    box(ax, 84, 12, 44, 40, "", fc=GREEN_L, ec=GREEN, lw=1.0)
    text(ax, 88, 46, "插件进程", size=7.4, weight="bold", color=GREEN, ha="left")
    text(ax, 88, 38, "读一行消息", size=6.0, color=INK, ha="left")
    text(ax, 88, 31, "执行命令", size=6.0, color=INK, ha="left")
    text(ax, 88, 24, "写一行结果", size=6.0, color=INK, ha="left")

    arrow(ax, (48, 40), (84, 40), color=GOLD, shrink=0.2)
    text(ax, 66, 43.5, "写 → 读", size=5.6, color=GOLD)
    arrow(ax, (84, 24), (48, 24), color=BLUE, shrink=0.2)
    text(ax, 66, 27.5, "写 ← 读", size=5.6, color=BLUE)

    line(ax, 4, 8, 128, 8, color="#dde3ea", lw=0.8)
    text(ax, 66, 4, "等太久：杀掉进程，宿主继续运行；下次启动可以重启它", size=5.8, color=RED)

    save(fig, os.path.join(ROOT, "images", "07", "fig7-1-process.png"))


if __name__ == "__main__":
    fig_7_1()
