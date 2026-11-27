# -*- coding: utf-8 -*-
"""第 4 章插图：同一份代码在三个层次上被验证。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "common", "figstyle"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))
from figlib import render_roles  # noqa: E402

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))), "vol3-engineering")


def fig_4_1():
    body = """  mh [label="假宿主", fillcolor="#f6efdd", color="#b08a2e"];
  load [label="加载\n取符号、调 init", fillcolor="#e8eef6", color="#1f3a5f"];
  caps [label="能力实现\n日志、存储、事件", fillcolor="#e8eef6", color="#1f3a5f"];
  rec [label="记录表\n命令、日志、钩子", fillcolor="#e8eef6", color="#1f3a5f"];
  probe [label="查询接口\n给测试断言用", fillcolor="#e8f2ec", color="#2f6b4f"];
  mh -> load [];
  mh -> caps [];
  mh -> rec [];
  rec -> probe [];
"""
    render_roles(body, os.path.join(ROOT, "images", "04", "fig4-1.png"), fontsize=7.4)


if __name__ == "__main__":
    fig_4_1()
