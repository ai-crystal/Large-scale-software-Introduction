# -*- coding: utf-8 -*-
"""第 11 章插图：信号与迁移。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "common", "figstyle"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))
from figlib import render_roles  # noqa: E402

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))), "vol2-architecture")


def fig_11_1():
    body = """  a [label="现象\\n同一个 bug 第三次", fillcolor="#f7e9e7", color="#9b3b32"];
  b [label="归因\\n缺哪一层", fillcolor="#f6efdd", color="#b08a2e"];
  c [label="一次只动一块", fillcolor="#e8eef6", color="#1f3a5f"];
  d [label="观察两个月\\n指标是否回落", fillcolor="#e8f2ec", color="#2f6b4f"];
  a -> b;
  b -> c;
  c -> d;
  d -> a [label="下一个信号", style=dashed];
"""
    render_roles(body, os.path.join(ROOT, "images", "11", "fig11-1-signal.png"))


def fig_11_2():
    body = """  s [label="宿主开关\\nWarn / Enforce", fillcolor="#f6efdd", color="#b08a2e"];
  o [label="旧路径\\n只告警不拒绝", fillcolor="#f1f3f5", color="#6b7280"];
  n [label="新路径\\n检查并拒绝", fillcolor="#e8eef6", color="#1f3a5f"];
  h [label="同一份日志\\n统计影响面", fillcolor="#e8f2ec", color="#2f6b4f"];
  t [label="两个版本后\\n删掉旧路径", fillcolor="#f7e9e7", color="#9b3b32"];
  s -> o [label="Warn"];
  s -> n [label="Enforce"];
  o -> h;
  n -> h;
  h -> t [label="数量收敛"];
"""
    render_roles(body, os.path.join(ROOT, "images", "11", "fig11-2-migrate.png"))


if __name__ == "__main__":
    fig_11_1()
    fig_11_2()
