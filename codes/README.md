# 配套代码

每章一个目录，和书里的章节一一对应。代码用 C++17 编写，只依赖标准库。

## 目录

| 目录 | 内容 | 怎么用 |
|---|---|---|
| `ch01` | 二十行的命令循环 | `cl /EHsc /std:c++17 /utf-8 main.cpp` |
| `ch02` | 函数、头文件、多文件编译 | `cmake -B build && cmake --build build` |
| `ch03` | 动态库、函数指针、第一个插件 | 同上，产物在 `build/plugins` |
| `ch04` | 契约结构体、命令注册 | 同上 |
| `ch05` | 命令表、所有者、冲突、卸载 | 同上，运行 `host` 后输入 `help` |
| `ch06` | 事件总线、钩子 | 同上，运行后自动演示保存流程 |
| `ch07` | 独立进程、管道、超时 | Windows 专用，见目录内 README |
| `ch08` | 插件模板与生成脚本 | `python tools/new_plugin.py hello` |
| `ch09` | 假宿主、断言测试 | `cmake -B build && ctest --test-dir build` |
| `ch10` | 打包与校验脚本 | `python pack.py <dir> <out.zip>` |
| `ch11` | 熔断器、RAII | `cmake -B build && cmake --build build` |
| `ch12` | 完整最小外壳 | 构建后运行 `build/host/host` |

## 构建环境

- Windows：Visual Studio 2019 或更新，开发者命令行里执行 `cl`
- Linux：GCC 9+ 或 Clang 10+
- CMake 3.16+

## 说明

`ch03` 到 `ch07` 的宿主会扫描当前目录下的 `plugins` 子目录。用 CMake 构建时，插件产物已经放在 `build/plugins`，从 `build` 目录里运行宿主即可。

`ch07` 的管道代码是 Windows 版本。Linux 的对应函数写在那个目录的 README 里，思路完全一样。

`ch08` 和 `ch10` 是工具脚本，不参与 C++ 编译。
