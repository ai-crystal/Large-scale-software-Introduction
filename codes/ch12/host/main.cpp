// 第 12 章：完整最小外壳的宿主
//
// 把前面几章拼在一起：
//   第 3、4 章  加载动态库、传 PluginApi
//   第 5 章    命令表、owner、冲突、卸载清理
//   第 6 章    事件总线、钩子
//
// 启动顺序很重要：
//   先声明表 -> 再加载插件 -> 注册宿主命令 -> 进入循环 -> 退出时卸载

#include "plugin_api.h"
#include "registry.h"
#include "events.h"

#include <cstdio>
#include <filesystem>
#include <functional>
#include <iostream>
#include <string>
#include <vector>

#ifdef _WIN32
#include <windows.h>
#endif

// 平台差异封装
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

static CommandTable g_table;                 // 命令表
static EventBus g_events;                    // 事件总线
static std::string g_current_plugin;         // 正在初始化的插件名
static std::vector<LibHandle> g_loaded;      // 已加载的动态库
static std::vector<std::string> g_loaded_names;
static std::vector<std::function<bool(std::string&)>> g_before_save;   // 保存前钩子

// 插件注册命令时，宿主在这里接收。
static void host_register_command(const PluginCommand* cmd) {
    if (!cmd || !cmd->name || !cmd->run) return;

    Command command;
    command.name = cmd->name;
    command.help = cmd->help ? cmd->help : "";
    command.run = cmd->run;
    command.owner = g_current_plugin;    // 自动填归属
    g_table.add(command);
}

// 插件订阅事件时，宿主在这里登记。
static void host_on_event(const char* type, void (*fn)(const char*, const char*)) {
    g_events.on(type ? type : "", g_current_plugin, fn);
}

// 插件写日志时，宿主在这里接收。
static void host_log(const char* message) {
    std::printf("[%s] %s\n", g_current_plugin.c_str(), message ? message : "");
}

// 宿主自己的 help 命令。
static void run_help(const char*) {
    g_table.list();
}

// 宿主自己的 save 命令：先走钩子，再发事件。
static void run_save(const char*) {
    std::string content = "第一行\n第二行\n";

    // 依次执行保存前钩子。任何一个返回 false 就中止。
    for (auto& hook : g_before_save) {
        if (!hook(content)) {
            std::printf("保存被钩子阻止\n");
            return;
        }
    }

    std::printf("保存内容：\n%s", content.c_str());

    // 保存完成，通知订阅者。
    g_events.emit("file.saved", "path=/notes/a.md");
}

int main() {
#ifdef _WIN32
    SetConsoleOutputCP(CP_UTF8);
#endif

    // 先注册宿主自己的命令，owner 写成 core。
    // 这样卸载插件时按 owner 清理，不会误删它们。
    Command help;
    help.name = "help";
    help.help = "列出所有命令";
    help.owner = "core";
    help.run = run_help;
    g_table.add(help);

    Command save;
    save.name = "save";
    save.help = "演示保存钩子与事件";
    save.owner = "core";
    save.run = run_save;
    g_table.add(save);

    // 宿主自己的保存前钩子：在内容前加一行注释。
    g_before_save.push_back([](std::string& content) {
        content = "// 由宿主添加\n" + content;
        return true;
    });

    // 准备工具箱。
    PluginApi api{};
    api.size = sizeof(PluginApi);
    api.version = PLUGIN_API_VERSION;
    api.register_command = host_register_command;
    api.on_event = host_on_event;
    api.log_info = host_log;

    // 加载 plugins 目录下的所有插件。
    for (const auto& entry : std::filesystem::directory_iterator("plugins")) {
#ifdef _WIN32
        if (entry.path().extension() != ".dll") continue;
#else
        if (entry.path().extension() != ".so") continue;
#endif
        LibHandle h = open_lib(entry.path().string());
        if (!h) continue;

        auto name = (const char*(*)())get_sym(h, "plugin_name");
        auto init = (int(*)(const PluginApi*))get_sym(h, "plugin_init");
        if (!name || !init) {
            close_lib(h);
            continue;
        }

        g_current_plugin = name();

        if (init(&api) != 0) {
            // 初始化失败：撤掉它可能已经注册的东西，关掉库。
            std::printf("插件初始化失败：%s\n", g_current_plugin.c_str());
            g_table.remove_owner(g_current_plugin);
            g_events.remove_owner(g_current_plugin);
            close_lib(h);
            continue;
        }

        g_loaded.push_back(h);
        g_loaded_names.push_back(g_current_plugin);
    }
    g_current_plugin.clear();

    // 命令循环。
    std::string line;
    while (true) {
        std::printf("> ");
        std::fflush(stdout);

        if (!std::getline(std::cin, line)) break;

        while (!line.empty() && (line.back() == '\r' || line.back() == ' ')) {
            line.pop_back();
        }
        if (line == "quit") break;
        if (line.empty()) continue;

        // 第一个词是命令名，剩下的是参数。
        size_t space = line.find(' ');
        std::string name = space == std::string::npos ? line : line.substr(0, space);
        std::string args = space == std::string::npos ? "" : line.substr(space + 1);

        const Command* cmd = g_table.find(name);
        if (!cmd) {
            std::printf("未知命令：%s（输入 help 查看）\n", name.c_str());
            continue;
        }
        cmd->run(args.c_str());
    }

    // 退出：反向停用插件，先 shutdown，再按 owner 清理。
    for (size_t i = g_loaded.size(); i-- > 0; ) {
        auto shut = (void(*)())get_sym(g_loaded[i], "plugin_shutdown");
        if (shut) shut();
        close_lib(g_loaded[i]);
        g_table.remove_owner(g_loaded_names[i]);
        g_events.remove_owner(g_loaded_names[i]);
    }

    return 0;
}
