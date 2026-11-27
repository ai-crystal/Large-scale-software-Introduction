# -*- coding: utf-8 -*-
"""第 11 章插图：弃用的时间轴，停止维护的收尾顺序。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "common", "figstyle"))
from figstyle import canvas, box, text, arrow, line, save, INK, BLUE, BLUE_L, GOLD, GOLD_L, GRAY, GRAY_L, RED, RED_L, GREEN, GREEN_L

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))), "vol3-engineering")


def fig_11_1():
    fig, ax = canvas(132, 54)

    phases = [
        (4, "决定与记录", "写下原因与替代", BLUE_L, BLUE),
        (30, "公告", "四个渠道都发一遍", BLUE_L, BLUE),
        (56, "双轨", "旧接口转发新接口", GOLD_L, GOLD),
        (82, "警告", "限频警告带链接", GOLD_L, GOLD),
        (108, "最后通牒", "日期跟着版本走", RED_L, RED),
    ]
    for x, name, note, fc, ec in phases:
        box(ax, x, 30, 22, 11, name, fc=fc, ec=ec, size=5.6)

    arrow(ax, (26, 35.5), (30, 35.5), color=GRAY, shrink=0.2)
    arrow(ax, (52, 35.5), (56, 35.5), color=GRAY, shrink=0.2)
    arrow(ax, (78, 35.5), (82, 35.5), color=GRAY, shrink=0.2)
    arrow(ax, (104, 35.5), (108, 35.5), color=GRAY, shrink=0.2)

    line(ax, 6, 24, 128, 24, color=GRAY, lw=0.9)

    for x, name, note, fc, ec in phases:
        text(ax, x + 11, 18, note, size=5.0, color=GRAY)

    text(ax, 66, 8, "每一步都在回答同一个问题，还有谁在用旧接口，他知不知道要改",
         size=5.8, color=GRAY)

    save(fig, os.path.join(ROOT, "images", "11", "fig11-1.png"))


def fig_11_2():
    fig, ax = canvas(132, 54)

    top = [
        (4, "1  发最后一个版本"),
        (36, "2  文档顶部加横幅"),
        (68, "3  标注不再维护"),
        (100, "4  关闭新问题入口"),
    ]
    bottom = [
        (100, "5  保留下载地址"),
        (68, "6  归档签名密钥"),
        (36, "7  给出迁移路径"),
    ]

    for x, label in top:
        box(ax, x, 32, 28, 12, label, fc=BLUE_L, ec=BLUE, size=5.2)
    for x, label in bottom:
        box(ax, x, 10, 28, 12, label, fc=GREEN_L, ec=GREEN, size=5.2)

    for x in (32, 64, 96):
        arrow(ax, (x, 38), (x + 4, 38), color=GRAY, shrink=0.2)
    arrow(ax, (114, 32), (114, 22), color=GRAY, shrink=0.2)
    for x in (100, 68):
        arrow(ax, (x, 16), (x - 4, 16), color=GRAY, shrink=0.2)

    text(ax, 66, 3.5, "先留下可用的最后一版，再收口，顺序反了用户就没东西可装",
         size=5.6, color=GRAY)

    save(fig, os.path.join(ROOT, "images", "11", "fig11-2.png"))


if __name__ == "__main__":
    fig_11_1()
    fig_11_2()
