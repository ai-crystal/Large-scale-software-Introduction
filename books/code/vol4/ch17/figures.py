# -*- coding: utf-8 -*-
"""第 17 章插图：控件之间不再互相调用，所有联动都经过中介者。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "common", "figstyle"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from figlib import render_roles  # noqa: E402

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))), "vol4-patterns")


def fig_17_1():
    body = """  c1 [label="日期控件", fillcolor="#ffffff", color="#6b7280"];
  c2 [label="金额控件", fillcolor="#ffffff", color="#6b7280"];
  c3 [label="状态下拉", fillcolor="#ffffff", color="#6b7280"];
  m [label="筛选面板\n（中介者）", fillcolor="#f6efdd", color="#b08a2e"];
  bt [label="查询按钮", fillcolor="#ffffff", color="#6b7280"];
  c1 -> m [label="变化通知"];
  c2 -> m [label="变化通知"];
  c3 -> m [label="变化通知"];
  m -> c2 [label="同步取值，静默设置", style=dashed];
  m -> bt [label="统一校验后启用"];
"""
    render_roles(body, os.path.join(ROOT, "images", "17", "fig17-1.png"))


if __name__ == "__main__":
    fig_17_1()
