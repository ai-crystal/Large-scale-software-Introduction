# -*- coding: utf-8 -*-
"""第 6 章插图：接口在适配器这里拐一个弯，业务代码不用改。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "common", "figstyle"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))
from figlib import render_roles  # noqa: E402

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))), "vol4-patterns")


def fig_06_1():
    body = """  cli [label="结算代码", fillcolor="#f1f3f5", color="#6b7280"];
  tg [label="支付接口\npay(order)", fillcolor="#f6efdd", color="#b08a2e"];
  ad [label="渠道适配器", fillcolor="#e8eef6", color="#1f3a5f"];
  ae [label="第三方 SDK\n接口对不上", fillcolor="#ffffff", color="#6b7280"];
  cli -> tg [label="只认识接口"];
  tg -> ad [label="实现", style=dashed];
  ad -> ae [label="转换参数"];
  ae -> ad [label="返回结果", style=dashed];
  ad -> cli [label="统一成自己的结果", style=dashed];
"""
    render_roles(body, os.path.join(ROOT, "images", "06", "fig6-1.png"))


if __name__ == "__main__":
    fig_06_1()
