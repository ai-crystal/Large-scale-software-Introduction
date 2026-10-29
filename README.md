# 大型软件是怎么长出来的

> 用 C++ 从二十行代码到一个插件系统

作者：Dr. Dezeming

这本书从一段二十行的 C++ 程序开始，一步一步把它改造成能加载插件、能隔离故障、能打包更新的小系统。每一章只增加一个概念，每个概念都落到能编译、能运行的代码里。

不假设你懂 Java，也不假设你学过操作系统。进程、链接、动态库、序列化这些词第一次出现时，都会先用日常经验讲明白。

## 在线阅读

完整站点：<https://feimos.github.io/cpp-plugin-book/>

也可以直接在 GitHub 上按章阅读：

- [前言](book/front/preface.md)
- [第 1 章 二十行程序](book/chapters/ch01.md)

## 下载

[下载完整 PDF](output/book.pdf)

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

## 本地编译

需要 Python 3.10 以上和 Chrome 或 Edge。克隆仓库后双击根目录的 `一键生成PDF.bat`，脚本会安装依赖、生成插图、排版 PDF，结果写到 `output/book.pdf`。

书里的 C++ 示例需要 C++17 编译器。Windows 可以用 Visual Studio，Linux 可以用 GCC 或 Clang。

## 许可

本书采用 [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) 许可协议。
