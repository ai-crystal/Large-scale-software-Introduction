// 第 6 章：notes 插件
//
// 第二个插件，用来证明命令表仍然是主线：
// hello 插件注册 hello 命令，notes 插件注册 note 命令，
// 两个命令都能在同一个循环里被调用。
// notes 不订阅事件，保存时它不会被通知。

#include "plugin_api.h"
#include <cstdio>

static void run_note(const char* args) {
    std::printf("note: %s\n", args ? args : "（空）");
    std::fflush(stdout);
}

static const PluginCommand kCommands[] = {
    { "note", "记录一句话", run_note },
};

extern "C" PLUGIN_EXPORT const char* plugin_name() {
    return "notes";
}

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

extern "C" PLUGIN_EXPORT void plugin_shutdown() {
}
