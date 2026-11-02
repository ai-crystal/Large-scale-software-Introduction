// 第 6 章：插件接口（事件 + 钩子）
//
// 相比第 5 章，PluginApi 末尾多了两个能力：
//   on_event       订阅事件
//   register_hook  往宿主的流程插槽上挂函数

#pragma once

#include <cstddef>
#include <cstdint>

#ifdef _WIN32
#define PLUGIN_EXPORT __declspec(dllexport)
#else
#define PLUGIN_EXPORT __attribute__((visibility("default")))
#endif

#define PLUGIN_API_VERSION 1

extern "C" {

// 命令和之前一样
typedef void (*CommandFn)(const char* args);

// 事件处理函数：接收类型和数据，不返回值
typedef void (*EventFn)(const char* type, const char* payload);

// 钩子函数：直接改宿主的缓冲区。
// buffer 是可写内存，size 是总容量，meta 是附加信息。
// 返回 0 表示继续，非 0 表示阻止流程。
// 用 char* 而不是 std::string，是因为要跨动态库传递。
typedef int (*HookFn)(char* buffer, std::size_t size, const char* meta);

typedef struct PluginCommand {
    const char* name;
    const char* help;
    CommandFn run;
} PluginCommand;

typedef struct PluginApi {
    uint32_t size;
    uint32_t version;
    void (*register_command)(const PluginCommand* cmd);
    void (*log_info)(const char* message);

    // 订阅事件：type 是事件名，fn 是事件发生时调用的函数
    void (*on_event)(const char* type, EventFn fn);

    // 挂钩子：name 是插槽名，比如 "before_save"
    int (*register_hook)(const char* name, HookFn fn);
} PluginApi;

PLUGIN_EXPORT const char* plugin_name();
PLUGIN_EXPORT int plugin_init(const PluginApi* api);
PLUGIN_EXPORT void plugin_shutdown();

}
