# -*- coding: utf-8 -*-
"""生成全部插图：按册、按章遍历 books/code/<册>/chNN/figures.py。"""
import glob
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CODE = os.path.join(ROOT, "books", "code")


def main():
    scripts = []
    for vol in sorted(os.listdir(CODE)):
        vol_dir = os.path.join(CODE, vol)
        if not os.path.isdir(vol_dir):
            continue
        cover = os.path.join(vol_dir, "cover", "cover_art.py")
        if os.path.exists(cover):
            scripts.append(cover)
        scripts.extend(sorted(glob.glob(os.path.join(vol_dir, "ch*", "figures.py"))))

    if not scripts:
        print("books/code 下没有找到绘图脚本")
        return

    for script in scripts:
        print("·", os.path.relpath(script, ROOT))
        subprocess.run([sys.executable, script], check=True)


if __name__ == "__main__":
    main()
