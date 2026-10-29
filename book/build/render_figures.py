# -*- coding: utf-8 -*-
"""生成全部插图：先跑封面，再按章跑 book/code/chNN/figures.py。"""
import glob
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BOOK = os.path.join(ROOT, "book")


def main():
    scripts = [os.path.join(BOOK, "code", "cover", "cover_art.py")]
    scripts += sorted(glob.glob(os.path.join(BOOK, "code", "ch*", "figures.py")))
    for script in scripts:
        print("·", os.path.relpath(script, ROOT))
        subprocess.run([sys.executable, script], check=True)


if __name__ == "__main__":
    main()
