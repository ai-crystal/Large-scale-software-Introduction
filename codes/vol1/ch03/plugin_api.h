// 第 3 章：插件接口
//
// 这个头文件是宿主和插件之间唯一的约定。
// 插件必须导出下面三个函数，宿主才能找到它、启动它、关闭它。
//
// 三个函数都放在 extern "C" 里，原因见第 3.4 节：
// C++ 会把参数类型编进函数名（名字修饰），不同编译器编出来的名字不一样。
// 插件可能是别人用别的编译器做的，用 C 的命名规则才能跨编译器找到。

#pragma once

// 导出标记：
//   Windows 上展开成 __declspec(dllexport)，表示“写进导出表，外面能调用”
//   Linux 上展开成 __attribute__((visibility("default")))，意思类似
// 没有这个标记，动态库里的函数默认不对外可见，宿主取不到。
#ifdef _WIN32
#define PLUGIN_EXPORT __declspec(dllexport)
#else
#define PLUGIN_EXPORT __attribute__((visibility("default")))
#endif

extern "C" {

// 返回插件的名字，比如 "hello"。
// 宿主用这个名字显示插件，也用它作为命令的归属。
PLUGIN_EXPORT const char* plugin_name();

// 插件被加载后调用，做初始化。
// 返回 0 表示成功，非 0 表示失败，宿主会跳过这个插件。
PLUGIN_EXPORT int plugin_init();

// 插件被卸载前调用，做清理。
PLUGIN_EXPORT void plugin_shutdown();

}
