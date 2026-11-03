# 大型软件开发技术：入门篇

> 用 C++ 从二十行代码到一个插件系统

作者：Dr. Dezeming

这本书从一段二十行的 C++ 程序开始，一步一步把它改造成能加载插件、能隔离故障、能打包更新的小系统。每一章只增加一个概念，每个概念都落到能编译、能运行的代码里。

不假设你懂 Java，也不假设你学过操作系统。进程、链接、动态库、序列化这些词第一次出现时，都会先用日常经验讲明白。

## 在线阅读

完整站点：<https://ai-crystal.github.io/Large-scale-software-Introduction/>

也可以直接在 GitHub 上按章阅读：

- [前言](book/front/preface.md)
- [第 1 章 二十行程序](book/chapters/ch01.md)

## 下载

[下载完整 PDF](output/book.pdf)

## 配套代码

每章的完整代码在根目录的 `codes/` 下，按 `ch01` 到 `ch12` 分目录，可以直接编译运行。总览见 [codes/README.md](codes/README.md)。

## 目录

**第一篇 从一段程序开始**

1. [二十行程序](book/chapters/ch01.md)
2. [把代码拆开](book/chapters/ch02.md)
3. [第一个插件](book/chapters/ch03.md)

**第二篇 把边界建起来**

4. [接口就是合同](book/chapters/ch04.md)
5. [注册表与扩展点](book/chapters/ch05.md)
6. [事件与钩子](book/chapters/ch06.md)
7. [插件出错怎么办](book/chapters/ch07.md)

**第三篇 把代码变成工程**

8. [一条命令生成插件](book/chapters/ch08.md)
9. [让插件独立开发](book/chapters/ch09.md)
10. [打包、分发与更新](book/chapters/ch10.md)

**第四篇 收拢**

11. [让它稳定运行](book/chapters/ch11.md)
12. [把整个系统跑起来](book/chapters/ch12.md)

**附录**

- [术语表与延伸阅读](book/appendix/appendix.md)

## 编译示例代码

根目录的 `build-codes.bat` 会调用本机的 MSVC，把 `codes/` 下每一章的代码编译到 `build/`，一章一个子目录：

```text
build/ch01/app.exe
build/ch02/app.exe
build/ch03/host.exe        build/ch03/plugins/hello_plugin.dll
build/ch05/host.exe        build/ch05/plugins/*.dll
build/ch07/host.exe        build/ch07/plugin_host.exe
build/ch09/mock_host.exe   build/ch09/test_registry.exe
build/ch11/raii_demo.exe   build/ch11/breaker_demo.exe
build/ch12/host.exe        build/ch12/plugins/*.dll
```

目标文件和可执行文件都放在 `build/` 里，不会写到源码目录。`build/` 是生成目录，不进入 Git。

脚本会自动寻找 `vcvars64.bat`。如果找不到，说明没有安装 Visual Studio 的“使用 C++ 的桌面开发”工作负载。

`ch08` 和 `ch10` 是 Python 工具，不需要编译，脚本里会打印用法。

## 编译本书 PDF

需要 Python 3.10 以上和 Chrome 或 Edge。克隆仓库后双击根目录的 `一键生成PDF.bat`，脚本会安装依赖、生成插图、排版 PDF，结果写到 `output/book.pdf`。

书里的 C++ 示例需要 C++17 编译器。Windows 可以用 Visual Studio，Linux 可以用 GCC 或 Clang。

## 许可

本书采用 [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) 许可协议。
