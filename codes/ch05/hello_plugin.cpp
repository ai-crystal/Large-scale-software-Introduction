// 第 5 章：hello 插件
//
// 和上一章几乎一样，只是命令表多了 owner，
// 而 owner 由宿主在注册时自动填上，插件不需要传。

#include "plugin_api.h"
#include <cstdio>

static void run_hello(const char* args) {
    std::printf("你好，世界（参数：%s）\n", args ? args : "");
    std::fflush(stdout);
}

// 这个插件提供的命令。
// 命令名 hello 在整张表里必须唯一，重名会被宿主拒绝。
static const PluginCommand kCommands[] = {
    { "hello", "打印一句问候", run_hello },
};

extern "C" PLUGIN_EXPORT const char* plugin_name() {
    return "hello";
}

extern "C" PLUGIN_EXPORT int plugin_init(const PluginApi* api) {
    if (!api || api->version != PLUGIN_API_VERSION) return 1;

    // 逐条交给宿主。
    // 宿主会用自己的当前插件名填 owner，所以这里不用管归属。
    for (const auto& cmd : kCommands) {
        api->register_command(&cmd);
    }
    return 0;
}

extern "C" PLUGIN_EXPORT void plugin_shutdown() {
    // 这个插件没有动态资源，不需要清理。
}
