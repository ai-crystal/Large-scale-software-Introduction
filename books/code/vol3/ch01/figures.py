# -*- coding: utf-8 -*-
"""第 1 章插图：模板里的每一部分最终被谁消费。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "common", "figstyle"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))
from figlib import render_roles  # noqa: E402

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))), "vol3-engineering")


def fig_1_1():
    body = """  tpl [label="组件模板", fillcolor="#f6efdd", color="#b08a2e"];
  mani [label="清单", fillcolor="#e8eef6", color="#1f3a5f"];
  entry [label="入口", fillcolor="#e8eef6", color="#1f3a5f"];
  ci [label="构建与 CI", fillcolor="#e8eef6", color="#1f3a5f"];
  doc [label="示例与文档", fillcolor="#e8eef6", color="#1f3a5f"];
  loader [label="加载器与审核", fillcolor="#e8f2ec", color="#2f6b4f"];
  pipe [label="流水线", fillcolor="#e8f2ec", color="#2f6b4f"];
  author [label="作者", fillcolor="#e8f2ec", color="#2f6b4f"];
  tpl -> mani [];
  tpl -> entry [];
  tpl -> ci [];
  tpl -> doc [];
  mani -> loader [];
  entry -> loader [];
  ci -> pipe [];
  doc -> author [];
"""
    render_roles(body, os.path.join(ROOT, "images", "01", "fig1-1.png"), fontsize=7.2)


if __name__ == "__main__":
    fig_1_1()
