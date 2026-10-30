#include "plugin_api.h"
#include <cstdio>

static void on_saved(const char* type, const char* payload) {
    std::printf("[hello] 收到事件 %s：%s\n", type, payload ? payload : "");
    std::fflush(stdout);
}

static void run_hello(const char* args) {
    std::printf("你好，世界（参数：%s）\n", args ? args : "");
    std::fflush(stdout);
}

static const PluginCommand kCommands[] = {
    { "hello", "打印一句问候", run_hello },
};

extern "C" PLUGIN_EXPORT const char* plugin_name() { return "hello"; }

extern "C" PLUGIN_EXPORT int plugin_init(const PluginApi* api) {
    if (!api || api->version != PLUGIN_API_VERSION) return 1;
    for (const auto& cmd : kCommands) api->register_command(&cmd);
    api->on_event("file.saved", on_saved);
    return 0;
}

extern "C" PLUGIN_EXPORT void plugin_shutdown() {}
