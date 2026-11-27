# -*- coding: utf-8 -*-
"""第 10 章插图：冷启动的四段。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "common", "figstyle"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))
from figlib import render_roles  # noqa: E402

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))), "vol2-architecture")


def fig_10_1():
    body = """  a [label="进程创建\\n几十毫秒", fillcolor="#e8eef6", color="#1f3a5f"];
  b [label="动态库加载\\n符号解析", fillcolor="#f6efdd", color="#b08a2e"];
  c [label="插件初始化\\n每个几毫秒", fillcolor="#f6efdd", color="#b08a2e"];
  d [label="首帧渲染\\n界面可见", fillcolor="#e8f2ec", color="#2f6b4f"];
  a -> b;
  b -> c;
  c -> d [label="可操作"];
"""
    render_roles(body, os.path.join(ROOT, "images", "10", "fig10-1-boot.png"))


if __name__ == "__main__":
    fig_10_1()
