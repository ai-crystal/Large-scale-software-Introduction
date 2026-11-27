# -*- coding: utf-8 -*-
"""第 8 章插图：渲染服务的取舍。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "common", "figstyle"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))
from figlib import render_roles  # noqa: E402

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))), "vol2-architecture")


def fig_8_1():
    body = """  a [label="插件写命令\\n本帧缓冲", fillcolor="#e8eef6", color="#1f3a5f"];
  c [label="宿主校验\\n归属 坐标 纹理", fillcolor="#f6efdd", color="#b08a2e"];
  d [label="按 z 序合成", fillcolor="#f6efdd", color="#b08a2e"];
  e [label="上传显存\\n输出到屏幕", fillcolor="#e8f2ec", color="#2f6b4f"];
  x [label="单条丢弃\\n节流记日志", fillcolor="#f7e9e7", color="#9b3b32"];
  a -> c;
  c -> d [label="通过"];
  c -> x [label="拒绝"];
  d -> e;
"""
    render_roles(body, os.path.join(ROOT, "images", "08", "fig8-1-frame.png"))


def fig_8_2():
    body = """  a [label="插件进程\\n没有显卡上下文", fillcolor="#e8eef6", color="#1f3a5f"];
  p1 [label="共享纹理句柄\\n零拷贝", fillcolor="#f6efdd", color="#b08a2e"];
  p2 [label="回读像素\\n再上传", fillcolor="#f6efdd", color="#b08a2e"];
  p3 [label="命令加数据\\n宿主代绘", fillcolor="#f6efdd", color="#b08a2e"];
  z [label="宿主进程\\n持有显卡设备", fillcolor="#e8f2ec", color="#2f6b4f"];
  a -> p1 [label="一次共享"];
  a -> p2 [label="读完再传"];
  a -> p3 [label="几十字节"];
  p1 -> z [label="微秒级"];
  p2 -> z [label="毫秒级"];
  p3 -> z [label="一次往返"];
"""
    render_roles(body, os.path.join(ROOT, "images", "08", "fig8-2-crossproc.png"))


if __name__ == "__main__":
    fig_8_1()
    fig_8_2()
