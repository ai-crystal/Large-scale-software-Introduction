# -*- coding: utf-8 -*-
"""第 8 章插图：更新的步骤与失败退路，三个通道的晋级关系。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "common", "figstyle"))
from figstyle import canvas, box, text, arrow, save, INK, BLUE, BLUE_L, GOLD, GOLD_L, GRAY, GRAY_L, RED, RED_L, GREEN, GREEN_L

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))), "vol3-engineering")


def fig_8_1():
    fig, ax = canvas(132, 100)

    steps = [
        ("读本地清单，拿到 v1 与宿主版本", "只需要本地文件"),
        ("请求更新元数据（带签名）", "取不到就下次再说"),
        ("比较版本", "v2 不高于 v1 就结束"),
        ("下载到 .part，可续传", "中断就留着，下次续传"),
        ("验签，整包", "不通过就删包，v1 继续用"),
        ("解压到 .staging/v2", "失败就删暂存目录"),
        ("逐文件核对哈希", "不一致就删暂存目录"),
        ("写 current.txt", "失败就保持原指针"),
        ("通知插件重载", "加载失败就指回 v1"),
        ("清理旧版本目录", "至少留一个上一个版本"),
    ]

    y = 90
    for index, (label, note) in enumerate(steps, 1):
        fill, edge = (GOLD_L, GOLD) if index in (5, 8, 9) else ("white", BLUE)
        box(ax, 6, y, 62, 7.2, f"{index}  {label}", fc=fill, ec=edge, size=6.0)
        text(ax, 72, y + 3.6, note, size=5.4, color=GRAY, ha="left")
        if index < len(steps):
            arrow(ax, (37, y), (37, y - 1.9), color=GRAY, shrink=0.2)
        y -= 8.9

    save(fig, os.path.join(ROOT, "images", "08", "fig8-1.png"))


def fig_8_2():
    fig, ax = canvas(132, 68)

    channels = [
        (4, "内测", "作者与固定测试组", "一天到一周", BLUE_L, BLUE),
        (48, "尝鲜", "用户主动打开开关", "三天", GOLD_L, GOLD),
        (92, "稳定", "全体用户，按桶放量", "半天一档", GREEN_L, GREEN),
    ]
    for x, name, who, window, fc, ec in channels:
        box(ax, x, 30, 36, 18, f"{name}\n{who}", fc=fc, ec=ec, size=5.8)
        text(ax, x + 18, 52.5, window, size=5.2, color=GRAY)

    arrow(ax, (40, 39), (48, 39), color=GRAY, shrink=0.2)
    arrow(ax, (84, 39), (92, 39), color=GRAY, shrink=0.2)
    text(ax, 44, 44, "晋级", size=5.0, color=GRAY)
    text(ax, 88, 44, "晋级", size=5.0, color=GRAY)

    arrow(ax, (110, 30), (22, 30), color=RED, ls="dashed", rad=-0.22, shrink=0.2)
    text(ax, 66, 6, "出问题就退回上一档，别跨档往回跳", size=5.6, color=RED)

    save(fig, os.path.join(ROOT, "images", "08", "fig8-2.png"))


if __name__ == "__main__":
    fig_8_1()
    fig_8_2()
