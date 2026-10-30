#include "plugin_api.h"
#include "events.h"
#include <cstdio>
#include <filesystem>
#include <functional>
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

static EventBus g_events;
static std::string g_current_plugin;
static std::vector<std::function<bool(std::string&)>> g_before_save;

static void host_on_event(const char* type, void (*fn)(const char*, const char*)) {
    g_events.on(type ? type : "", g_current_plugin, fn);
}

static void host_log(const char* message) {
    std::printf("[%s] %s\n", g_current_plugin.c_str(), message ? message : "");
}

static void host_register_command(const PluginCommand* cmd) {
    if (cmd && cmd->name) {
        std::printf("注册命令：%s（来自 %s）\n", cmd->name, g_current_plugin.c_str());
    }
}

int main() {
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
        if (init(&api) != 0) { close_lib(h); continue; }
        loaded.push_back(h);
    }
    g_current_plugin.clear();

    // 宿主自己的钩子：保存前给内容加一行注释
    g_before_save.push_back([](std::string& content) {
        content = "// 由宿主在保存前添加\n" + content;
        return true;
    });

    std::string content = "hello world\n";
    for (auto& hook : g_before_save) {
        if (!hook(content)) {
            std::printf("保存被钩子阻止\n");
            return 1;
        }
    }
    std::printf("保存内容：\n%s", content.c_str());

    g_events.emit("file.saved", "path=/notes/a.md");

    for (auto it = loaded.rbegin(); it != loaded.rend(); ++it) {
        auto shut = (void(*)())get_sym(*it, "plugin_shutdown");
        if (shut) shut();
        close_lib(*it);
    }
    return 0;
}
