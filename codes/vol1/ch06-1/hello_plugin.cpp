// 第 6 章（第一阶段）：hello 插件
//
// 演示两件事：
//   1. 注册 hello 命令
//   2. 订阅 file.saved 事件
// 钩子相关的代码在第二阶段 codes/ch06-2 才加入。

#include "plugin_api.h"
#include <cstdio>

static const PluginApi* g_api = nullptr;

static void on_saved(const char* type, const char* payload) {
    std::printf("[hello] 收到事件 %s：%s\n", type, payload ? payload : "");
    std::fflush(stdout);
}

static void run_hello(const char* args) {
    if (g_api && g_api->log_info) {
        g_api->log_info("hello 命令被执行");
    }
    std::printf("你好，世界（参数：%s）\n", args ? args : "");
    std::fflush(stdout);
}

static const PluginCommand kCommands[] = {
    { "hello", "打印一句问候", run_hello },
};

extern "C" PLUGIN_EXPORT const char* plugin_name() {
    return "hello";
}

extern "C" PLUGIN_EXPORT int plugin_init(const PluginApi* api) {
    if (!api || api->version != PLUGIN_API_VERSION) return 1;

    g_api = api;

    for (const auto& cmd : kCommands) {
        api->register_command(&cmd);
    }

    api->on_event("file.saved", on_saved);

    if (api->log_info) {
        api->log_info("hello 插件已加载");
    }
    return 0;
}

extern "C" PLUGIN_EXPORT void plugin_shutdown() {
    g_api = nullptr;
}
