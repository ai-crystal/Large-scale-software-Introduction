#include "plugin_api.h"
#include <cstdio>

static void run_{{name}}(const char* args) {
    std::printf("{{name}} 命令执行，参数：%s\n", args ? args : "");
    std::fflush(stdout);
}

static const PluginCommand kCommands[] = {
    { "{{name}}", "{{name}} 插件的示例命令", run_{{name}} },
};

extern "C" PLUGIN_EXPORT const char* plugin_name() {
    return "{{name}}";
}

extern "C" PLUGIN_EXPORT int plugin_init(const PluginApi* api) {
    if (!api || api->version != PLUGIN_API_VERSION) return 1;
    for (const auto& cmd : kCommands) {
        api->register_command(&cmd);
    }
    return 0;
}

extern "C" PLUGIN_EXPORT void plugin_shutdown() {
}
