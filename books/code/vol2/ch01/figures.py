# -*- coding: utf-8 -*-
"""第 1 章插图：两种加载顺序下，同一次保存的结果差异。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "common", "figstyle"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))
from figlib import render_roles  # noqa: E402

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))), "vol2-architecture")


def fig_1_1():
    body = """  s [label="保存完成\\n发 file.saved", fillcolor="#f6efdd", color="#b08a2e"];
  subgraph cluster_a {
    label="index 先加载";
    style=dashed; color="#2f6b4f"; fontcolor="#2f6b4f";
    a1 [label="index\\n补元数据并写回"];
    a2 [label="sync\\n读到带元数据的版本"];
    a3 [label="远端正确", fillcolor="#e8f2ec", color="#2f6b4f"];
    a1 -> a2 -> a3;
  }
  subgraph cluster_b {
    label="sync 先加载";
    style=dashed; color="#9b3b32"; fontcolor="#9b3b32";
    b1 [label="sync\\n读到原版并上传"];
    b2 [label="index\\n补元数据并写回"];
    b3 [label="远端缺元数据", fillcolor="#f7e9e7", color="#9b3b32"];
    b1 -> b2 -> b3;
  }
  s -> a1 [];
  s -> b1 [];
"""
    render_roles(body, os.path.join(ROOT, "images", "01", "fig1-1.png"))


def fig_1_2():
    body = """  core [label="内核", fillcolor="#f6efdd", color="#b08a2e"];
  cmd [label="命令表\\nname → { fn, owner }"];
  svc [label="服务表\\nname → { impl, owner }"];
  sub [label="订阅表\\ntype → [ { fn, owner } ]"];
  core -> cmd [label="注册与分发"];
  core -> svc [];
  core -> sub [];
  cmd -> unload [label="remove_owner", style=dashed];
  svc -> unload [style=dashed];
  sub -> unload [style=dashed];
  unload [label="卸载时按 owner 清干净", fillcolor="#e8f2ec", color="#2f6b4f"];
"""
    render_roles(body, os.path.join(ROOT, "images", "01", "fig1-2.png"))


if __name__ == "__main__":
    fig_1_1()
    fig_1_2()
