# -*- coding: utf-8 -*-
"""第 6 章插图：跨进程的一条消息通道，以及权限检查的三步。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "common", "figstyle"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))
from figlib import render_roles  # noqa: E402

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))), "vol2-architecture")


def fig_6_1():
    body = """  h [label="宿主进程\\n命令循环", fillcolor="#f6efdd", color="#b08a2e"];
  p [label="插件宿主进程\\n插件 A、B", fillcolor="#e8eef6", color="#1f3a5f"];
  to [label="超时\\n杀进程并标记不可用", fillcolor="#f7e9e7", color="#9b3b32"];
  h -> p [label="请求帧\\nseq + 超时"];
  p -> h [label="响应帧\\n同一个 seq"];
  hb [label="心跳\\n发现对端卡死", fillcolor="#f1f3f5", color="#6b7280"];
  p -> hb [style=dotted];
  hb -> to [style=dotted];
  h -> to [style=dashed, label="到期没回"];
"""
    render_roles(body, os.path.join(ROOT, "images", "06", "fig6-1.png"))


def fig_6_2():
    body = """  pl [label="插件\\nread(...)", fillcolor="#e8eef6", color="#1f3a5f"];
  chk [label="查权限表", fillcolor="#f6efdd", color="#b08a2e"];
  join [label="规范化路径\\n拼到根下"];
  ok [label="返回内容", fillcolor="#e8f2ec", color="#2f6b4f"];
  deny [label="无权或越界\\n返回错误", fillcolor="#f7e9e7", color="#9b3b32"];
  pl -> chk [];
  chk -> join [label="有权"];
  chk -> deny [label="无权"];
  join -> ok [label="仍在根内"];
  join -> deny [label="越界"];
"""
    render_roles(body, os.path.join(ROOT, "images", "06", "fig6-2.png"))


if __name__ == "__main__":
    fig_6_1()
    fig_6_2()
