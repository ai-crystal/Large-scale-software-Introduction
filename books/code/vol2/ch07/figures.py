# -*- coding: utf-8 -*-
"""第 7 章插图：服务注册表。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "common", "figstyle"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))
from figlib import render_roles  # noqa: E402

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))), "vol2-architecture")


def fig_7_1():
    body = """  a [label="插件调用\\nrequire_service", fillcolor="#e8eef6", color="#1f3a5f"];
  b [label="取当前插件身份\\n查权限表", fillcolor="#f6efdd", color="#b08a2e"];
  c [label="服务表查名字\\n未就绪则懒加载", fillcolor="#f6efdd", color="#b08a2e"];
  f [label="返回实现指针", fillcolor="#e8f2ec", color="#2f6b4f"];
  g [label="返回空\\n走降级路径", fillcolor="#f7e9e7", color="#9b3b32"];
  a -> b;
  b -> c [label="允许"];
  b -> g [label="拒绝"];
  c -> f [label="找到"];
  c -> g [label="缺服务"];
"""
    render_roles(body, os.path.join(ROOT, "images", "07", "fig7-1-require.png"))


def fig_7_2():
    body = """  a [label="withdraw_owner\\n摘掉服务条目", fillcolor="#e8eef6", color="#1f3a5f"];
  b [label="命令表与总线\\n按 owner 清理", fillcolor="#e8eef6", color="#1f3a5f"];
  c [label="借用计数\\n归零吗", fillcolor="#f6efdd", color="#b08a2e"];
  d [label="dlclose\\n卸载动态库", fillcolor="#e8f2ec", color="#2f6b4f"];
  e [label="推迟到帧边界", fillcolor="#f7e9e7", color="#9b3b32"];
  a -> b;
  b -> c;
  c -> d [label="是"];
  c -> e [label="否"];
  e -> c [label="下一帧再查", style=dashed];
"""
    render_roles(body, os.path.join(ROOT, "images", "07", "fig7-2-unload.png"))


if __name__ == "__main__":
    fig_7_1()
    fig_7_2()
