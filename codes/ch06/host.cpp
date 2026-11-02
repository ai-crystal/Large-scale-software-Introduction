// 第 6 章：宿主
//
// 命令循环和命令表来自第 5 章。这一章增加两样东西：
//   1. 事件总线：save 完成后广播 file.saved
//   2. 钩子链：save 写文件之前，调用插件挂上来的函数
//
// 插件既可以通过 on_event 订阅事件，也可以通过 register_hook 挂到
// before_save 这个插槽上。两条路径的用途不同：钩子改数据，事件做通知。

#include "plugin_api.h"
#include "registry.h"
#include "events.h"

#include <cstdio>
#include <filesystem>
#include <functional>
#include <iostream>
#include <map>
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

static CommandTable g_table;
static EventBus g_events;
static std::string g_current_plugin;
static std::vector<LibHandle> g_loaded;
static std::vector<std::string> g_loaded_names;

// 钩子链：插槽名 -> 挂在上面的函数
struct HookEntry {
    std::string owner;
    HookFn fn;
};

static std::map<std::string, std::vector<HookEntry>> g_hooks;

// 宿主自己的保存前钩子，和插件钩子分开演示
static std::vector<std::function<bool(std::string&)>> g_before_save;

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

// 插件挂钩子
static int host_register_hook(const char* name, HookFn fn) {
    if (!name || !fn) return 1;
    g_hooks[name].push_back({ g_current_plugin, fn });
    return 0;
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
static void run_save(const char*) {
    std::string content = "第一行\n第二行\n";

    // 1. 插件钩子：宿主准备一块可写缓冲区，插件直接在里面改。
    //    多留 4096 字节，让插件有空间追加内容。
    std::vector<char> buffer(content.begin(), content.end());
    buffer.resize(content.size() + 4096, '\0');

    auto it = g_hooks.find("before_save");
    if (it != g_hooks.end()) {
        for (const auto& hook : it->second) {
            int rc = hook.fn(buffer.data(), buffer.size(), "path=/notes/a.md");
            if (rc != 0) {
                std::printf("插件 %s 阻止了保存\n", hook.owner.c_str());
                return;
            }
        }
    }

    // 把插件改过的缓冲区读回字符串。
    // assign 遇到 \0 停止，文本内容够用。
    content.assign(buffer.data());

    // 2. 宿主自己的钩子：改的是 std::string，只在宿主内部使用。
    for (auto& hook : g_before_save) {
        if (!hook(content)) {
            std::printf("宿主钩子阻止了保存\n");
            return;
        }
    }

    // 3. 写文件（这里用打印代替）
    std::printf("写入文件，内容如下：\n%s", content.c_str());
    std::fflush(stdout);

    // 4. 通知订阅者
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
    api.register_hook = host_register_hook;

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

// 卸载插件：命令、事件、钩子都要按 owner 清掉
static void unload_all_plugins() {
    for (size_t i = g_loaded.size(); i-- > 0; ) {
        auto shut = (void(*)())get_sym(g_loaded[i], "plugin_shutdown");
        if (shut) shut();
        close_lib(g_loaded[i]);

        const std::string& owner = g_loaded_names[i];
        g_table.remove_owner(owner);
        g_events.remove_owner(owner);

        for (auto& pair : g_hooks) {
            auto& list = pair.second;
            for (auto it = list.begin(); it != list.end(); ) {
                if (it->owner == owner) it = list.erase(it);
                else ++it;
            }
        }
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

    // 宿主自己的钩子：在内容开头加一行注释。
    // 它和插件钩子做类似的事，用来对比两种写法。
    g_before_save.push_back([](std::string& content) {
        content = "// 由宿主添加\n" + content;
        return true;
    });

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
