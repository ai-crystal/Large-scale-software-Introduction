// 第 4 章：宿主
//
// 宿主做了五件事：
//   1. 准备一张命令表
//   2. 实现 register_command 和 log_info 两个函数
//   3. 把这两个函数地址填进 PluginApi，递给插件
//   4. 加载插件，调用 plugin_init
//   5. 用户输入命令时，查表并调用插件给的函数

#include "plugin_api.h"

#include <cstdio>
#include <filesystem>
#include <map>
#include <string>
#include <vector>

#ifdef _WIN32
#include <windows.h>
#endif

// 平台差异封装，和第 3 章一样。
#ifdef _WIN32
using LibHandle = HMODULE;
static LibHandle open_lib(const std::string& p) { return LoadLibraryA(p.c_str()); }
static void* get_sym(LibHandle h, const char* n) { return (void*)GetProcAddress(h, n); }
static void close_lib(LibHandle h) { FreeLibrary(h); }
#else
#include <dlfcn.h>
using LibHandle = void*;
static LibHandle open_lib(const std::string& p) { return dlopen(p.c_str(), RTLD_NOW); }
static void* get_sym(LibHandle h, const char* n) { return dlsym(h, n); }
static void close_lib(LibHandle h) { dlclose(h); }
#endif

// 宿主内部保存命令用的结构。
// 这里可以用 std::string，因为它只在宿主内部使用，不跨动态库。
struct CommandEntry {
    std::string name;
    std::string help;
    CommandFn run;
};

// 命令表：键是命令名，值是命令本身。
// std::map 是标准库的键值表，按名字查找很快。
static std::map<std::string, CommandEntry> g_commands;

// 插件调用 register_command 时，实际执行的是这个函数。
// 它收到的是插件里的 PluginCommand，里面是 C 风格字符串。
static void host_register_command(const PluginCommand* cmd) {
    // 基本检查：名字和执行函数都不能为空。
    if (!cmd || !cmd->name || !cmd->run) return;

    CommandEntry entry;
    // 把 const char* 赋给 std::string，std::string 会自己复制一份内容。
    // 这样即使插件后来被卸载，表里的名字仍然有效。
    entry.name = cmd->name;
    entry.help = cmd->help ? cmd->help : "";
    entry.run = cmd->run;

    g_commands[entry.name] = entry;

    std::printf("registered command: %s\n", cmd->name);
}

// 插件通过这个函数写日志。
// 宿主可以统一加时间戳、写文件、按插件过滤，这里只打印到屏幕。
static void host_log_info(const char* message) {
    std::printf("[host] %s\n", message ? message : "");
}

int main() {
#ifdef _WIN32
    SetConsoleOutputCP(CP_UTF8);
#endif

    // 准备工具箱。
    // PluginApi api{} 会把所有字段先清零，避免忘记赋值时留下垃圾。
    PluginApi api{};
    api.size = sizeof(PluginApi);       // 我这个结构体有多大
    api.version = PLUGIN_API_VERSION;   // 契约版本
    api.register_command = host_register_command;
    api.log_info = host_log_info;

    std::vector<LibHandle> loaded;

    for (const auto& entry : std::filesystem::directory_iterator("plugins")) {
#ifdef _WIN32
        if (entry.path().extension() != ".dll") continue;
#else
        if (entry.path().extension() != ".so") continue;
#endif
        LibHandle h = open_lib(entry.path().string());
        if (!h) continue;

        // 取初始化函数。它现在接收一个 PluginApi 指针。
        auto init = (int(*)(const PluginApi*))get_sym(h, "plugin_init");
        if (!init) {
            close_lib(h);
            continue;
        }

        // 把工具箱递过去。
        // 插件在里面调用 register_command，命令就进了 g_commands。
        if (init(&api) != 0) {
            close_lib(h);
            continue;
        }

        loaded.push_back(h);
    }

    // 模拟用户输入 hello：查表，找到就调用。
    auto it = g_commands.find("hello");
    if (it != g_commands.end()) {
        it->second.run("示例参数");
    }

    // 卸载插件。
    for (auto h : loaded) {
        auto shut = (void(*)())get_sym(h, "plugin_shutdown");
        if (shut) shut();
        close_lib(h);
    }
    return 0;
}
