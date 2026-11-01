// 第 5 章：宿主
//
// 和第 4 章相比，多了三件事：
//   1. 命令表有了 owner，注册时自动记下是哪个插件
//   2. 有了一个真正的命令循环：读一行、切名字、查表、执行
//   3. 退出时按 owner 逐个插件清理
//
// 加载和卸载被提取成两个函数，方便对照书里的七步流程。

#include "plugin_api.h"
#include "registry.h"

#include <cstdio>
#include <filesystem>
#include <iostream>
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

// 命令表放在文件级，因为 run_help 需要访问它。
// 函数指针不能携带上下文，只能通过全局变量找到表。
static CommandTable g_table;

// 正在初始化的插件名。
// 插件调用 register_command 时，宿主用它给命令填 owner。
static std::string g_current_plugin;

// 已经加载成功的动态库和它们对应的插件名，退出时用。
static std::vector<LibHandle> g_loaded;
static std::vector<std::string> g_loaded_names;

// 插件调用 register_command 时执行这里。
static void host_register_command(const PluginCommand* cmd) {
    if (!cmd || !cmd->name || !cmd->run) return;

    Command command;
    command.name = cmd->name;                       // std::string 会复制内容
    command.help = cmd->help ? cmd->help : "";
    command.run = cmd->run;
    command.owner = g_current_plugin;               // 关键：自动填归属
    g_table.add(command);
}

// 插件通过它写日志。
static void host_log_info(const char* message) {
    std::printf("[%s] %s\n", g_current_plugin.c_str(), message ? message : "");
}

// 宿主自己的 help 命令。
// 它需要访问 g_table，所以表必须放在文件级。
static void run_help(const char*) {
    g_table.list();
}

// 扫描 plugins 目录，加载每个动态库，调用 plugin_init。
static void load_all_plugins() {
    // 工具箱：两个函数指针 + 大小和版本。
    PluginApi api{};
    api.size = sizeof(PluginApi);
    api.version = PLUGIN_API_VERSION;
    api.register_command = host_register_command;
    api.log_info = host_log_info;

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

        // 先记下名字，插件在 init 里注册命令时，owner 就用它。
        g_current_plugin = name();

        if (init(&api) != 0) {
            // 初始化失败：把已经注册的命令撤掉，避免留下半个插件。
            std::printf("插件初始化失败：%s\n", g_current_plugin.c_str());
            g_table.remove_owner(g_current_plugin);
            close_lib(h);
            continue;
        }

        g_loaded.push_back(h);
        g_loaded_names.push_back(g_current_plugin);
    }

    // 加载结束，清空“当前插件”，避免后续误用。
    g_current_plugin.clear();
}

// 停止所有插件：先调用各自的 shutdown，再按 owner 删命令。
static void unload_all_plugins() {
    // 反向遍历：最后加载的最先卸载。
    for (size_t i = g_loaded.size(); i-- > 0; ) {
        auto shut = (void(*)())get_sym(g_loaded[i], "plugin_shutdown");
        if (shut) shut();
        close_lib(g_loaded[i]);
        g_table.remove_owner(g_loaded_names[i]);
    }
    g_loaded.clear();
    g_loaded_names.clear();
}

int main() {
#ifdef _WIN32
    SetConsoleOutputCP(CP_UTF8);
#endif

    // 宿主自己的命令，owner 写成 core，卸载插件时不会误删。
    Command help;
    help.name = "help";
    help.help = "列出所有命令";
    help.owner = "core";
    help.run = run_help;
    g_table.add(help);

    load_all_plugins();

    // 命令循环：读一行，第一个词是命令名，后面是参数。
    std::string line;
    while (true) {
        std::printf("> ");
        std::fflush(stdout);

        if (!std::getline(std::cin, line)) break;

        // Windows 管道输入可能带 \r，去掉行尾空白。
        while (!line.empty() && (line.back() == '\r' || line.back() == ' ')) {
            line.pop_back();
        }
        if (line == "quit") break;
        if (line.empty()) continue;

        // 按第一个空格切成命令名和参数。
        size_t space = line.find(' ');
        std::string name = space == std::string::npos ? line : line.substr(0, space);
        std::string args = space == std::string::npos ? "" : line.substr(space + 1);

        const Command* cmd = g_table.find(name);
        if (!cmd) {
            std::printf("未知命令：%s（输入 help 查看）\n", name.c_str());
            continue;
        }

        // 调用插件注册的函数。args.c_str() 只在调用期间有效。
        cmd->run(args.c_str());
    }

    unload_all_plugins();
    return 0;
}
