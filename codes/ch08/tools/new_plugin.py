"""第 8 章：插件生成器

用法（在 codes 目录下执行）：
    python ch08/tools/new_plugin.py hello

它会把 templates/plugin 复制到 plugins/hello，
并把文件内容里的 {{name}} 替换成 hello。
"""

import os
import shutil
import sys

# 需要做文本替换的文件类型。
# 图片、字体这类二进制文件不能按文本读，直接原样复制。
TEXT_EXT = (".cpp", ".h", ".txt", ".json", ".md")


def render(text, values):
    """把文本里的 {{key}} 替换成 values[key]。"""
    for key, value in values.items():
        text = text.replace("{{" + key + "}}", value)
    return text


def main():
    # sys.argv[0] 是脚本名，后面才是用户输入。
    if len(sys.argv) < 2:
        print("用法: python new_plugin.py <name>")
        return

    name = sys.argv[1]

    # 生成到当前目录的 plugins/<name>。
    target = os.path.join("plugins", name)

    # 目录已存在就停下，绝不覆盖别人写好的代码。
    if os.path.exists(target):
        print("目录已存在:", target)
        return

    # 复制整个模板目录（包括子目录）。
    shutil.copytree("templates/plugin", target)

    # 遍历刚复制出来的目录树。
    # os.walk 每次给出：当前目录、子目录列表、文件列表。
    for root, dirs, files in os.walk(target):
        for filename in files:
            if not filename.endswith(TEXT_EXT):
                continue

            path = os.path.join(root, filename)

            # 读入、替换、写回。
            # with 块结束时自动关闭文件，不用手动 close。
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
            with open(path, "w", encoding="utf-8") as f:
                f.write(render(text, {"name": name}))

    print("已创建", target)
    print("下一步: cd", target, "&& cmake -B build && cmake --build build")


if __name__ == "__main__":
    main()
