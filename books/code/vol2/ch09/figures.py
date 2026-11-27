# -*- coding: utf-8 -*-
"""第 9 章插图：把结构装回去。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "common", "figstyle"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))
from figlib import render_roles  # noqa: E402

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))), "vol2-architecture")


def fig_9_1():
    body = """  a [label="建内核\\n注册内置", fillcolor="#e8eef6", color="#1f3a5f"];
  b [label="扫描清单", fillcolor="#e8eef6", color="#1f3a5f"];
  c [label="依赖排序", fillcolor="#f6efdd", color="#b08a2e"];
  d [label="逐个 init\\n失败回滚", fillcolor="#f6efdd", color="#b08a2e"];
  e [label="开总线\\n进主循环", fillcolor="#e8f2ec", color="#2f6b4f"];
  a -> b;
  b -> c;
  c -> d [label="按序"];
  d -> e [label="分发缓存"];
"""
    render_roles(body, os.path.join(ROOT, "images", "09", "fig9-1-boot.png"))


def fig_9_2():
    body = """  a [label="请求保存\\n插件状态", fillcolor="#e8eef6", color="#1f3a5f"];
  b [label="撤登记\\n等在途结束", fillcolor="#f6efdd", color="#b08a2e"];
  c [label="卸载动态库", fillcolor="#f6efdd", color="#b08a2e"];
  d [label="重新加载\\nplugin_init", fillcolor="#e8eef6", color="#1f3a5f"];
  e [label="读回状态\\n重建图层", fillcolor="#e8f2ec", color="#2f6b4f"];
  a -> b;
  b -> c [label="借用归零"];
  c -> d;
  d -> e;
"""
    render_roles(body, os.path.join(ROOT, "images", "09", "fig9-2-reload.png"))


if __name__ == "__main__":
    fig_9_1()
    fig_9_2()
