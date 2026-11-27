# -*- coding: utf-8 -*-
"""第 16 章插图：怎么走交给迭代器，调用方只看到一个平坦的序列。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "common", "figstyle"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))
from figlib import render_roles  # noqa: E402

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))), "vol4-patterns")


def fig_16_1():
    body = """  cli [label="上传任务", fillcolor="#f1f3f5", color="#6b7280"];
  ag [label="目录
（聚合）", fillcolor="#f6efdd", color="#b08a2e"];
  it [label="目录迭代器
hasNext / next", fillcolor="#e8eef6", color="#1f3a5f"];
  nd [label="文件与子目录", fillcolor="#ffffff", color="#6b7280"];
  cli -> ag [label="iterator()"];
  ag -> it [label="创建"];
  it -> nd [label="逐个取出"];
  cli -> nd [label="看不到内部结构", style=dashed];
"""
    render_roles(body, os.path.join(ROOT, "images", "16", "fig16-1.png"))


if __name__ == "__main__":
    fig_16_1()
