# -*- coding: utf-8 -*-
"""第 13 章插图：请求沿着链往后走，谁有权谁处理。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "common", "figstyle"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))
from figlib import render_roles  # noqa: E402

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))), "vol4-patterns")


def fig_13_1():
    body = """  rq [label="报销请求", fillcolor="#f1f3f5", color="#6b7280"];
  h1 [label="组长\n500 以下", fillcolor="#e8eef6", color="#1f3a5f"];
  h2 [label="部门经理\n500 到 5000", fillcolor="#e8eef6", color="#1f3a5f"];
  h3 [label="总监\n5000 到 5 万", fillcolor="#e8eef6", color="#1f3a5f"];
  h4 [label="总裁办\n5 万以上", fillcolor="#e8eef6", color="#1f3a5f"];
  rq -> h1 [];
  h1 -> h2 [label="额度不够，交给下一个"];
  h2 -> h3 [label="额度不够"];
  h3 -> h4 [label="额度不够"];
"""
    render_roles(body, os.path.join(ROOT, "images", "13", "fig13-1.png"))


if __name__ == "__main__":
    fig_13_1()
