"""第 10 章：校验插件包

用法：
    python verify.py <包.zip>

读取包里的 SHA256SUMS.txt，逐个文件重新算哈希并比对。
任何一个对不上，就说明文件在打包之后被改过。
"""

import hashlib
import sys
import zipfile


def main():
    if len(sys.argv) < 2:
        print("用法: python verify.py <package.zip>")
        return

    with zipfile.ZipFile(sys.argv[1]) as z:
        names = z.namelist()

        # 没有清单就无法校验，直接报错。
        if "SHA256SUMS.txt" not in names:
            print("缺少 SHA256SUMS.txt")
            return

        # 读清单，建成 路径 -> 哈希 的字典。
        expected = {}
        for line in z.read("SHA256SUMS.txt").decode("utf-8").splitlines():
            if not line.strip():
                continue
            digest, path = line.split("  ", 1)
            expected[path] = digest

        # 逐个文件重新计算并比对。
        failed = 0
        for path, digest in expected.items():
            actual = hashlib.sha256(z.read(path)).hexdigest()
            if actual != digest:
                print("校验失败:", path)
                failed += 1

        print("通过" if failed == 0 else f"{failed} 个文件失败")


if __name__ == "__main__":
    main()
