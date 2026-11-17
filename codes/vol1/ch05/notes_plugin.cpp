// 第 5 章：notes 插件
//
// 第二个插件，用来演示：
//   1. 多个插件可以各自注册命令
//   2. 每个插件注册的命令带各自的 owner
//   3. 卸载一个插件时，不会影响另一个

#include "plugin_api.h"
#include <cstdio>

// note 命令的实现：把用户输入的参数原样打印出来。
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
    return 0;
}

extern "C" PLUGIN_EXPORT void plugin_shutdown() {
}
