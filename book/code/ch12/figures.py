# -*- coding: utf-8 -*-
"""第 12 章插图。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "common"))
from figstyle import render_dot, dot_graph

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def fig_12_1():
    body = """
  main [label="host/main.cpp\\n启动与命令循环", fillcolor="#f6efdd", color="#b08a2e"];
  loader [label="loader\\n扫描、检查、加载"];
  registry [label="registry\\n命令表"];
  events [label="events\\n订阅与发布"];
  api [label="sdk/plugin_api.h\\n契约"];
  p1 [label="hello 插件", fillcolor="#e8f2ec", color="#2f6b4f"];
  p2 [label="notes 插件", fillcolor="#e8f2ec", color="#2f6b4f"];

  main -> loader;
  main -> registry;
  main -> events;
  loader -> p1; loader -> p2;
  api -> loader [style=dashed, label="被引用"];
  p1 -> registry [label="注册命令", style=dashed];
  p1 -> events [label="订阅", style=dashed];
  p2 -> registry [style=dashed];

"""
    render_dot(dot_graph(body, rankdir="TB", nodesep=0.45, ranksep=0.36,
                         fontsize=8.8, node_width=1.85),
               os.path.join(ROOT, "images", "12", "fig12-1-modules.png"))


if __name__ == "__main__":
    fig_12_1()
