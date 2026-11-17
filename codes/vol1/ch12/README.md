# 第 12 章：完整最小外壳

```text
sdk/include/plugin_api.h   契约
host/                      宿主：注册表、事件、命令循环
plugins/hello/             hello 命令 + 订阅 file.saved
plugins/notes/             note 命令
```

## 构建

```bash
cmake -B build
cmake --build build --config Release
```

## 运行

Windows：

```bat
build\host\Release\host.exe
```

Linux：

```bash
./build/host/host
```

要保证工作目录里能找到 `plugins` 目录，所以从 `build` 目录里运行，或者把 `plugins` 复制到可执行文件旁边。

## 试一试

```text
> help
> hello 世界
> note 今天学了插件
> save
> quit
```

`save` 会先经过宿主钩子，在内容前加一行注释，然后发出 `file.saved` 事件，`hello` 插件会打印收到的消息。
