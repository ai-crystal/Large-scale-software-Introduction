#include "plugin_api.h"
#include "registry.h"
#include <cstdio>
#include <filesystem>
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
static std::string g_current_plugin;

static void host_register_command(const PluginCommand* cmd) {
    if (!cmd || !cmd->name || !cmd->run) return;
    Command command;
    command.name = cmd->name;
    command.help = cmd->help ? cmd->help : "";
    command.run = cmd->run;
    command.owner = g_current_plugin;
    g_table.add(command);
}

static void host_log_info(const char* message) {
    std::printf("[%s] %s\n", g_current_plugin.c_str(), message ? message : "");
}

static void run_help(const char*) {
    g_table.list();
}

int main() {
    Command help;
    help.name = "help";
    help.help = "列出所有命令";
    help.owner = "core";
    help.run = run_help;
    g_table.add(help);

    PluginApi api{};
    api.size = sizeof(PluginApi);
    api.version = PLUGIN_API_VERSION;
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

        auto name = (const char*(*)())get_sym(h, "plugin_name");
        auto init = (int(*)(const PluginApi*))get_sym(h, "plugin_init");
        if (!name || !init) { close_lib(h); continue; }

        g_current_plugin = name();
        if (init(&api) != 0) {
            std::printf("插件初始化失败：%s\n", g_current_plugin.c_str());
            g_table.remove_owner(g_current_plugin);
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
        while (!line.empty() && (line.back() == '' || line.back() == ' ')) line.pop_back();
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
    g_table.remove_owner("hello");
    g_table.remove_owner("notes");
    return 0;
}
