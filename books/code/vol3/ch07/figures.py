# -*- coding: utf-8 -*-
"""第 7 章插图：签名与验签两侧的步骤，密钥轮换的四段顺序。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "common", "figstyle"))
from figstyle import canvas, box, text, arrow, save, INK, BLUE, BLUE_L, GOLD, GOLD_L, GRAY, RED, RED_L, GREEN, GREEN_L

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))), "vol3-engineering")


def fig_7_1():
    fig, ax = canvas(132, 80)

    text(ax, 18, 75, "作者这一侧", size=6.0, color=GRAY)
    row1 = [
        (4, "按路径排序\n逐文件算 SHA-256", BLUE_L, BLUE),
        (34, "拼成总哈希\n路径 + 大小 + 哈希", BLUE_L, BLUE),
        (64, "私钥签名", GOLD_L, GOLD),
        (94, "打包装箱", BLUE_L, BLUE),
    ]
    for x, label, fc, ec in row1:
        box(ax, x, 56, 26, 15, label, fc=fc, ec=ec, size=5.8)
    for x in (30, 60, 90):
        arrow(ax, (x, 63.5), (x + 4, 63.5), color=GRAY, shrink=0.2)

    text(ax, 18, 33, "用户这一侧", size=6.0, color=GRAY)
    row2 = [
        (94, "按同样顺序\n重算总哈希", BLUE_L, BLUE),
        (64, "内置公钥验签", GOLD_L, GOLD),
        (34, "逐文件核对哈希", BLUE_L, BLUE),
        (4, "拒绝加载", RED_L, RED),
    ]
    for x, label, fc, ec in row2:
        box(ax, x, 14, 26, 15, label, fc=fc, ec=ec, size=5.8)
    for x in (94, 64, 34):
        arrow(ax, (x, 21.5), (x - 4, 21.5), color=GRAY, shrink=0.2)

    arrow(ax, (107, 56), (107, 29), color=GOLD, shrink=0.2)
    text(ax, 109, 42, "下载", size=5.6, color=GRAY, ha="left")

    text(ax, 66, 5.5, "验不过就停在这里，后面的解压和 JSON 解析一步都不走", size=5.8, color=GRAY)

    save(fig, os.path.join(ROOT, "images", "07", "fig7-1.png"))


def fig_7_2():
    fig, ax = canvas(132, 60)

    phases = [
        ("准备", "宿主先内置 A、B\n发布方仍用 A 签", BLUE_L, BLUE),
        ("过渡", "每个包带两个签名\n任何宿主都装得上", GOLD_L, GOLD),
        ("切换", "只用 B 签\n宿主还留着 A", BLUE_L, BLUE),
        ("收尾", "宿主删掉 A\n老包一律拒绝", GREEN_L, GREEN),
    ]
    xs = [3, 36, 69, 102]
    for x, (name, label, fc, ec) in zip(xs, phases):
        box(ax, x, 24, 27, 22, label, fc=fc, ec=ec, size=5.6)
        text(ax, x + 13.5, 50, name, size=6.4, weight="bold", color=INK)

    for x in (30, 63, 96):
        arrow(ax, (x, 35), (x + 6, 35), color=GRAY, shrink=0.2)

    text(ax, 33, 18, "先发布新版宿主", size=5.2, color=GRAY)
    text(ax, 66, 18, "旧宿主占比降到一成", size=5.2, color=GRAY)
    text(ax, 99, 18, "确认还有谁只认 A", size=5.2, color=GRAY)

    text(ax, 66, 8, "顺序反过来，就是新包在老宿主上验不过，用户只看到一句验证失败", size=5.8, color=GRAY)

    save(fig, os.path.join(ROOT, "images", "07", "fig7-2.png"))


if __name__ == "__main__":
    fig_7_1()
    fig_7_2()
