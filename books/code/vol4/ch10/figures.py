# -*- coding: utf-8 -*-
"""第 10 章插图：四个子系统被收在一个入口后面，调用方不必知道顺序。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "common", "figstyle"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))
from figlib import render_roles  # noqa: E402

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))), "vol4-patterns")


def fig_10_1():
    body = """  cli [label="上传入口", fillcolor="#f1f3f5", color="#6b7280"];
  fa [label="转码外观\ntranscode(file)\n内部按顺序执行", fillcolor="#f6efdd", color="#b08a2e"];
  s1 [label="解封装", fillcolor="#ffffff", color="#6b7280"];
  s2 [label="转码", fillcolor="#ffffff", color="#6b7280"];
  s3 [label="切片", fillcolor="#ffffff", color="#6b7280"];
  s4 [label="写入存储", fillcolor="#ffffff", color="#6b7280"];
  cli -> fa [label="一次调用"];
  fa -> s1 [];
  fa -> s2 [];
  fa -> s3 [];
  fa -> s4 [];
"""
    render_roles(body, os.path.join(ROOT, "images", "10", "fig10-1.png"))


if __name__ == "__main__":
    fig_10_1()
