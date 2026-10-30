import hashlib
import os
import sys
import zipfile

FIXED_TIME = (2026, 1, 1, 0, 0, 0)

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def collect(root):
    files = []
    for base, dirs, names in os.walk(root):
        dirs.sort()
        names.sort()
        for name in names:
            path = os.path.join(base, name)
            rel = os.path.relpath(path, root).replace("\\", "/")
            files.append((rel, path))
    return sorted(files)

def main():
    if len(sys.argv) < 3:
        print("用法: python pack.py <plugin_dir> <out.zip>")
        return

    root, out = sys.argv[1], sys.argv[2]
    files = collect(root)
    sums = "".join(f"{sha256_file(p)}  {rel}\n" for rel, p in files)

    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for rel, path in files:
            info = zipfile.ZipInfo(rel, date_time=FIXED_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            with open(path, "rb") as f:
                z.writestr(info, f.read())
        info = zipfile.ZipInfo("SHA256SUMS.txt", date_time=FIXED_TIME)
        info.compress_type = zipfile.ZIP_DEFLATED
        z.writestr(info, sums)

    print("已打包", out, "共", len(files), "个文件")

if __name__ == "__main__":
    main()
