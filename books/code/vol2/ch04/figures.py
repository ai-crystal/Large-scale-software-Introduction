# -*- coding: utf-8 -*-
"""第 4 章插图：版本范围求交，以及一次加载里的检查顺序。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "common", "figstyle"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))
from figlib import render_roles  # noqa: E402

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))), "vol2-architecture")


def fig_4_1():
    body = """  r [label="插件清单\\napi: >=2 <4", fillcolor="#e8eef6", color="#1f3a5f"];
  s [label="宿主支持\\n1、2、3", fillcolor="#f6efdd", color="#b08a2e"];
  i [label="求交集\\n得到 2、3"];
  pick [label="取最高可用\\n按 3 建接口表", fillcolor="#e8f2ec", color="#2f6b4f"];
  none [label="交集为空\\n拒绝并说明该升到哪版", fillcolor="#f7e9e7", color="#9b3b32"];
  r -> i [label="范围"];
  s -> i [label="集合"];
  i -> pick [label="非空"];
  i -> none [label="为空"];
"""
    render_roles(body, os.path.join(ROOT, "images", "04", "fig4-1.png"))


def fig_4_2():
    body = """  m [label="读清单"];
  v [label="范围求交"];
  h [label="加载动态库"];
  init [label="调用 plugin_init"];
  ok [label="可用", fillcolor="#e8f2ec", color="#2f6b4f"];
  f1 [label="缺字段", fillcolor="#f7e9e7", color="#9b3b32"];
  f2 [label="无交集\\n拒绝并提示", fillcolor="#f7e9e7", color="#9b3b32"];
  f3 [label="返回非零\\n回滚", fillcolor="#f7e9e7", color="#9b3b32"];
  m -> v [];
  v -> h [label="有交集"];
  h -> init [];
  init -> ok [label="返回 0"];
  m -> f1 [style=dashed];
  v -> f2 [style=dashed];
  init -> f3 [style=dashed];
"""
    render_roles(body, os.path.join(ROOT, "images", "04", "fig4-2.png"))


if __name__ == "__main__":
    fig_4_1()
    fig_4_2()
