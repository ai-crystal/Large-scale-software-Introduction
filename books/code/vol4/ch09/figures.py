# -*- coding: utf-8 -*-
"""第 9 章插图：四层实现同一个客户端接口，能力一层层包上去，顺序就是包装顺序。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "common", "figstyle"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from figlib import render_roles  # noqa: E402

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))), "vol4-patterns")


def fig_09_1():
    body = """  cli [label="业务代码", fillcolor="#f1f3f5", color="#6b7280"];
  d3 [label="缓存装饰器", fillcolor="#e8eef6", color="#1f3a5f"];
  d2 [label="日志装饰器", fillcolor="#e8eef6", color="#1f3a5f"];
  d1 [label="重试装饰器", fillcolor="#e8eef6", color="#1f3a5f"];
  ba [label="真实客户端\n解码并发送", fillcolor="#e8eef6", color="#1f3a5f"];
  cli -> d3 [label="调用"];
  d3 -> d2 [label="包住"];
  d2 -> d1 [label="包住"];
  d1 -> ba [label="包住"];
"""
    render_roles(body, os.path.join(ROOT, "images", "09", "fig9-1.png"))


if __name__ == "__main__":
    fig_09_1()
