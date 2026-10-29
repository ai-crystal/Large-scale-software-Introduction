# 附录 A 术语表

## 程序与编译

**源代码**
人写的程序文本。计算机不能直接执行，需要经过编译或者解释。

**编译**
把源代码翻译成计算机能执行的形式。C++ 的编译通常分两步：先编译成目标文件，再链接成可执行文件。

**目标文件**
编译单个源文件得到的中间产物。Windows 上是 `.obj`，Linux 上是 `.o`。它包含机器指令和符号表，但还不能直接运行。

**链接**
把多个目标文件和库拼成一个可执行文件。链接器负责把“调用某个函数”的位置填上真实地址。

**静态库**
把一堆目标文件打包成一个文件。Windows 上是 `.lib`，Linux 上是 `.a`。链接时被复制进程序。

**动态库**
运行时才被加载的库。Windows 上是 `.dll`，Linux 上是 `.so`。多个程序可以共用，插件系统的基础。

**符号**
编译器给函数和全局变量起的名字，写在目标文件里。链接器靠符号找东西。

**名字修饰**
C++ 把参数类型编进函数名的过程。不同编译器规则不同，所以跨动态库的接口要用 `extern "C"`。

**头文件**
放声明、类型、常量的文件，被 `#include` 展开到源文件里。它共享的是“能做什么”，不是“怎么做”。

**编译单元**
一个源文件加上它包含的所有头文件。编译器一次处理一个编译单元。

**构建**
从源码到可运行产物的整个过程，包括编译、链接、复制资源。

## 插件与接口

**插件**
由宿主之外的人开发、在宿主运行时加载的模块。

**宿主**
负责发现、加载、管理和隔离插件的程序。

**内核**
宿主中最稳定的部分，提供加载、注册、事件、资源管理。

**接口**
双方约定的调用方式。它描述“能做什么”，不暴露内部实现。

**契约**
接口、数据格式、版本规则、行为约定的总称。

**清单**
描述插件名字、版本、入口、依赖、权限的文件，通常是一个 JSON。

**导出表**
动态库里记录“外部可以调用哪些函数”的表。

**函数指针**
保存函数地址的变量。取到地址后可以像普通函数一样调用。

**回调**
你先交给别人一个函数，别人在合适的时候替你调用。

**扩展点**
宿主在某个位置留下的命名入口，插件向它提交实现。

**注册表**
按名字保存命令、服务或者资源的表。

**所有者**
注册表里记录“这条是谁注册的”，卸载时按它清理。

**语义化版本**
用主版本、次版本、修订号三个数字表示兼容性。主版本变化表示不兼容。

**ABI**
二进制接口。它规定结构体怎么排、函数怎么调用、名字怎么修饰。跨动态库时，两边必须遵守同一套 ABI。

## 运行与隔离

**进程**
操作系统分配给一个运行中程序的独立空间，包括内存、打开的文件和正在执行的代码。

**线程**
进程里的执行流。多个线程共享同一块内存。

**内存对齐**
结构体字段在内存里按特定边界排列，为了让处理器读得更快。

**序列化**
把内存里的数据变成一串字节，便于传输或者保存。反过来叫反序列化。

**管道**
操作系统提供的一根通道，一头写、另一头读，用于进程间通信。

**进程间通信**
两个进程交换数据的统称。管道、套接字、共享内存都是它的实现方式。

**沙箱**
给代码划出的受限活动范围。代码只能使用允许的资源。

**故障域**
一个地方出错时最多影响的范围。

**超时**
等待一段时间后放弃，避免永远卡住。

**熔断**
连续失败后暂时拒绝请求，冷却后再试探。

**降级**
主要功能不可用时，退而求其次。

**RAII**
资源获取即初始化。把资源的生命周期绑在对象上，析构时自动释放。

**内存泄漏**
申请的内存没有归还，越积越多，最后耗尽。

**空指针**
没有指向任何有效对象的指针。通过它读写会触发崩溃。

**数组越界**
访问数组范围之外的位置，可能改坏别的数据。

## 工程与发布

**包**
分发单位，通常是一个压缩文件，包含清单、产物和说明。

**CMake**
一个生成构建文件的工具。写一份配置，它在不同平台生成对应的构建文件。

**哈希**
把任意长度的数据压成固定长度的指纹。内容变一个字节，指纹就完全不同。

**签名**
用私钥对内容算出的校验值。别人用公钥验证，确认来源和完整性。

**公钥 / 私钥**
一对配对的密码。私钥自己保存用来签名，公钥公开用来验证。

**路径穿越**
压缩包里带 `../` 这样的路径，解压后写到目标目录之外。安装时要防护。

**原子操作**
要么全部完成，要么完全没发生，不会停在中间。文件重命名通常是原子的。

**灰度**
先把新版本发给一小部分用户，观察后再扩大范围。

**回滚**
发现问题后退回上一个可用版本。

**热更新**
不重启程序，直接替换插件代码或者资源。

**持续集成**
服务器在每次提交后自动编译、测试、打包。

**假宿主**
只实现接口、不实现真实功能的最小宿主，用来测试插件。

**契约版本**
描述接口兼容性的版本号，和产品版本分开。

# 附录 B 延伸阅读

下面列出书中涉及的主要文献，按主题排列。论文原文放在项目本地的 `papers` 目录。

**模块化与软件设计**

Parnas, D. L. On the Criteria To Be Used in Decomposing Systems into Modules. Communications of the ACM, 15(12), 1972.

Gamma, E., Helm, R., Johnson, R., Vlissides, J. Design Patterns: Elements of Reusable Object-Oriented Software. Addison-Wesley, 1994.

Fowler, M. Patterns of Enterprise Application Architecture. Addison-Wesley, 2002.

**插件架构与模块系统**

OSGi Alliance. OSGi Core Specification, Release 8. 2020.

Kiczales, G., Lamping, J., Mendhekar, A., et al. Aspect-Oriented Programming. Proceedings of ECOOP, 1997.

El-Sharkawy, S., Krafczyk, A., Schmid, K. MetricHaven: More Than 23,000 Metrics for Measuring Quality Attributes of Software Product Lines. 2021. arXiv:2110.09755.

**模组生态的实证研究**

Lee, D., Rajbahadur, G. K., Lin, D., Sayagh, M., Bezemer, C.-P., Hassan, A. E. An Empirical Study of the Characteristics of Popular Minecraft Mods. 2021. arXiv:2103.14439.

**动态更新与兼容性**

Mlinaric, D., Mornar, V. Dynamic Software Updating in Java: Comparing Concepts and Resource Demands. 2025. arXiv:2506.01875.

Shen, J., Bazzi, R. A. A Formal Study on Backward Compatible Dynamic Software Updates. 2015. arXiv:1503.07235.

**隔离与安全**

Perrone, G., Romano, S. P. WebAssembly and Security: A Review. 2024. arXiv:2407.12297.

Ehret, A., Abraham, J., Isakov, M., Kinsy, M. A. Zeno: A Scalable Capability-Based Secure Architecture. 2022. arXiv:2208.09800.

**C++ 与工程实践**

Stroustrup, B. The C++ Programming Language. 4th edition. Addison-Wesley, 2013.

Meyers, S. Effective Modern C++. O'Reilly Media, 2014.

Nygard, M. T. Release It! Design and Deploy Production-Ready Software. 2nd edition. Pragmatic Bookshelf, 2018.
