// 第 5 章：hello 插件
//
// 和上一章相比，命令表多了 owner，宿主在注册时自动填上。
// 命令执行时，宿主会把“当前插件”设成命令的 owner，
// 所以这里可以通过 log_info 写日志，日志会自动带上插件名。

#include "plugin_api.h"
#include <cstdio>

// 保存宿主递过来的工具箱，命令执行时要用它写日志。
static const PluginApi* g_api = nullptr;

static void run_hello(const char* args) {
    if (g_api && g_api->log_info) {
        g_api->log_info("hello 命令被执行");
    }
    std::printf("你好，世界（参数：%s）\n", args ? args : "");
    std::fflush(stdout);
}

// 这个插件提供的命令。命令名在整张表里必须唯一。
static const PluginCommand kCommands[] = {
    { "hello", "打印一句问候", run_hello },
};

extern "C" PLUGIN_EXPORT const char* plugin_name() {
    return "hello";
}

extern "C" PLUGIN_EXPORT int plugin_init(const PluginApi* api) {
    if (!api || api->version != PLUGIN_API_VERSION) return 1;

    g_api = api;

    // 逐条交给宿主，owner 由宿主填。
    for (const auto& cmd : kCommands) {
        api->register_command(&cmd);
    }
    return 0;
}

extern "C" PLUGIN_EXPORT void plugin_shutdown() {
    g_api = nullptr;
}
