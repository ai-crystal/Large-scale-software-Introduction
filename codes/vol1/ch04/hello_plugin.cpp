// 第 4 章：示例插件
//
// 插件在 plugin_init 里做两件事：
//   1. 检查宿主给的工具箱版本对不对
//   2. 把命令数组里的每一条，通过 register_command 交给宿主
//
// 命令数组是静态的，生命周期和插件一样长，
// 所以把指针交给宿主是安全的。

#include "plugin_api.h"
#include <cstdio>

// 保存宿主递过来的工具箱，命令执行时还要用（比如写日志）。
// static：只在本文件可见。
static const PluginApi* g_api = nullptr;

// 执行 hello 命令时调用的函数。
// 参数是用户输入命令时带的额外文字，比如 "hello 世界" 里的 "世界"。
static void run_hello(const char* args) {
    if (g_api && g_api->log_info) {
        g_api->log_info("hello 命令被执行");
    }
    std::printf("你好，世界（参数：%s）\n", args ? args : "");
    std::fflush(stdout);
}

// 这个插件提供的所有命令。
// 现在只有一条，以后加命令只需要往数组里加一行。
static const PluginCommand kCommands[] = {
    { "hello", "打印一句问候", run_hello },
};

extern "C" PLUGIN_EXPORT const char* plugin_name() {
    return "hello";
}

extern "C" PLUGIN_EXPORT int plugin_init(const PluginApi* api) {
    // 工具箱必须有，版本必须对，否则拒绝加载。
    if (!api) return 1;
    if (api->version != PLUGIN_API_VERSION) return 2;

    g_api = api;

    // 逐条注册。register_command 是宿主提供的函数，
    // 插件只是把命令的地址递过去。
    for (const auto& cmd : kCommands) {
        api->register_command(&cmd);
    }
    return 0;
}

extern "C" PLUGIN_EXPORT void plugin_shutdown() {
    g_api = nullptr;   // 卸载后不再使用宿主的能力
}
