# -*- coding: utf-8 -*-
"""第 6 章插图：把三条会飘的输入钉死，才得到字节相同的动态库。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "common", "figstyle"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))
from figlib import render_roles  # noqa: E402

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))), "vol3-engineering")


def fig_6_1():
    body = """  src [label="源码与构建目录", fillcolor="#f1f3f5", color="#6b7280"];
  t [label="时间\\nSOURCE_DATE_EPOCH", fillcolor="#e8eef6", color="#1f3a5f"];
  p [label="路径\\n-ffile-prefix-map", fillcolor="#e8eef6", color="#1f3a5f"];
  o [label="顺序与种子\\n排序、-frandom-seed", fillcolor="#e8eef6", color="#1f3a5f"];
  so [label="字节相同的动态库", fillcolor="#e8f2ec", color="#2f6b4f"];
  src -> t [];
  src -> p [];
  src -> o [];
  t -> so [];
  p -> so [];
  o -> so [];
"""
    render_roles(body, os.path.join(ROOT, "images", "06", "fig6-1.png"), fontsize=7.6)


if __name__ == "__main__":
    fig_6_1()
