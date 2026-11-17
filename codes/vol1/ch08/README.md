# 第 8 章：模板与生成器

本目录是生成器的完整素材，不是一次编译的工程。

```text
templates/plugin/   插件模板
tools/new_plugin.py 生成脚本
```

在 `codes/` 根目录执行：

```bash
python ch08/tools/new_plugin.py hello
```

它会在当前目录下创建 `plugins/hello/`，把 `{{name}}` 替换成 `hello`。
