# -*- coding: utf-8 -*-
"""第 3 章插图：契约包站在宿主和插件中间，只声明不实现。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "common", "figstyle"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))
from figlib import render_roles  # noqa: E402

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))), "vol3-engineering")


def fig_3_1():
    body = """  host [label="宿主\\n实现全部能力", fillcolor="#f6efdd", color="#b08a2e"];
  sdk [label="契约包\\n类型、常量、版本、能力名", fillcolor="#e8eef6", color="#1f3a5f"];
  a [label="插件 A", fillcolor="#e8f2ec", color="#2f6b4f"];
  b [label="插件 B", fillcolor="#e8f2ec", color="#2f6b4f"];
  host -> sdk [label="照着实现"];
  sdk -> a [label="只声明"];
  sdk -> b [];
"""
    render_roles(body, os.path.join(ROOT, "images", "03", "fig3-1.png"), fontsize=8.6)


if __name__ == "__main__":
    fig_3_1()
