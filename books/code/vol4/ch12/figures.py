# -*- coding: utf-8 -*-
"""第 12 章插图：访问控制、延迟创建、缓存都加在代理这一层。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "common", "figstyle"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from figlib import render_roles  # noqa: E402

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))), "vol4-patterns")


def fig_12_1():
    body = """  cli [label="相册界面", fillcolor="#f1f3f5", color="#6b7280"];
  su [label="图片接口\nthumb()", fillcolor="#f6efdd", color="#b08a2e"];
  px [label="缩略图代理", fillcolor="#e8eef6", color="#1f3a5f"];
  re [label="真实图片\n解码开销大", fillcolor="#ffffff", color="#6b7280"];
  cli -> su [label="按需显示"];
  su -> px [label="实现", style=dashed];
  px -> re [label="第一次访问才创建"];
  re -> px [label="像素数据", style=dashed];
  px -> cli [label="缓存后直接返回", style=dashed];
"""
    render_roles(body, os.path.join(ROOT, "images", "12", "fig12-1.png"))


if __name__ == "__main__":
    fig_12_1()
