# -*- coding: utf-8 -*-
"""第 19 章插图：下单的人不知道谁在关心，关心的人自己来登记。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "common", "figstyle"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from figlib import render_roles  # noqa: E402

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))), "vol4-patterns")


def fig_19_1():
    body = """  su [label="订单\n（主题）", fillcolor="#f6efdd", color="#b08a2e"];
  o1 [label="锁定库存", fillcolor="#e8eef6", color="#1f3a5f"];
  o2 [label="增加积分", fillcolor="#e8eef6", color="#1f3a5f"];
  o3 [label="发送通知", fillcolor="#e8eef6", color="#1f3a5f"];
  o4 [label="记录流水", fillcolor="#e8eef6", color="#1f3a5f"];
  su -> o1 [label="notify(事件)"];
  su -> o2 [];
  su -> o3 [];
  su -> o4 [];
  o1 -> su [label="订阅与退订", style=dashed];
"""
    render_roles(body, os.path.join(ROOT, "images", "19", "fig19-1.png"))


if __name__ == "__main__":
    fig_19_1()
