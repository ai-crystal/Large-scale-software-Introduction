// 第 6 章：hello 插件（带事件订阅）
//
// 这个插件除了注册命令，还订阅 file.saved 事件。
// 它不需要知道谁保存了文件，只要在事件发生时打印一行。

#include "plugin_api.h"
#include <cstdio>

// 事件处理函数。签名必须和 EventFn 一致。
static void on_saved(const char* type, const char* payload) {
    std::printf("[hello] 收到事件 %s：%s\n", type, payload ? payload : "");
    std::fflush(stdout);
}

static void run_hello(const char* args) {
    std::printf("你好，世界（参数：%s）\n", args ? args : "");
    std::fflush(stdout);
}

static const PluginApi* g_api = nullptr;

static const PluginCommand kCommands[] = {
    { "hello", "打印一句问候", run_hello },
};

extern "C" PLUGIN_EXPORT const char* plugin_name() {
    return "hello";
}

extern "C" PLUGIN_EXPORT int plugin_init(const PluginApi* api) {
    if (!api || api->version != PLUGIN_API_VERSION) return 1;

    for (const auto& cmd : kCommands) {
        api->register_command(&cmd);
    }

    // 保存工具箱，后面如果需要写日志可以用。
    g_api = api;

    // 用宿主提供的日志接口写一条，日志会自动带上插件名。
    if (api->log_info) {
        api->log_info("hello 插件已加载，准备订阅 file.saved");
    }

    // 订阅事件。第二个参数是事件处理函数的地址。
    api->on_event("file.saved", on_saved);

    return 0;
}

extern "C" PLUGIN_EXPORT void plugin_shutdown() {
    g_api = nullptr;
}
