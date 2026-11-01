// 第 3 章：示例插件
//
// 这个文件编译成一个动态库（Windows 上是 hello_plugin.dll，
// Linux 上是 hello_plugin.so）。宿主在运行时把它读进来，
// 调用下面三个导出函数。
//
// 编译（Windows 开发者命令行）：
//   cl /EHsc /std:c++17 /utf-8 /LD hello_plugin.cpp /Fe:plugins\hello_plugin.dll
// 编译（Linux）：
//   g++ -std=c++17 -shared -fPIC hello_plugin.cpp -o plugins/hello_plugin.so
//
// /LD 和 -shared 都表示“生成动态库”，不是可执行文件。

#include "plugin_api.h"
#include <cstdio>   // printf、fflush

// 插件自己的状态：记录初始化了多少次。
// static 表示这个变量只在当前文件可见，别的插件有同名变量也不冲突。
static int counter = 0;

// 实现头文件里声明的第一个函数。
// 返回的字符串是字面量，生命周期和程序一样长，宿主可以安全地保存指针。
extern "C" PLUGIN_EXPORT const char* plugin_name() {
    return "hello";
}

// 宿主加载插件后调用这里。
extern "C" PLUGIN_EXPORT int plugin_init() {
    std::printf("[hello] init\n");

    // printf 的输出可能先放在缓冲区里，不立刻显示。
    // fflush 强制把它送到屏幕，保证输出顺序和代码顺序一致。
    std::fflush(stdout);

    ++counter;
    return 0;   // 0 表示初始化成功
}

// 宿主卸载插件前调用这里，做清理。
extern "C" PLUGIN_EXPORT void plugin_shutdown() {
    std::printf("[hello] shutdown, counter=%d\n", counter);
    std::fflush(stdout);
}
