# -*- coding: utf-8 -*-
"""第 3 章插图：同一族的产品一起出现，换平台就是整族一起换。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "common", "figstyle"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))
from figlib import render_roles  # noqa: E402

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))), "vol4-patterns")


def fig_03_1():
    body = """  cli [label="客户端
只声明要哪种风格", fillcolor="#f1f3f5", color="#6b7280"];
  f [label="界面工厂
（抽象）", fillcolor="#f6efdd", color="#b08a2e"];
  w [label="Windows 工厂", fillcolor="#e8eef6", color="#1f3a5f"];
  m [label="macOS 工厂", fillcolor="#e8eef6", color="#1f3a5f"];
  b [label="按钮", fillcolor="#ffffff", color="#6b7280"];
  mn [label="菜单", fillcolor="#ffffff", color="#6b7280"];
  cli -> f [];
  f -> w [];
  f -> m [];
  w -> b [label="创建"];
  w -> mn [];
  m -> b [style=dashed];
  m -> mn [label="创建", style=dashed];
"""
    render_roles(body, os.path.join(ROOT, "images", "03", "fig3-1.png"))


if __name__ == "__main__":
    fig_03_1()
