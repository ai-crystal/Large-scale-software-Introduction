// 第 6 章：notes 插件
//
// 第二个插件，用来证明命令表仍然是主线：
// hello 插件注册 hello 命令，notes 插件注册 note 命令，
// 两个命令都能在同一个循环里被调用。
// notes 不订阅事件，保存时它不会被通知。

#include "plugin_api.h"

#include <cstdio>
#include <cstring>

static void run_note(const char* args) {
    std::printf("note: %s\n", args ? args : "（空）");
    std::fflush(stdout);
}

static const PluginCommand kCommands[] = {
    { "note", "记录一句话", run_note },
};

extern "C" PLUGIN_EXPORT const char* plugin_name() {
    return "notes";
}

// 钩子函数：在内容末尾追加一行 HTML 注释。
// buffer 是宿主的可写缓冲区，size 是总容量。
// 返回 0 继续，返回非 0 阻止保存。
static int before_save(char* buffer, std::size_t size, const char* meta) {
    (void)meta;   // 这个钩子用不到附加信息

    const char* tail = "\n<!-- finish by save -->\n";
    std::size_t used = std::strlen(buffer);
    std::size_t need = std::strlen(tail);

    // 放不下就返回非 0，让宿主中止保存，而不是写出半截内容。
    if (used + need + 1 > size) {
        return 1;
    }

    std::strcat(buffer, tail);
    return 0;
}

extern "C" PLUGIN_EXPORT int plugin_init(const PluginApi* api) {
    if (!api || api->version != PLUGIN_API_VERSION) return 1;

    for (const auto& cmd : kCommands) {
        api->register_command(&cmd);
    }

    // 往宿主预留的 before_save 插槽上挂函数
    if (api->register_hook) {
        api->register_hook("before_save", before_save);
    }

    if (api->log_info) {
        api->log_info("notes 插件已加载");
    }
    return 0;
}

extern "C" PLUGIN_EXPORT void plugin_shutdown() {
}
