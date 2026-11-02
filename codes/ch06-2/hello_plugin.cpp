// 第 6 章（第二阶段）：hello 插件
//
// 这个插件同时演示两种能力：
//   1. 注册 hello 命令（第 5 章）
//   2. 订阅 file.saved 事件，并往 before_save 插槽上挂一个钩子
//
// 钩子函数直接改宿主给的缓冲区，在内容末尾加一行标记。

#include "plugin_api.h"

#include <cstdio>
#include <cstring>

static const PluginApi* g_api = nullptr;

// 事件处理函数：保存完成后打印一行
static void on_saved(const char* type, const char* payload) {
    std::printf("[hello] 收到事件 %s：%s\n", type, payload ? payload : "");
    std::fflush(stdout);
}

// 钩子函数：在内容末尾追加一行 HTML 注释。
// buffer 是宿主的可写缓冲区，size 是总容量。
// 返回 0 继续，返回非 0 阻止保存。
static int before_save(char* buffer, std::size_t size, const char* meta) {
    (void)meta;   // 这个钩子用不到附加信息

    const char* tail = "\n<!-- saved by hello -->\n";
    std::size_t used = std::strlen(buffer);
    std::size_t need = std::strlen(tail);

    // 放不下就返回非 0，让宿主中止保存，而不是写出半截内容。
    if (used + need + 1 > size) {
        return 1;
    }

    std::strcat(buffer, tail);
    return 0;
}

static void run_hello(const char* args) {
    if (g_api && g_api->log_info) {
        g_api->log_info("hello 命令被执行");
    }
    std::printf("你好，世界（参数：%s）\n", args ? args : "");
    std::fflush(stdout);
}

static const PluginCommand kCommands[] = {
    { "hello", "打印一句问候", run_hello },
};

extern "C" PLUGIN_EXPORT const char* plugin_name() {
    return "hello";
}

extern "C" PLUGIN_EXPORT int plugin_init(const PluginApi* api) {
    if (!api || api->version != PLUGIN_API_VERSION) return 1;

    g_api = api;

    for (const auto& cmd : kCommands) {
        api->register_command(&cmd);
    }

    // 往宿主预留的 before_save 插槽上挂函数
    if (api->register_hook) {
        api->register_hook("before_save", before_save);
    }

    api->on_event("file.saved", on_saved);

    if (api->log_info) {
        api->log_info("hello 插件已加载");
    }
    return 0;
}

extern "C" PLUGIN_EXPORT void plugin_shutdown() {
    g_api = nullptr;
}
