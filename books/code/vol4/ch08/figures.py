# -*- coding: utf-8 -*-
"""第 8 章插图：文件夹和文件实现同一个接口，调用方不必分辨。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "common", "figstyle"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))
from figlib import render_roles  # noqa: E402

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))), "vol4-patterns")


def fig_08_1():
    body = """  cli [label="文件管理器", fillcolor="#f1f3f5", color="#6b7280"];
  cp [label="节点接口
size()", fillcolor="#f6efdd", color="#b08a2e"];
  fl [label="文件", fillcolor="#e8eef6", color="#1f3a5f"];
  fd [label="文件夹
子节点列表", fillcolor="#e8eef6", color="#1f3a5f"];
  cli -> cp [label="一视同仁"];
  fl -> cp [label="实现", style=dashed];
  fd -> cp [style=dashed];
  fd -> fl [label="包含"];
  cli -> fd [label="求和时递归"];
"""
    render_roles(body, os.path.join(ROOT, "images", "08", "fig8-1.png"))


def fig_08_2():
    body = """  r [label="根节点", fillcolor="#f1f3f5", color="#6b7280"];
  a [label="组 A", fillcolor="#e8eef6", color="#1f3a5f"];
  b [label="组 B", fillcolor="#e8eef6", color="#1f3a5f"];
  s [label="共享子树", fillcolor="#f6efdd", color="#b08a2e"];
  p [label="父指针\n只指向最后挂上的那个", fillcolor="#f1f3f5", color="#6b7280"];
  r -> a [label="包含"];
  r -> b [label="包含"];
  a -> s [label="先挂"];
  b -> s [label="后挂", style=dashed];
  s -> p [label="parent", style=dashed];
"""
    render_roles(body, os.path.join(ROOT, "images", "08", "fig8-2.png"))


if __name__ == "__main__":
    fig_08_1()
    fig_08_2()
