# -*- coding: utf-8 -*-
"""第 5 章插图：一条流水线按耗时分层，越慢的越少跑。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "common", "figstyle"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))
from figlib import render_roles  # noqa: E402

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))), "vol3-engineering")


def fig_5_1():
    body = """  push [label="每次提交代码", fillcolor="#f6efdd", color="#b08a2e"];
  pr [label="发起合并请求", fillcolor="#f6efdd", color="#b08a2e"];
  tag [label="打上版本标签", fillcolor="#f6efdd", color="#b08a2e"];
  fast [label="格式检查与编译\n几十秒", fillcolor="#e8eef6", color="#1f3a5f"];
  mid [label="三平台矩阵构建\n几分钟", fillcolor="#e8eef6", color="#1f3a5f"];
  slow [label="打包与冒烟安装\n复用测过的那份产物", fillcolor="#e8f2ec", color="#2f6b4f"];
  push -> fast [];
  pr -> mid [];
  tag -> slow [];
"""
    render_roles(body, os.path.join(ROOT, "images", "05", "fig5-1.png"), rankdir="TB", fontsize=7.0)


if __name__ == "__main__":
    fig_5_1()
