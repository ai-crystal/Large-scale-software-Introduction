# 大型软件开发技术

一套讲可扩展系统的书。从一段二十行的 C++ 程序开始，逐步做出一个能加载插件、能隔离故障、能打包更新的系统，再往下讨论架构取舍和工程交付。

作者：Dr. Dezeming

## 三册

| 册 | 主题 | 页数 | 在线阅读 | PDF |
|---|---|---|---|---|
| 入门篇 | 用 C++ 从二十行代码到一个插件系统 | 142 | [开始阅读](books/vol1-basics/README.md) | [下载](output/vol1-basics.pdf) |
| 架构篇 | 可扩展系统的内核、契约与协作机制 | 73 | [开始阅读](books/vol2-architecture/README.md) | [下载](output/vol2-architecture.pdf) |
| 工程篇 | 组件模板、分发生态与稳定运行 | 67 | [开始阅读](books/vol3-engineering/README.md) | [下载](output/vol3-engineering.pdf) |

## 三册的关系

**入门篇**从一段会打印命令的程序开始，拆函数、拆文件、装插件、建契约，一路做到能打包更新的小系统。每一章只加一个概念，代码都能编译运行。适合没有大型项目经验、想弄清插件系统到底怎么运转的读者。

**架构篇**接着入门篇的系统往下走，处理插件变多之后的问题：命名冲突、故障扩散、插件之间怎么互相调用、契约怎么演进、插件跑在哪个进程。这一册的很多决定没有唯一答案，书里会说明每种方案的适用条件。

**工程篇**把结构变成可以交付的工程：用模板固定组件结构，用生成器创建骨架，用假宿主独立测试，用签名和灰度把插件安全地送到用户手里，用日志和指标定位问题。

三册共用一套代码和例子，建议按顺序读。如果只想解决具体问题，架构篇和工程篇也可以单独看，每册开头会说明前置。

## 在线阅读

完整站点：<https://ai-crystal.github.io/Large-scale-software-Introduction/>

## 配套代码

三册的代码在根目录 `codes/` 下，按册和章分目录：

```text
codes/vol1/         入门篇，ch01 到 ch12
```

入门篇的代码可以用 MSVC 一次全部编译，产物放在 `build/`：

```bat
build-codes.bat
```

## 编译本书

需要 Python 3.10 以上和 Chrome 或 Edge。克隆仓库后双击根目录的 `一键生成PDF.bat`，或者按册单独构建：

```bash
python books/build/build.py --book books/vol1-basics
python books/build/build.py --book books/vol2-architecture
python books/build/build.py --book books/vol3-engineering
python books/build/build.py --all
```

PDF 输出到 `output/`，文件名由各册的 `book.json` 决定。

## 许可

本书采用 [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) 许可协议。
