# -*- coding: utf-8 -*-
"""第 3 章插图。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "common"))
from figstyle import render_dot, dot_graph

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def fig_3_1():
    body = """
  host [label="宿主程序"];
  open [label="LoadLibrary / dlopen\\n把路径交给系统"];
  os [label="操作系统\\n找到文件、装入内存"];
  table [label="读取导出表\\n有哪些函数、在哪里"];
  handle [label="返回一个把手\\n句柄"];
  sym [label="GetProcAddress / dlsym\\n按名字取地址"];
  call [label="存进函数指针\\n像普通函数一样调用", fillcolor="#e8f2ec", color="#2f6b4f"];

  host -> open -> os -> table -> handle -> sym -> call;
"""
    render_dot(dot_graph(body, rankdir="TB", nodesep=0.24, ranksep=0.24,
                         fontsize=8.8, node_width=2.7),
               os.path.join(ROOT, "images", "03", "fig3-1-load.png"))


if __name__ == "__main__":
    fig_3_1()
