// 第 12 章：hello 插件
//
// 完整的插件示例：
//   1. 注册 hello 命令
//   2. 订阅 file.saved 事件
// 卸载时没有动态资源，所以 plugin_shutdown 是空的。

#include "plugin_api.h"
#include <cstdio>

// 事件处理函数：保存完成后打印一行。
static void on_saved(const char* type, const char* payload) {
    std::printf("[hello] 收到事件 %s：%s\n", type, payload ? payload : "");
    std::fflush(stdout);
}

// 命令执行函数。
static void run_hello(const char* args) {
    std::printf("你好，世界（参数：%s）\n", args ? args : "");
    std::fflush(stdout);
}

// 命令数组。加命令就往这里加一行。
static const PluginCommand kCommands[] = {
    { "hello", "打印一句问候", run_hello },
};

extern "C" PLUGIN_EXPORT const char* plugin_name() { return "hello"; }

extern "C" PLUGIN_EXPORT int plugin_init(const PluginApi* api) {
    if (!api || api->version != PLUGIN_API_VERSION) return 1;

    // 注册命令。
    for (const auto& cmd : kCommands) {
        api->register_command(&cmd);
    }

    // 订阅事件。
    api->on_event("file.saved", on_saved);
    return 0;
}

extern "C" PLUGIN_EXPORT void plugin_shutdown() {}
