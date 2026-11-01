"""第 10 章：插件打包

用法：
    python pack.py <插件目录> <输出.zip>
例如：
    python pack.py plugins/hello hello-1.0.0.zip

做三件事：
    1. 按路径排序收集文件，保证同样的输入得到同样的包
    2. 固定时间戳，避免每次打包哈希都变
    3. 生成 SHA256SUMS.txt 一起打进包里，供 verify.py 校验
"""

import hashlib
import os
import sys
import zipfile

# 固定的时间戳。zip 默认写入当前时间，会导致两次打包字节不一致。
FIXED_TIME = (2026, 1, 1, 0, 0, 0)


def sha256_file(path):
    """算一个文件的 SHA-256 指纹。"""
    h = hashlib.sha256()
    # 分块读取，避免一次把大文件全读进内存。
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def collect(root):
    """收集目录下的所有文件，返回 (相对路径, 绝对路径) 列表。"""
    files = []
    for base, dirs, names in os.walk(root):
        # 排序，保证遍历顺序稳定。
        dirs.sort()
        names.sort()
        for name in names:
            path = os.path.join(base, name)
            # 统一用正斜杠，跨平台解压不会出问题。
            rel = os.path.relpath(path, root).replace("\\", "/")
            files.append((rel, path))
    return sorted(files)


def main():
    if len(sys.argv) < 3:
        print("用法: python pack.py <plugin_dir> <out.zip>")
        return

    root, out = sys.argv[1], sys.argv[2]
    files = collect(root)

    # 每个文件一行：哈希 + 两个空格 + 路径。
    # 两个空格是 sha256sum 工具的标准格式，方便外部工具复用。
    sums = "".join(f"{sha256_file(p)}  {rel}\n" for rel, p in files)

    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for rel, path in files:
            # 手动构造 ZipInfo，才能指定固定时间戳。
            info = zipfile.ZipInfo(rel, date_time=FIXED_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            with open(path, "rb") as f:
                z.writestr(info, f.read())

        # 把校验清单也放进包里。
        info = zipfile.ZipInfo("SHA256SUMS.txt", date_time=FIXED_TIME)
        info.compress_type = zipfile.ZIP_DEFLATED
        z.writestr(info, sums)

    print("已打包", out, "共", len(files), "个文件")


if __name__ == "__main__":
    main()
