# -*- coding: utf-8 -*-
"""第 2 章插图：生成器把参数和模板变成一堆文件，再由自检确认能跑。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "common", "figstyle"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))
from figlib import render_roles  # noqa: E402

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))), "vol3-engineering")


def fig_2_1():
    body = """  arg [label="参数\\n缺的补默认值", fillcolor="#f6efdd", color="#b08a2e"];
  tpl [label="模板目录\\nbase + 选中的类型", fillcolor="#f6efdd", color="#b08a2e"];
  gen [label="生成器", fillcolor="#e8eef6", color="#1f3a5f"];
  txt [label="文本文件\\n替换占位符", fillcolor="#e8eef6", color="#1f3a5f"];
  bin [label="二进制文件\\n原样复制", fillcolor="#e8eef6", color="#1f3a5f"];
  exist [label="目标已存在\\n跳过或要求 --force", fillcolor="#f7e9e7", color="#9b3b32"];
  check [label="自检\\n编译、测试、冒烟加载", fillcolor="#e8f2ec", color="#2f6b4f"];
  arg -> gen [];
  tpl -> gen [];
  gen -> txt [];
  gen -> bin [];
  gen -> exist [style=dashed];
  txt -> check [];
  bin -> check [];
"""
    render_roles(body, os.path.join(ROOT, "images", "02", "fig2-1.png"), fontsize=9.0)


if __name__ == "__main__":
    fig_2_1()
