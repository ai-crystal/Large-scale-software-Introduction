import os
import shutil
import sys

TEXT_EXT = (".cpp", ".h", ".txt", ".json", ".md")

def render(text, values):
    for key, value in values.items():
        text = text.replace("{{" + key + "}}", value)
    return text

def main():
    if len(sys.argv) < 2:
        print("用法: python new_plugin.py <name>")
        return

    name = sys.argv[1]
    target = os.path.join("plugins", name)

    if os.path.exists(target):
        print("目录已存在:", target)
        return

    shutil.copytree("templates/plugin", target)

    for root, dirs, files in os.walk(target):
        for filename in files:
            if not filename.endswith(TEXT_EXT):
                continue
            path = os.path.join(root, filename)
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
            with open(path, "w", encoding="utf-8") as f:
                f.write(render(text, {"name": name}))

    print("已创建", target)
    print("下一步: cd", target, "&& cmake -B build && cmake --build build")

if __name__ == "__main__":
    main()
