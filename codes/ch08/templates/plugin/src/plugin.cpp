// 第 8 章：插件模板
//
// 这是模板源文件，不是直接编译的文件。
// 生成器会把下面所有 {{name}} 替换成实际的插件名，比如 hello。
//
// 生成后的文件可以：
//   1. 用 CMake 编译成动态库
//   2. 放进宿主的 plugins 目录
//   3. 被宿主加载，注册一条和插件同名的命令

#include "plugin_api.h"
#include <cstdio>

// 命令的执行函数。{{name}} 会被替换成插件名，
// 所以生成 hello 插件后，这个函数叫 run_hello。
static void run_{{name}}(const char* args) {
    std::printf("{{name}} 命令执行，参数：%s\n", args ? args : "");
    std::fflush(stdout);
}

// 这个插件提供的命令。名字和插件名相同，方便记忆。
static const PluginCommand kCommands[] = {
    { "{{name}}", "{{name}} 插件的示例命令", run_{{name}} },
};

extern "C" PLUGIN_EXPORT const char* plugin_name() {
    return "{{name}}";
}

extern "C" PLUGIN_EXPORT int plugin_init(const PluginApi* api) {
    if (!api || api->version != PLUGIN_API_VERSION) return 1;

    // 把命令逐条交给宿主。宿主会填上 owner，记在这个插件名下。
    for (const auto& cmd : kCommands) {
        api->register_command(&cmd);
    }
    return 0;
}

extern "C" PLUGIN_EXPORT void plugin_shutdown() {
    // 模板没有动态资源。如果插件创建了文件、线程、定时器，
    // 要在这里释放，否则卸载后会泄漏。
}
