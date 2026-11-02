// 第 6 章（第一阶段）：宿主
//
// 命令循环和命令表来自第 5 章。
// 这一阶段只加事件：save 写完之后广播 file.saved，插件收到后各自处理。
// 钩子（保存前改内容）在第二阶段 codes/ch06-2 才加入。

#include "plugin_api.h"
#include "registry.h"
#include "events.h"

#include <cstdio>
#include <filesystem>
#include <iostream>
#include <string>
#include <vector>

#ifdef _WIN32
#include <windows.h>
#endif

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

static CommandTable g_table;
static EventBus g_events;
static std::string g_current_plugin;
static std::vector<LibHandle> g_loaded;
static std::vector<std::string> g_loaded_names;

// 插件注册命令
static void host_register_command(const PluginCommand* cmd) {
    if (!cmd || !cmd->name || !cmd->run) return;
    Command command;
    command.name = cmd->name;
    command.help = cmd->help ? cmd->help : "";
    command.run = cmd->run;
    command.owner = g_current_plugin;
    g_table.add(command);
}

// 插件订阅事件
static void host_on_event(const char* type, EventFn fn) {
    g_events.on(type ? type : "", g_current_plugin, fn);
}

// 插件写日志
static void host_log(const char* message) {
    std::printf("[%s] %s\n", g_current_plugin.c_str(), message ? message : "");
    std::fflush(stdout);
}

// 宿主命令：列出所有命令
static void run_help(const char*) {
    g_table.list();
}

// 宿主命令：保存
// 这一阶段没有钩子，流程只有两步：写文件，发事件。
static void run_save(const char*) {
    std::string content = "第一行\n第二行\n";

    // 1. 写文件（这里用打印代替）
    std::printf("写入文件，内容如下：\n%s", content.c_str());
    std::fflush(stdout);

    // 2. 通知订阅者
    g_events.emit("file.saved", "path=/notes/a.md");
}

// 加载插件
static void load_all_plugins() {
    PluginApi api{};
    api.size = sizeof(PluginApi);
    api.version = PLUGIN_API_VERSION;
    api.register_command = host_register_command;
    api.log_info = host_log;
    api.on_event = host_on_event;

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
}

// 卸载插件：清命令和事件订阅
static void unload_all_plugins() {
    for (size_t i = g_loaded.size(); i-- > 0; ) {
        auto shut = (void(*)())get_sym(g_loaded[i], "plugin_shutdown");
        if (shut) shut();
        close_lib(g_loaded[i]);

        g_table.remove_owner(g_loaded_names[i]);
        g_events.remove_owner(g_loaded_names[i]);
    }
    g_loaded.clear();
    g_loaded_names.clear();
}

int main() {
#ifdef _WIN32
    SetConsoleOutputCP(CP_UTF8);
#endif

    Command help;
    help.name = "help";
    help.help = "列出所有命令";
    help.owner = "core";
    help.run = run_help;
    g_table.add(help);

    Command save;
    save.name = "save";
    save.help = "保存并通知插件";
    save.owner = "core";
    save.run = run_save;
    g_table.add(save);

    load_all_plugins();

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

        size_t space = line.find(' ');
        std::string name = space == std::string::npos ? line : line.substr(0, space);
        std::string args = space == std::string::npos ? "" : line.substr(space + 1);

        const Command* cmd = g_table.find(name);
        if (!cmd) {
            std::printf("未知命令：%s（输入 help 查看）\n", name.c_str());
            continue;
        }

        g_current_plugin = cmd->owner;
        cmd->run(args.c_str());
        g_current_plugin.clear();
    }

    unload_all_plugins();
    return 0;
}
