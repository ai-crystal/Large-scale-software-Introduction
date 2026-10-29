# -*- coding: utf-8 -*-
"""第 10 章插图。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "common"))
from figstyle import canvas, box, text, arrow, save, BLUE, BLUE_L, GOLD, GOLD_L, GRAY, GRAY_L, INK, GREEN, GREEN_L

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def fig_10_1():
    fig, ax = canvas(132, 58)

    box(ax, 4, 10, 46, 38, "", fc=GRAY_L, ec=GRAY, lw=1.0)
    text(ax, 27, 43, "hello-1.2.0.zip", size=6.8, weight="bold", color=INK)
    for i, name in enumerate(["plugin.json", "hello.dll", "README.md"]):
        text(ax, 10, 34 - i * 8, name, size=6.0, color=INK, ha="left")

    steps = [
        (60, 34, "按路径排序\n逐个算哈希"),
        (60, 18, "私钥签名\n写进包里"),
        (60, 2, "用户用公钥\n重新验证"),
    ]
    for x, y, label in steps:
        box(ax, x, y, 34, 12, label, fc="white", ec=BLUE, size=5.8, wrap=9)

    arrow(ax, (50, 29), (60, 40), color=GRAY, shrink=0.2)
    arrow(ax, (77, 34), (77, 30), color=GRAY, shrink=0.2)
    arrow(ax, (77, 18), (77, 14), color=GRAY, shrink=0.2)

    text(ax, 100, 36, "签名覆盖\n路径 + 内容", size=5.6, color=GRAY, ha="left")
    text(ax, 100, 12, "任何一步不对\n拒绝安装", size=5.6, color=GRAY, ha="left")

    save(fig, os.path.join(ROOT, "images", "10", "fig10-1-package.png"))


if __name__ == "__main__":
    fig_10_1()
