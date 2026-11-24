# -*- coding: utf-8 -*-
"""第 7 章插图：报表种类和导出方式各自变化，互不牵连。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "common", "figstyle"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from figlib import render_roles  # noqa: E402

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))), "vol4-patterns")


def fig_07_1():
    body = """  ab [label="报表\n（抽象）", fillcolor="#f6efdd", color="#b08a2e"];
  ab2 [label="图表报表\n（细化）", fillcolor="#e8eef6", color="#1f3a5f"];
  im [label="导出方式\n（实现者）", fillcolor="#f6efdd", color="#b08a2e"];
  pdf [label="PDF 导出", fillcolor="#e8eef6", color="#1f3a5f"];
  xl [label="Excel 导出", fillcolor="#e8eef6", color="#1f3a5f"];
  ab2 -> ab [label="继承"];
  ab -> im [label="持有"];
  im -> pdf [];
  im -> xl [];
"""
    render_roles(body, os.path.join(ROOT, "images", "07", "fig7-1.png"))


if __name__ == "__main__":
    fig_07_1()
