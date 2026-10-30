#include "plugin_api.h"
#include <cstdio>
#include <cstring>
#include <filesystem>
#include <map>
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

struct CommandEntry {
    std::string name;
    std::string help;
    CommandFn run;
};

static std::map<std::string, CommandEntry> g_commands;

static void host_register_command(const PluginCommand* cmd) {
    if (!cmd || !cmd->name || !cmd->run) return;
    CommandEntry entry;
    entry.name = cmd->name;
    entry.help = cmd->help ? cmd->help : "";
    entry.run = cmd->run;
    g_commands[entry.name] = entry;
    std::printf("registered command: %s\n", cmd->name);
}

static void host_log_info(const char* message) {
    std::printf("[host] %s\n", message ? message : "");
}

int main() {
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
        auto init = (int(*)(const PluginApi*))get_sym(h, "plugin_init");
        if (!init || init(&api) != 0) {
            close_lib(h);
            continue;
        }
        loaded.push_back(h);
    }

    auto it = g_commands.find("hello");
    if (it != g_commands.end()) {
        it->second.run("示例参数");
    }

    for (auto h : loaded) {
        auto shut = (void(*)())get_sym(h, "plugin_shutdown");
        if (shut) shut();
        close_lib(h);
    }
    return 0;
}
