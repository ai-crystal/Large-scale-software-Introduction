# -*- coding: utf-8 -*-
"""第 10 章插图：流水线的四段结构，同一份包在环境之间晋级。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "common", "figstyle"))
from figstyle import canvas, box, text, arrow, save, INK, BLUE, BLUE_L, GOLD, GOLD_L, GRAY, GRAY_L, RED, RED_L, GREEN, GREEN_L

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))), "vol3-engineering")


def fig_10_1():
    fig, ax = canvas(132, 58)

    groups = [
        (2, "造出代码", [
            ("生成", "骨架目录"),
            ("开发", "提交"),
            ("测试", "报告"),
        ], BLUE_L, BLUE),
        (36, "做成分发件", [
            ("构建", "动态库"),
            ("打包", "zip + 清单"),
            ("签名", "包 + 签名"),
        ], GOLD_L, GOLD),
        (70, "放给用户", [
            ("上传", "草稿条目"),
            ("审核", "上架许可"),
            ("分发", "用户装上"),
        ], BLUE_L, BLUE),
        (104, "持续看着", [
            ("更新", "升级记录"),
            ("监控", "一次判断"),
            ("回滚", "退回上一版"),
        ], GREEN_L, GREEN),
    ]

    for x, title, items, fc, ec in groups:
        box(ax, x, 8, 28, 44, "", fc="white", ec=GRAY, lw=0.8)
        text(ax, x + 14, 48.5, title, size=6.2, weight="bold", color=ec)
        y = 36
        for name, artifact in items:
            if not name:
                break
            box(ax, x + 2, y, 24, 9, f"{name}\n{artifact}", fc=fc, ec=ec, size=5.0)
            y -= 11

    for x in (30, 64, 98):
        arrow(ax, (x, 30), (x + 6, 30), color=GRAY, shrink=0.2)

    text(ax, 66, 2.5, "每个小方框下面那行是这一步留下的东西，后面所有环节只认这一份",
         size=5.6, color=GRAY)

    save(fig, os.path.join(ROOT, "images", "10", "fig10-1.png"))


def fig_10_2():
    fig, ax = canvas(132, 46)

    box(ax, 3, 18, 28, 14, "CI 构建\n唯一一份包", fc=GOLD_L, ec=GOLD, size=5.6)
    box(ax, 40, 18, 24, 14, "测试环境", fc=BLUE_L, ec=BLUE, size=5.8)
    box(ax, 73, 18, 24, 14, "预发布", fc=BLUE_L, ec=BLUE, size=5.8)
    box(ax, 106, 18, 24, 14, "生产与灰度", fc=GREEN_L, ec=GREEN, size=5.6)

    arrow(ax, (31, 25), (40, 25), color=GRAY, shrink=0.2)
    arrow(ax, (64, 25), (73, 25), color=GRAY, shrink=0.2)
    arrow(ax, (97, 25), (106, 25), color=GRAY, shrink=0.2)

    text(ax, 35.5, 14, "签名可信", size=4.8, color=GRAY)
    text(ax, 68.5, 14, "测试通过", size=4.8, color=GRAY)
    text(ax, 101.5, 14, "哈希一致", size=4.8, color=GRAY)

    text(ax, 66, 5, "晋级只改“这份包在哪生效”，不改包本身，中途重新构建就等于前面白验",
         size=5.6, color=GRAY)

    save(fig, os.path.join(ROOT, "images", "10", "fig10-2.png"))


if __name__ == "__main__":
    fig_10_1()
    fig_10_2()
