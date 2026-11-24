# -*- coding: utf-8 -*-
"""第 22 章插图：顺序由模板方法定死，差异留在子类里。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "common", "figstyle"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from figlib import render_roles  # noqa: E402

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))), "vol4-patterns")


def fig_22_1():
    body = """  sub [label="Excel 导入器\n（子类）", fillcolor="#e8eef6", color="#1f3a5f"];
  tm [label="导入流程\nrun() 模板方法", fillcolor="#f6efdd", color="#b08a2e"];
  s1 [label="① 读文件\n（抽象步骤）", fillcolor="#ffffff", color="#6b7280"];
  s2 [label="② 解析\n（抽象步骤）", fillcolor="#ffffff", color="#6b7280"];
  s3 [label="③ 校验\n（公共步骤）", fillcolor="#ffffff", color="#6b7280"];
  s4 [label="④ 写库与日志\n（公共步骤）", fillcolor="#ffffff", color="#6b7280"];
  sub -> tm [label="只填抽象步骤", style=dashed];
  tm -> s1 [];
  tm -> s2 [];
  tm -> s3 [];
  tm -> s4 [];
"""
    render_roles(body, os.path.join(ROOT, "images", "22", "fig22-1.png"))


if __name__ == "__main__":
    fig_22_1()
