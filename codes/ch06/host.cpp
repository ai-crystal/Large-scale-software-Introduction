// 第 6 章：宿主
//
// 在第 5 章的命令循环上继续：
//   - 命令表还在，help / hello / note 仍然照常工作
//   - 新增一个 save 命令，由宿主注册
//   - save 执行时：先走钩子改内容，再“写文件”，最后发 file.saved 事件
//   - 插件订阅事件，收到后各自处理
//
// 这样读者能看到：事件不是凭空出现的，它挂在一条具体的命令上。

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

static CommandTable g_table;              // 命令表
static EventBus g_events;                 // 新增的事件总线
static std::string g_current_plugin;      // 当前插件：加载时或执行命令时
static std::vector<LibHandle> g_loaded;
static std::vector<std::string> g_loaded_names;

// 保存前的钩子链，只在宿主内部使用
static std::vector<std::function<bool(std::string&)>> g_before_save;

// 插件注册命令时回调这里（第 5 章的逻辑）
static void host_register_command(const PluginCommand* cmd) {
    if (!cmd || !cmd->name || !cmd->run) return;
    Command command;
    command.name = cmd->name;
    command.help = cmd->help ? cmd->help : "";
    command.run = cmd->run;
    command.owner = g_current_plugin;
    g_table.add(command);
}

// 插件订阅事件时回调这里（这一章新增）
static void host_on_event(const char* type, EventFn fn) {
    g_events.on(type ? type : "", g_current_plugin, fn);
}

// 插件写日志时回调这里
static void host_log(const char* message) {
    std::printf("[%s] %s\n", g_current_plugin.c_str(), message ? message : "");
    std::fflush(stdout);
}

// 宿主命令：列出所有命令
static void run_help(const char*) {
    g_table.list();
}

// 宿主命令：保存
// 这是这一章的主线：一条普通命令，执行到一半时发出事件。
static void run_save(const char*) {
    // 模拟“当前文档”的内容。真实项目里从文档对象取。
    std::string content = "第一行\n第二行\n";

    // 1. 保存前的钩子：可以改内容，也可以阻止保存
    for (auto& hook : g_before_save) {
        if (!hook(content)) {
            std::printf("保存被钩子阻止\n");
            return;
        }
    }

    // 2. 写文件。这里用打印代替，重点在顺序。
    std::printf("写入文件，内容如下：\n%s", content.c_str());
    std::fflush(stdout);

    // 3. 写完之后，通知所有订阅了 file.saved 的插件
    g_events.emit("file.saved", "path=/notes/a.md");
}

// 扫描 plugins 目录，加载插件
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

// 卸载所有插件
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

    // 宿主自己的命令，owner 是 core
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

    // 宿主的保存前钩子：在内容开头加一行注释
    g_before_save.push_back([](std::string& content) {
        content = "// 由宿主添加\n" + content;
        return true;
    });

    load_all_plugins();

    // 第 5 章的命令循环，原样保留
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

        // 命令执行期间，当前插件设成命令的主人，日志和事件归属才对
        g_current_plugin = cmd->owner;
        cmd->run(args.c_str());
        g_current_plugin.clear();
    }

    unload_all_plugins();
    return 0;
}
