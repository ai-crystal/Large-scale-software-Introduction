# -*- coding: utf-8 -*-
"""第 11 章插图。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "common"))
from figstyle import render_dot, dot_graph

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def fig_11_1():
    body = """
  closed [label="闭合\\n正常放行", fillcolor="#e8f2ec", color="#2f6b4f"];
  open [label="打开\\n直接拒绝", fillcolor="#f7e9e7", color="#9b3b32"];
  half [label="半开\\n允许一次试探", fillcolor="#f6efdd", color="#b08a2e"];

  closed -> open [label="失败达到阈值"];
  open -> half [dir=both, label="冷却结束 / 试探失败"];
  half -> closed [label="试探成功"];
  closed -> closed [label="失败计数", style=dashed];
"""
    render_dot(dot_graph(body, rankdir="LR", nodesep=0.35, ranksep=0.6, fontsize=8.6),
               os.path.join(ROOT, "images", "11", "fig11-1-breaker.png"))


if __name__ == "__main__":
    fig_11_1()
