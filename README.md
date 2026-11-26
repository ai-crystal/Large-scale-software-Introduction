# 大型软件开发技术

> 从二十行 C++ 代码到一个可交付的插件系统

一套讲大型软件开发的书。从一段二十行的 C++ 程序开始，逐步做出一个能加载插件、能隔离故障、能打包更新的系统；往下讨论架构取舍和工程交付；最后把写代码时反复用到的二十三种解法逐一讲清楚。

四册共用一套叙述方式，建议按顺序读。如果只想解决具体问题，后面三册也可以单独看，每册开头会说明前置。

作者：Dr. Dezeming　·　2026

**在线阅读**：[在线阅读站](https://ai-crystal.github.io/Large-scale-software-Introduction/)　·　**仓库**：[GitHub 仓库](https://github.com/ai-crystal/Large-scale-software-Introduction)

## 分册

| 册 | 书名 | 一句话 | 页数 | 在线阅读 | PDF |
| --- | --- | --- | ---: | --- | --- |
| 01 | [入门篇](books/vol1-basics/README.md) | 用 C++ 从二十行代码到一个插件系统 | 142 | [阅读](books/vol1-basics/README.md) | <a href="output/v1-basics.pdf" target="_blank" rel="noopener" data-router-ignore>下载</a> |
| 02 | [架构篇](books/vol2-architecture/README.md) | 可扩展系统的内核、契约与协作机制 | 73 | [阅读](books/vol2-architecture/README.md) | <a href="output/v2-architecture.pdf" target="_blank" rel="noopener" data-router-ignore>下载</a> |
| 03 | [工程篇](books/vol3-engineering/README.md) | 组件模板、分发生态与稳定运行 | 67 | [阅读](books/vol3-engineering/README.md) | <a href="output/v3-engineering.pdf" target="_blank" rel="noopener" data-router-ignore>下载</a> |
| 04 | [模式篇](books/vol4-patterns/README.md) | 二十三种可复用的解法 | 152 | [阅读](books/vol4-patterns/README.md) | <a href="output/v4-patterns.pdf" target="_blank" rel="noopener" data-router-ignore>下载</a> |

## 怎么读

- 没有大型项目经验：从入门篇开始，每章只加一个概念。
- 插件变多之后：读架构篇，处理命名、故障、互调与契约演进。
- 要把结构变成可交付工程：读工程篇的模板、生成器、签名与灰度。
- 回到代码本身：读模式篇的二十三种设计模式。

## 许可

本系列文字与插图采用 [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) 许可发布，转载请注明作者与出处。书中引用的论文、数据集与模型归各自作者所有。

---

作者：Dr. Dezeming　·　2026
