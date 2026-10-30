// 第 3 章的示例插件：提供一个 hello 命令的雏形
#include "plugin_api.h"
#include <cstdio>

static int counter = 0;

extern "C" PLUGIN_EXPORT const char* plugin_name() {
    return "hello";
}

extern "C" PLUGIN_EXPORT int plugin_init() {
    std::printf("[hello] init\n");
    std::fflush(stdout);
    return 0;
}

extern "C" PLUGIN_EXPORT void plugin_shutdown() {
    std::printf("[hello] shutdown, counter=%d\n", counter);
    std::fflush(stdout);
}
