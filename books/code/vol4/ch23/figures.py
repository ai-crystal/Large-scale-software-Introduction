# -*- coding: utf-8 -*-
"""第 23 章插图：节点只报告自己的类型，动作由访问者决定。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "common", "figstyle"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))
from figlib import render_roles  # noqa: E402

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))), "vol4-patterns")


def fig_23_1():
    body = """  tr [label="语法树\n（对象结构）", fillcolor="#f1f3f5", color="#6b7280"];
  nd [label="节点\naccept(visitor)", fillcolor="#f6efdd", color="#b08a2e"];
  vi [label="访问者\nvisit_xxx(node)", fillcolor="#f6efdd", color="#b08a2e"];
  ch [label="检查器", fillcolor="#e8eef6", color="#1f3a5f"];
  fm [label="格式化器", fillcolor="#e8eef6", color="#1f3a5f"];
  tr -> nd [label="遍历"];
  nd -> vi [label="accept 把自己传进去"];
  vi -> ch [style=dashed];
  vi -> fm [style=dashed];
  ch -> nd [label="递归访问子节点", style=dashed];
"""
    render_roles(body, os.path.join(ROOT, "images", "23", "fig23-1.png"))


if __name__ == "__main__":
    fig_23_1()
