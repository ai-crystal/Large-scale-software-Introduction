# -*- coding: utf-8 -*-
"""第 21 章插图：选哪套算法由外部决定，上下文只负责调用。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "common", "figstyle"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))
from figlib import render_roles  # noqa: E402

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))), "vol4-patterns")


def fig_21_1():
    body = """  se [label="策略选择器
按订单特征挑一个", fillcolor="#f1f3f5", color="#6b7280"];
  ca [label="运费计算
（上下文）", fillcolor="#f6efdd", color="#b08a2e"];
  st [label="运费策略
fee(order)", fillcolor="#f6efdd", color="#b08a2e"];
  f1 [label="满额包邮", fillcolor="#e8eef6", color="#1f3a5f"];
  f2 [label="冷链计件", fillcolor="#e8eef6", color="#1f3a5f"];
  f3 [label="偏远加收", fillcolor="#e8eef6", color="#1f3a5f"];
  se -> ca [label="选中并注入"];
  ca -> st [label="委托"];
  st -> f1 [label="实现", style=dashed];
  st -> f2 [style=dashed];
  st -> f3 [style=dashed];
"""
    render_roles(body, os.path.join(ROOT, "images", "21", "fig21-1.png"))


def fig_21_2():
    body = """  od [label="订单", fillcolor="#ffffff", color="#6b7280"];
  se [label="选择器", fillcolor="#e8eef6", color="#1f3a5f"];
  c1 [label="基础运费", fillcolor="#f6efdd", color="#b08a2e"];
  c2 [label="偏远加收", fillcolor="#f6efdd", color="#b08a2e"];
  c3 [label="冷链附加", fillcolor="#f6efdd", color="#b08a2e"];
  sm [label="求和并出行明细", fillcolor="#e8eef6", color="#1f3a5f"];
  od -> se [label="特征签名"];
  se -> c1 [label="装配生效的项"];
  se -> c2 [];
  se -> c3 [];
  c1 -> sm [label="金额与规则名"];
  c2 -> sm [];
  c3 -> sm [];
"""
    render_roles(body, os.path.join(ROOT, "images", "21", "fig21-2.png"))


if __name__ == "__main__":
    fig_21_1()
    fig_21_2()
