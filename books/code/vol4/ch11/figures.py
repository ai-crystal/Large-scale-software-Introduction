# -*- coding: utf-8 -*-
"""第 11 章插图：不变的共享，逐字符变化的部分放在外面。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "common", "figstyle"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))
from figlib import render_roles  # noqa: E402

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))), "vol4-patterns")


def fig_11_1():
    body = """  cli [label="排版渲染", fillcolor="#f1f3f5", color="#6b7280"];
  fa [label="字形工厂\n按 key 取", fillcolor="#f6efdd", color="#b08a2e"];
  po [label="共享字形池\n字符 + 字体 + 字号", fillcolor="#e8eef6", color="#1f3a5f"];
  ex [label="外部状态\n位置、颜色", fillcolor="#ffffff", color="#6b7280"];
  cli -> fa [label="取字形"];
  fa -> po [label="命中则复用"];
  po -> fa [label="同一份对象", style=dashed];
  cli -> ex [label="另存", style=dashed];
"""
    render_roles(body, os.path.join(ROOT, "images", "11", "fig11-1.png"))


def fig_11_2():
    body = """  cli [label="客户端
Glyph 集合", fillcolor="#f1f3f5", color="#6b7280"];
  fac [label="享元工厂
get(key)", fillcolor="#f6efdd", color="#b08a2e"];
  hit [label="命中
复用同一对象", fillcolor="#e8eef6", color="#1f3a5f"];
  miss [label="未命中
创建并入池", fillcolor="#e8eef6", color="#1f3a5f"];
  sty [label="共享样式
只读，无 setter", fillcolor="#e8eef6", color="#1f3a5f"];
  cli -> fac [label="要一个样式"];
  fac -> hit [label="池里有活引用"];
  fac -> miss [label="池里没有"];
  hit -> sty [];
  miss -> sty [label="新建"];
"""
    render_roles(body, os.path.join(ROOT, "images", "11", "fig11-2.png"))


if __name__ == "__main__":
    fig_11_1()
    fig_11_2()
