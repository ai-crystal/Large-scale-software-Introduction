// 假宿主：加载指定插件，打印它注册的命令，不启动界面
#ifdef _WIN32
#include <windows.h>
#endif

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

static void on_command(const PluginCommand* cmd) {
    std::printf("  命令: %-10s %s\n", cmd->name, cmd->help ? cmd->help : "");
}

static void on_log(const char* message) {
    std::printf("  日志: %s\n", message ? message : "");
}

int main(int argc, char** argv) {
#ifdef _WIN32
    SetConsoleOutputCP(CP_UTF8);
#endif

    if (argc < 2) {
        std::printf("用法: mock_host <plugin.dll>\n");
        return 1;
    }

    auto handle = LIB_OPEN(argv[1]);
    if (!handle) {
        std::printf("加载失败: %s\n", argv[1]);
        return 2;
    }

    auto init = (int(*)(const PluginApi*))LIB_SYM(handle, "plugin_init");
    if (!init) {
        std::printf("缺少 plugin_init\n");
        return 3;
    }

    PluginApi api{};
    api.size = sizeof(PluginApi);
    api.version = PLUGIN_API_VERSION;
    api.register_command = on_command;
    api.log_info = on_log;

    std::printf("加载 %s\n", argv[1]);
    int rc = init(&api);
    std::printf("init 返回 %d\n", rc);
    return rc;
}
