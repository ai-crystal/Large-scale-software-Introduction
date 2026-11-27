# -*- coding: utf-8 -*-
"""第 2 章插图：选哪一个由子类决定，调用方只面对文档接口。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "common", "figstyle"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))
from figlib import render_roles  # noqa: E402

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))), "vol4-patterns")


def fig_02_1():
    body = """  cli [label="调用方\n打开文件", fillcolor="#f1f3f5", color="#6b7280"];
  cr [label="创建者\n（抽象）", fillcolor="#f6efdd", color="#b08a2e"];
  c1 [label="Markdown 工厂", fillcolor="#e8eef6", color="#1f3a5f"];
  c2 [label="Excel 工厂", fillcolor="#e8eef6", color="#1f3a5f"];
  pr [label="文档接口", fillcolor="#f6efdd", color="#b08a2e"];
  p1 [label="Markdown 文档", fillcolor="#e8eef6", color="#1f3a5f"];
  p2 [label="Excel 文档", fillcolor="#e8eef6", color="#1f3a5f"];
  cli -> cr [label="只要打开，不管类型"];
  cr -> c1 [];
  cr -> c2 [];
  c1 -> p1 [label="创建"];
  c2 -> p2 [label="创建"];
  p1 -> pr [label="实现", style=dashed];
  p2 -> pr [label="实现", style=dashed];
"""
    render_roles(body, os.path.join(ROOT, "images", "02", "fig2-1.png"))


def fig_02_2():
    body = """  en [label="五个入口", fillcolor="#f1f3f5", color="#6b7280"];
  rg [label="注册表", fillcolor="#f6efdd", color="#b08a2e"];
  f1 [label="Markdown 工厂", fillcolor="#e8eef6", color="#1f3a5f"];
  f2 [label="Epub 工厂", fillcolor="#e8eef6", color="#1f3a5f"];
  pi [label="文档接口", fillcolor="#f6efdd", color="#b08a2e"];
  en -> rg [label="扩展名"];
  rg -> f1 [label="md"];
  rg -> f2 [label="epub"];
  f1 -> pi [label="创建解析器", style=dashed];
  f2 -> pi [style=dashed];
"""
    render_roles(body, os.path.join(ROOT, "images", "02", "fig2-2.png"))


if __name__ == "__main__":
    fig_02_1()
    fig_02_2()
