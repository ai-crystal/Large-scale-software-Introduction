# -*- coding: utf-8 -*-
"""第 14 章插图：操作变成对象之后，排队、记录、撤销都成了普通操作。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "common", "figstyle"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from figlib import render_roles  # noqa: E402

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))), "vol4-patterns")


def fig_14_1():
    body = """  ui [label="按钮与快捷键", fillcolor="#f1f3f5", color="#6b7280"];
  cm [label="命令接口\nexecute / undo", fillcolor="#f6efdd", color="#b08a2e"];
  c1 [label="加粗命令", fillcolor="#e8eef6", color="#1f3a5f"];
  c2 [label="插入命令", fillcolor="#e8eef6", color="#1f3a5f"];
  rv [label="文档\n（接收者）", fillcolor="#ffffff", color="#6b7280"];
  hi [label="历史栈", fillcolor="#ffffff", color="#6b7280"];
  ui -> cm [label="构造命令"];
  cm -> c1 [style=dashed];
  cm -> c2 [style=dashed];
  c1 -> rv [label="执行 / 撤销"];
  c2 -> rv [label="执行 / 撤销"];
  hi -> cm [label="弹出后调用 undo"];
  ui -> hi [label="执行后压栈"];
"""
    render_roles(body, os.path.join(ROOT, "images", "14", "fig14-1.png"))


if __name__ == "__main__":
    fig_14_1()
