# -*- coding: utf-8 -*-
"""第 4 章插图：装配顺序在指挥者手里，每一步怎么做在建造者手里。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "common", "figstyle"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))
from figlib import render_roles  # noqa: E402

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))), "vol4-patterns")


def fig_04_1():
    body = """  cli [label="调用方", fillcolor="#f1f3f5", color="#6b7280"];
  d [label="指挥者\n固定装配顺序", fillcolor="#f6efdd", color="#b08a2e"];
  b [label="建造者接口\nset_xxx()", fillcolor="#f6efdd", color="#b08a2e"];
  cb [label="请求建造者", fillcolor="#e8eef6", color="#1f3a5f"];
  pr [label="请求对象", fillcolor="#ffffff", color="#6b7280"];
  cli -> d [label="发起"];
  d -> b [label="按步骤调用"];
  b -> cb [label="实现", style=dashed];
  cb -> pr [label="分步装配"];
  pr -> cli [label="交给调用方", style=dashed];
"""
    render_roles(body, os.path.join(ROOT, "images", "04", "fig4-1.png"))


if __name__ == "__main__":
    fig_04_1()
