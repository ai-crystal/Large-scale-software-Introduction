// 第 12 章：notes 插件
//
// 只注册一条 note 命令，演示多个插件共存。
// 它不订阅事件，所以不需要 on_event。

#include "plugin_api.h"
#include <cstdio>

static void run_note(const char* args) {
    std::printf("note: %s\n", args ? args : "（空）");
    std::fflush(stdout);
}

static const PluginCommand kCommands[] = {
    { "note", "记录一句话", run_note },
};

extern "C" PLUGIN_EXPORT const char* plugin_name() { return "notes"; }

extern "C" PLUGIN_EXPORT int plugin_init(const PluginApi* api) {
    if (!api || api->version != PLUGIN_API_VERSION) return 1;
    for (const auto& cmd : kCommands) {
        api->register_command(&cmd);
    }

    if (api->log_info) {
        api->log_info("notes 插件已加载");
    }
    return 0;
}

extern "C" PLUGIN_EXPORT void plugin_shutdown() {}
