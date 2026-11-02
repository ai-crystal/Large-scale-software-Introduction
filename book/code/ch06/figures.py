# -*- coding: utf-8 -*-
"""第 6 章插图。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "common"))
from figstyle import canvas, box, text, arrow, line, save, BLUE, BLUE_L, GOLD, GOLD_L, GRAY, INK, GREEN, GREEN_L

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def fig_6_1():
    fig, ax = canvas(132, 64)

    text(ax, 33, 59, "事件：通知", size=7.6, weight="bold", color=BLUE)
    text(ax, 99, 59, "钩子：修改", size=7.6, weight="bold", color=GOLD)
    line(ax, 65, 6, 65, 56, color="#dde3ea", lw=0.8, ls=(0, (5, 4)))

    box(ax, 22, 40, 22, 10, "保存插件", fc="white", ec=BLUE, size=6.4)
    box(ax, 20, 24, 26, 12, "事件总线", fc=BLUE_L, ec=BLUE, size=6.8, weight="bold")
    for i, x in enumerate((6, 24, 42)):
        box(ax, x, 8, 16, 9, f"监听者 {i+1}", fc="white", ec=GREEN, size=5.6)
    arrow(ax, (33, 40), (33, 36), color=BLUE, shrink=0.2)
    arrow(ax, (27, 24), (14, 17), color=GREEN, shrink=0.2)
    arrow(ax, (33, 24), (32, 17), color=GREEN, shrink=0.2)
    arrow(ax, (39, 24), (50, 17), color=GREEN, shrink=0.2)
    text(ax, 33, 3, "发出去就不管结果", size=5.6, color=GRAY)

    xs = [68, 82, 96, 110]
    labels = ["输入", "钩子 1", "钩子 2", "输出"]
    for x, label in zip(xs, labels):
        box(ax, x, 26, 12, 12, label, fc=GOLD_L if "钩子" in label else "white",
            ec=GOLD, size=5.6)
    for i in range(3):
        arrow(ax, (xs[i] + 12, 32), (xs[i + 1], 32), color=GOLD, shrink=0.2)
    text(ax, 99, 20, "每个环节可以改数据、阻止流程", size=5.6, color=GRAY)

    save(fig, os.path.join(ROOT, "images", "06", "fig6-1-event-hook.png"))




def fig_6_2_save_flow():
    fig, ax = canvas(132, 82)

    box(ax, 24, 70, 84, 8, "内容：第一行 / 第二行", fc="white", ec=BLUE, size=6.0)
    box(ax, 24, 57, 84, 8, "钩子 1：在开头加一行注释", fc=GOLD_L, ec=GOLD, size=6.0)
    box(ax, 24, 44, 84, 8, "钩子 2：去掉多余空行", fc=GOLD_L, ec=GOLD, size=6.0)
    box(ax, 24, 31, 84, 8, "写文件（宿主自己完成）", fc="white", ec=BLUE, size=6.0)
    box(ax, 24, 19, 84, 8, "事件总线：发布 file.saved", fc=BLUE_L, ec=BLUE,
        size=6.0, weight="bold")

    box(ax, 6, 3, 50, 8, "订阅者 A：更新索引", fc=GREEN_L, ec=GREEN, size=6.0)
    box(ax, 76, 3, 50, 8, "订阅者 B：上传云端", fc=GREEN_L, ec=GREEN, size=6.0)

    for y1, y2 in [(70, 65), (57, 52), (44, 39), (31, 27)]:
        arrow(ax, (66, y1), (66, y2), color=GRAY, shrink=0.2)
    arrow(ax, (60, 19), (32, 11), color=GREEN, shrink=0.2)
    arrow(ax, (72, 19), (100, 11), color=GREEN, shrink=0.2)

    text(ax, 6, 62, "钩子改内容", size=5.6, color=GOLD, ha="left")
    text(ax, 6, 36, "内容确定后才写", size=5.6, color=GRAY, ha="left")
    text(ax, 6, 23, "事件只通知", size=5.6, color=BLUE, ha="left")

    save(fig, os.path.join(ROOT, "images", "06", "fig6-2-save-flow.png"))

if __name__ == "__main__":
    fig_6_1()
    fig_6_2_save_flow()
