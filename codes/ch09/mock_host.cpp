// 第 9 章：假宿主
//
// 这是一个很小的程序，只做一件事：
// 加载指定的插件，把它注册的命令打印出来。
//
// 它不启动界面、不读配置、不连网络，几秒钟就能跑完。
// 插件作者用它验证“插件能不能被加载、命令有没有注册上”，
// 不用每次都启动完整的主程序。
//
// 用法：
//   mock_host <插件路径>
// 例如：
//   mock_host build/plugins/hello_plugin.dll

#include "plugin_api.h"

#include <cstdio>
#include <string>

#ifdef _WIN32
#include <windows.h>
#define LIB_OPEN(p) LoadLibraryA(p)
#define LIB_SYM(h, n) ((void*)GetProcAddress(h, n))
#else
#include <dlfcn.h>
#define LIB_OPEN(p) dlopen(p, RTLD_NOW)
#define LIB_SYM(h, n) dlsym(h, n)
#endif

// 插件注册命令时，回调到这里。
static void on_command(const PluginCommand* cmd) {
    std::printf("  命令: %-10s %s\n", cmd->name, cmd->help ? cmd->help : "");
}

// 插件写日志时，回调到这里。
static void on_log(const char* message) {
    std::printf("  日志: %s\n", message ? message : "");
}

int main(int argc, char** argv) {
#ifdef _WIN32
    SetConsoleOutputCP(CP_UTF8);
#endif

    // argc 是参数个数，argv[1] 是插件路径。
    if (argc < 2) {
        std::printf("用法: mock_host <plugin.dll>\n");
        return 1;
    }

    auto handle = LIB_OPEN(argv[1]);
    if (!handle) {
        std::printf("加载失败: %s\n", argv[1]);
        return 2;
    }

    // 取初始化函数。
    auto init = (int(*)(const PluginApi*))LIB_SYM(handle, "plugin_init");
    if (!init) {
        std::printf("缺少 plugin_init\n");
        return 3;
    }

    // 准备一个最小工具箱。
    // 命令注册和日志都指向上面的打印函数。
    PluginApi api{};
    api.size = sizeof(PluginApi);
    api.version = PLUGIN_API_VERSION;
    api.register_command = on_command;
    api.log_info = on_log;

    std::printf("加载 %s\n", argv[1]);
    int rc = init(&api);
    std::printf("init 返回 %d\n", rc);

    // 返回非零表示插件初始化失败，测试脚本可以据此判断。
    return rc;
}
