#ifdef _WIN32
#include <windows.h>
#endif

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
static std::vector<std::function<bool(std::string&)>> g_before_save;

static void host_register_command(const PluginCommand* cmd) {
    if (!cmd || !cmd->name || !cmd->run) return;
    Command command;
    command.name = cmd->name;
    command.help = cmd->help ? cmd->help : "";
    command.run = cmd->run;
    command.owner = g_current_plugin;
    g_table.add(command);
}

static void host_on_event(const char* type, void (*fn)(const char*, const char*)) {
    g_events.on(type ? type : "", g_current_plugin, fn);
}

static void host_log(const char* message) {
    std::printf("[%s] %s\n", g_current_plugin.c_str(), message ? message : "");
}

static void run_help(const char*) {
    g_table.list();
}

static void run_save(const char*) {
    std::string content = "第一行\n第二行\n";
    for (auto& hook : g_before_save) {
        if (!hook(content)) {
            std::printf("保存被钩子阻止\n");
            return;
        }
    }
    std::printf("保存内容：\n%s", content.c_str());
    g_events.emit("file.saved", "path=/notes/a.md");
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
    save.help = "演示保存钩子与事件";
    save.owner = "core";
    save.run = run_save;
    g_table.add(save);

    // 宿主自己的钩子：保存前加一行注释
    g_before_save.push_back([](std::string& content) {
        content = "// 由宿主添加\n" + content;
        return true;
    });

    PluginApi api{};
    api.size = sizeof(PluginApi);
    api.version = PLUGIN_API_VERSION;
    api.register_command = host_register_command;
    api.on_event = host_on_event;
    api.log_info = host_log;

    std::vector<LibHandle> loaded;
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
        if (!name || !init) { close_lib(h); continue; }
        g_current_plugin = name();
        if (init(&api) != 0) {
            std::printf("插件初始化失败：%s\n", g_current_plugin.c_str());
            g_table.remove_owner(g_current_plugin);
            g_events.remove_owner(g_current_plugin);
            close_lib(h);
            continue;
        }
        loaded.push_back(h);
    }
    g_current_plugin.clear();

    std::string line;
    while (true) {
        std::printf("> ");
        std::fflush(stdout);
        if (!std::getline(std::cin, line)) break;
        while (!line.empty() && (line.back() == '\r' || line.back() == ' ')) line.pop_back();
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
        cmd->run(args.c_str());
    }

    for (auto it = loaded.rbegin(); it != loaded.rend(); ++it) {
        auto shut = (void(*)())get_sym(*it, "plugin_shutdown");
        if (shut) shut();
        close_lib(*it);
    }
    return 0;
}
