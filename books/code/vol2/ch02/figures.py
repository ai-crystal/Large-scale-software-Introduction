# -*- coding: utf-8 -*-
"""第 2 章插图：机制与策略的分界，以及一次服务调用的路径。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "common", "figstyle"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))
from figlib import render_roles  # noqa: E402

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))), "vol2-architecture")


def fig_2_1():
    body = """  subgraph cluster_k {
    label="内核，只放机制";
    style=dashed; color="#b08a2e"; fontcolor="#b08a2e";
    m1 [label="register_service", fillcolor="#f6efdd", color="#b08a2e"];
    m2 [label="emit_event", fillcolor="#f6efdd", color="#b08a2e"];
  }
  s1 [label="索引插件\\n注册什么由它定", fillcolor="#e8eef6", color="#1f3a5f"];
  s2 [label="保存流程\\n发什么事件由它定", fillcolor="#e8eef6", color="#1f3a5f"];
  leak [label="if (event == 业务事件名)\\n策略漏进内核", fillcolor="#f7e9e7", color="#9b3b32", style=dashed];
  s1 -> m1 [label="调用"];
  s2 -> m2 [label="调用"];
"""
    render_roles(body, os.path.join(ROOT, "images", "02", "fig2-1.png"))


def fig_2_2():
    body = """  c [label="插件 A\\nservice(\\"index.query\\")", fillcolor="#e8eef6", color="#1f3a5f"];
  g [label="内核\\n权限检查", fillcolor="#f6efdd", color="#b08a2e"];
  t [label="服务表\\n按名字查"];
  ok [label="拿到实现指针\\n调用成功", fillcolor="#e8f2ec", color="#2f6b4f"];
  e1 [label="没有权限\\n返回 nullptr", fillcolor="#f7e9e7", color="#9b3b32"];
  e2 [label="名字未注册或已撤销\\n返回 nullptr", fillcolor="#f7e9e7", color="#9b3b32"];
  c -> g [];
  g -> t [label="有权"];
  g -> e1 [label="无权"];
  t -> ok [label="命中"];
  t -> e2 [label="未命中"];
"""
    render_roles(body, os.path.join(ROOT, "images", "02", "fig2-2.png"))


if __name__ == "__main__":
    fig_2_1()
    fig_2_2()
