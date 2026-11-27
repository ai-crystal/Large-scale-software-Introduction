# -*- coding: utf-8 -*-
"""第 18 章插图：快照由表单自己生成，管理者只负责保管和递回。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "common", "figstyle"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))
from figlib import render_roles  # noqa: E402

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))), "vol4-patterns")


def fig_18_1():
    body = """  kp [label="草稿管理
（管理者）", fillcolor="#f1f3f5", color="#6b7280"];
  og [label="报销表单
（原发器）", fillcolor="#f6efdd", color="#b08a2e"];
  me [label="快照
（备忘录）", fillcolor="#e8eef6", color="#1f3a5f"];
  st [label="本地存储", fillcolor="#ffffff", color="#6b7280"];
  kp -> og [label="要求快照 / 递回"];
  og -> me [label="create_memento"];
  me -> kp [label="交出快照", style=dashed];
  kp -> st [label="save / load"];
"""
    render_roles(body, os.path.join(ROOT, "images", "18", "fig18-1.png"))


def fig_18_2():
    body = """  fo [label="表单", fillcolor="#f6efdd", color="#b08a2e"];
  li [label="附件列表", fillcolor="#e8eef6", color="#1f3a5f"];
  at [label="附件对象", fillcolor="#ffffff", color="#6b7280"];
  bu [label="字节缓冲区", fillcolor="#ffffff", color="#6b7280"];
  sn [label="快照", fillcolor="#f6efdd", color="#b08a2e"];
  fo -> li [label="持有"];
  li -> at [];
  at -> bu [label="指向"];
  fo -> sn [label="生成时复制"];
  sn -> at [label="必须复制到这一层", style=dashed];
"""
    render_roles(body, os.path.join(ROOT, "images", "18", "fig18-2.png"))


if __name__ == "__main__":
    fig_18_1()
    fig_18_2()
