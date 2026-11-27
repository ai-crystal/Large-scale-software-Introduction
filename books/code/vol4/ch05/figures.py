# -*- coding: utf-8 -*-
"""第 5 章插图：复制比重新构造快，原型自己知道该复制哪些字段。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "common", "figstyle"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))
from figlib import render_roles  # noqa: E402

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))), "vol4-patterns")


def fig_05_1():
    body = """  cli [label="图形编辑器", fillcolor="#f1f3f5", color="#6b7280"];
  pr [label="原型接口\nclone()", fillcolor="#f6efdd", color="#b08a2e"];
  im [label="图层原型\n已配好样式", fillcolor="#e8eef6", color="#1f3a5f"];
  nw [label="新图层", fillcolor="#ffffff", color="#6b7280"];
  cli -> pr [label="复制当前选中"];
  pr -> im [label="实现", style=dashed];
  im -> nw [label="克隆"];
  nw -> cli [label="微调后使用", style=dashed];
"""
    render_roles(body, os.path.join(ROOT, "images", "05", "fig5-1.png"))


def fig_05_2():
    body = """  a [label="原图层 A", fillcolor="#f1f3f5", color="#6b7280"];
  b [label="副本 A′", fillcolor="#f1f3f5", color="#6b7280"];
  ma [label="蒙版", fillcolor="#e8eef6", color="#1f3a5f"];
  mb [label="蒙版", fillcolor="#e8eef6", color="#1f3a5f"];
  sa [label="样式", fillcolor="#e8eef6", color="#1f3a5f"];
  sb [label="样式", fillcolor="#e8eef6", color="#1f3a5f"];
  im [label="图片资源\n只读", fillcolor="#f6efdd", color="#b08a2e"];
  a -> ma [label="深拷"];
  b -> mb [label="新对象"];
  a -> sa [label="深拷"];
  b -> sb [label="新对象"];
  a -> im [label="共享"];
  b -> im [label="共享", style=dashed];
"""
    render_roles(body, os.path.join(ROOT, "images", "05", "fig5-2.png"))


if __name__ == "__main__":
    fig_05_1()
    fig_05_2()
