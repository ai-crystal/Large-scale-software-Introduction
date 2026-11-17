// 第 4 章：插件接口（带命令注册）
//
// 和第 3 章相比，这里多了两样东西：
//   1. PluginCommand：描述“一条命令”长什么样
//   2. PluginApi：宿主递给插件的工具箱，里面有注册函数和日志函数
//
// 跨动态库只能传“两边布局完全一致”的东西，所以这里只有
// 整数、指针和 C 风格字符串，没有 std::string、std::function。

#pragma once

#include <cstdint>   // uint32_t：固定 4 字节，不随平台变化

#ifdef _WIN32
#define PLUGIN_EXPORT __declspec(dllexport)
#else
#define PLUGIN_EXPORT __attribute__((visibility("default")))
#endif

// 当前契约版本。不兼容的改动加一，兼容的改动不加。
#define PLUGIN_API_VERSION 1

extern "C" {

// “执行命令”的函数类型：接收一个参数串，不返回值。
// 插件里的每个命令都要符合这个形状，宿主才能统一调用。
typedef void (*CommandFn)(const char* args);

// 一条命令的描述。
// 注意三个字段都是指针，没有 C++ 对象，跨编译器布局一致。
typedef struct PluginCommand {
    const char* name;   // 命令名，比如 "hello"
    const char* help;   // 一句说明，显示帮助时用
    CommandFn run;      // 执行函数的地址
} PluginCommand;

// “注册命令”的函数类型：接收一条命令，不返回值。
// 这个函数由宿主实现，插件调用。
typedef void (*RegisterCommandFn)(const PluginCommand* cmd);

// 宿主递给插件的工具箱。
// size 和 version 是说明书，后面两个是能力。
typedef struct PluginApi {
    uint32_t size;                        // 这个结构体有多少字节，宿主填
    uint32_t version;                     // 契约版本，宿主填
    RegisterCommandFn register_command;   // 插件用它把命令交给宿主
    void (*log_info)(const char* message); // 插件用它输出日志
} PluginApi;

// 三个导出函数，第 3 章已经见过，只是 init 多了一个参数。
PLUGIN_EXPORT const char* plugin_name();
PLUGIN_EXPORT int plugin_init(const PluginApi* api);
PLUGIN_EXPORT void plugin_shutdown();

}
