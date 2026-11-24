# -*- coding: utf-8 -*-
"""第 1 章插图：两个模块取到的是同一份配置，创建只发生一次。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "common", "figstyle"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from figlib import render_roles  # noqa: E402

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))), "vol4-patterns")


def fig_01_1():
    body = """  a [label="业务模块 A", fillcolor="#f1f3f5", color="#6b7280"];
  b [label="业务模块 B", fillcolor="#f1f3f5", color="#6b7280"];
  g [label="获取配置\ngetInstance()", fillcolor="#f6efdd", color="#b08a2e"];
  s [label="唯一实例\n配置对象", fillcolor="#e8eef6", color="#1f3a5f"];
  a -> g [label="请求"];
  b -> g [];
  g -> s [label="首次创建"];
  s -> g [label="之后直接返回", style=dashed];
"""
    render_roles(body, os.path.join(ROOT, "images", "01", "fig1-1.png"))


if __name__ == "__main__":
    fig_01_1()
