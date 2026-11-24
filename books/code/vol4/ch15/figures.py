# -*- coding: utf-8 -*-
"""第 15 章插图：一条规则是一棵树，求值就是一次深度优先遍历。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "common", "figstyle"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from figlib import render_roles  # noqa: E402

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))), "vol4-patterns")


def fig_15_1():
    body = """  ctx [label="订单上下文", fillcolor="#f1f3f5", color="#6b7280"];
  root [label="And", fillcolor="#f6efdd", color="#b08a2e"];
  cm [label="Compare\n会员等级 >= 3", fillcolor="#e8eef6", color="#1f3a5f"];
  or [label="Or", fillcolor="#e8eef6", color="#1f3a5f"];
  a1 [label="Compare\n金额 >= 200", fillcolor="#e8eef6", color="#1f3a5f"];
  a2 [label="Compare\n品类 = 生鲜", fillcolor="#e8eef6", color="#1f3a5f"];
  v [label="变量与常量", fillcolor="#ffffff", color="#6b7280"];
  ctx -> root [label="求值时传入"];
  root -> cm [label="先算左"];
  root -> or [label="再算右"];
  or -> a1 [];
  or -> a2 [];
  cm -> v [style=dashed];
  a1 -> v [style=dashed];
"""
    render_roles(body, os.path.join(ROOT, "images", "15", "fig15-1.png"))


if __name__ == "__main__":
    fig_15_1()
