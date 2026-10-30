#include "plugin_api.h"
#include <cstdio>

static const PluginApi* g_api = nullptr;

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
    if (!api) return 1;
    if (api->version != PLUGIN_API_VERSION) return 2;
    for (const auto& cmd : kCommands) {
        api->register_command(&cmd);
    }
    return 0;
}

extern "C" PLUGIN_EXPORT void plugin_shutdown() {
}
