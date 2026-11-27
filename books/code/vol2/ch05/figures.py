# -*- coding: utf-8 -*-
"""第 5 章插图：三类订阅者的执行顺序与失败分支，钩子链的短路与撤销。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "common", "figstyle"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))
from figlib import render_roles  # noqa: E402

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))), "vol2-architecture")


def fig_5_1():
    body = """  g [label="拦截者\\n最先跑", fillcolor="#f6efdd", color="#b08a2e"];
  m [label="修改者\\n中间", fillcolor="#e8eef6", color="#1f3a5f"];
  o [label="观察者\\n最后", fillcolor="#e8eef6", color="#1f3a5f"];
  done [label="事件分发结束", fillcolor="#e8f2ec", color="#2f6b4f"];
  e1 [label="拒绝\\n流程中止", fillcolor="#f7e9e7", color="#9b3b32"];
  e2 [label="抛异常\\n中止并回滚", fillcolor="#f7e9e7", color="#9b3b32"];
  e3 [label="抛异常\\n跳过并记日志", fillcolor="#f7e9e7", color="#9b3b32"];
  g -> m [label="放行"];
  m -> o [];
  o -> done [];
  g -> e1 [style=dashed];
  m -> e2 [style=dashed];
  o -> e3 [style=dashed];
"""
    render_roles(body, os.path.join(ROOT, "images", "05", "fig5-1.png"))


def fig_5_2():
    body = """  s [label="请求保存"];
  h1 [label="钩子 1\\n只读检查"];
  h2 [label="钩子 2\\n改内容"];
  h3 [label="钩子 3\\n拦截判断", fillcolor="#f6efdd", color="#b08a2e"];
  ok [label="写盘", fillcolor="#e8f2ec", color="#2f6b4f"];
  abort [label="倒序撤销\\n恢复原内容", fillcolor="#f7e9e7", color="#9b3b32"];
  s -> h1 [];
  h1 -> h2 [];
  h2 -> h3 [];
  h3 -> ok [label="全部放行"];
  h3 -> abort [label="拒绝"];
  h1 -> abort [style=dashed, label="出错"];
  h2 -> abort [style=dashed];
"""
    render_roles(body, os.path.join(ROOT, "images", "05", "fig5-2.png"))


if __name__ == "__main__":
    fig_5_1()
    fig_5_2()
