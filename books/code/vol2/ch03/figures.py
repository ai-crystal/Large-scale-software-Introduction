# -*- coding: utf-8 -*-
"""第 3 章插图：管道的两种顺序，以及声明式与命令式两条提交路径。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "common", "figstyle"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))
from figlib import render_roles  # noqa: E402

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))), "vol2-architecture")


def fig_3_1():
    body = """  subgraph cluster_bad {
    label="先加标签，后转义";
    style=dashed; color="#9b3b32"; fontcolor="#9b3b32";
    b1 [label="原始文本"];
    b2 [label="处理粗体"];
    b3 [label="转义 < > &"];
    b4 [label="页面上显示 <b>", fillcolor="#f7e9e7", color="#9b3b32"];
    b1 -> b2 -> b3 -> b4;
  }
  subgraph cluster_ok {
    label="先转义，后加标签";
    style=dashed; color="#2f6b4f"; fontcolor="#2f6b4f";
    o1 [label="原始文本"];
    o2 [label="转义 < > &"];
    o3 [label="处理粗体"];
    o4 [label="HTML 正常", fillcolor="#e8f2ec", color="#2f6b4f"];
    o1 -> o2 -> o3 -> o4;
  }
"""
    render_roles(body, os.path.join(ROOT, "images", "03", "fig3-1.png"))


def fig_3_2():
    body = """  decl [label="清单里的 contributes\\n纯数据", fillcolor="#e8eef6", color="#1f3a5f"];
  code [label="插件代码里的调用\\nadd_button(...)", fillcolor="#e8eef6", color="#1f3a5f"];
  host [label="宿主启动时收集\\n冲突可以提前算"];
  api  [label="api->add_extension\\n只在初始化期有效", fillcolor="#f6efdd", color="#b08a2e"];
  ep   [label="同一个扩展点容器\\n同一套校验规则"];
  late [label="窗口还没创建就加\\n贡献无处可去", fillcolor="#f7e9e7", color="#9b3b32"];
  decl -> host [label="解析"];
  host -> ep [];
  code -> api [label="调用"];
  api -> ep [];
  code -> late [style=dashed];
"""
    render_roles(body, os.path.join(ROOT, "images", "03", "fig3-2.png"))


if __name__ == "__main__":
    fig_3_1()
    fig_3_2()
