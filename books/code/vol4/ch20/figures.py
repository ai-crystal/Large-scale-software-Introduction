# -*- coding: utf-8 -*-
"""第 20 章插图：订单的五个状态与允许的转移，每个操作都先交给当前状态处理。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "common", "figstyle"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from figlib import render_roles  # noqa: E402

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))), "vol4-patterns")


def fig_20_1():
    body = """  p [label="待付款", fillcolor="#e8eef6", color="#1f3a5f"];
  pa [label="已付款", fillcolor="#e8eef6", color="#1f3a5f"];
  sh [label="已发货", fillcolor="#e8eef6", color="#1f3a5f"];
  si [label="已签收", fillcolor="#e8eef6", color="#1f3a5f"];
  ca [label="已取消", fillcolor="#e8eef6", color="#1f3a5f"];
  p -> pa [label="pay"];
  pa -> sh [label="ship"];
  sh -> si [label="confirm"];
  p -> ca [label="cancel"];
  pa -> ca [];
"""
    render_roles(body, os.path.join(ROOT, "images", "20", "fig20-1.png"))


if __name__ == "__main__":
    fig_20_1()
