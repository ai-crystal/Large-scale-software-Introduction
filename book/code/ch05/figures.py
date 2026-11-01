# -*- coding: utf-8 -*-
"""第 5 章插图。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "common"))
from figstyle import canvas, box, text, arrow, save, BLUE, BLUE_L, GOLD, GOLD_L, GRAY, GRAY_L, INK, GREEN, GREEN_L

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def fig_5_1():
    fig, ax = canvas(132, 66)

    box(ax, 4, 40, 26, 12, "hello 插件", fc=GREEN_L, ec=GREEN, size=6.8)
    box(ax, 4, 16, 26, 12, "notes 插件", fc=GREEN_L, ec=GREEN, size=6.8)

    box(ax, 44, 4, 52, 56, "", fc="white", ec=BLUE, lw=1.0)
    text(ax, 48, 55, "命令表", size=7.2, weight="bold", color=BLUE, ha="left")

    rows = [
        ("hello", "owner = hello", 40, BLUE_L),
        ("note", "owner = notes", 26, BLUE_L),
        ("help", "owner = core", 12, GRAY_L),
    ]
    for name, owner, y, fill in rows:
        box(ax, 48, y, 20, 9, name, fc=fill, ec=GRAY, size=5.8)
        text(ax, 72, y + 4.5, owner, size=5.4, color=GRAY, ha="left")

    box(ax, 106, 26, 22, 12, "执行命令", fc=GOLD_L, ec=GOLD, size=6.6)
    arrow(ax, (30, 46), (44, 44), color=GREEN, shrink=0.2)
    arrow(ax, (30, 22), (44, 30), color=GREEN, shrink=0.2)
    arrow(ax, (96, 32), (106, 32), color=GOLD, shrink=0.2)

    text(ax, 66, 1.6, "每条记录都带 owner，卸载时按 owner 一次清干净", size=5.8, color=GRAY)
    save(fig, os.path.join(ROOT, "images", "05", "fig5-1-registry.png"))




def fig_5_2_pipeline():
    fig, ax = canvas(132, 48)

    xs = [4, 30, 56, 82, 108]
    labels = [
        "原始文本\n**你好**",
        "插件 A\n转义 HTML",
        "插件 B\n处理粗体",
        "插件 C\n处理链接",
        "最终 HTML\n粗体已生成",
    ]
    for x, label in zip(xs, labels):
        box(ax, x, 22, 20, 14, label, fc="white", ec=BLUE, size=5.4, wrap=8)

    for i in range(4):
        arrow(ax, (xs[i] + 20, 29), (xs[i + 1], 29), color=GOLD, shrink=0.2)

    text(ax, 66, 14, "每一步的输出就是下一步的输入，顺序不能乱", size=6.0, color=GRAY)
    text(ax, 66, 7, "先加粗再转义，生成的标签会被当成普通文字显示出来", size=6.0, color=GRAY)

    save(fig, os.path.join(ROOT, "images", "05", "fig5-2-pipeline.png"))



def fig_5_3_lifecycle():
    fig, ax = canvas(132, 78)

    steps = [
        ("宿主建一张空表", "宿主"),
        ("加载插件，把 PluginApi 递过去", "宿主"),
        ("插件注册命令，宿主填上 owner", "插件 → 宿主"),
        ("用户输入 hello 世界", "用户"),
        ("按名字查表，找到 Command", "宿主"),
        ("调用 run 函数指针", "宿主"),
        ("退出时按 owner 清理", "宿主"),
    ]

    y = 67
    for index, (label, who) in enumerate(steps, 1):
        box(ax, 8, y, 78, 7.5, f"{index}  {label}", fc="white", ec=BLUE, size=6.2)
        text(ax, 92, y + 3.75, who, size=5.6, color=GRAY, ha="left")
        if index < len(steps):
            arrow(ax, (47, y), (47, y - 2.5), color=GRAY, shrink=0.2)
        y -= 9.5

    save(fig, os.path.join(ROOT, "images", "05", "fig5-3-lifecycle.png"))

if __name__ == "__main__":
    fig_5_1()
    fig_5_2_pipeline()
    fig_5_3_lifecycle()
