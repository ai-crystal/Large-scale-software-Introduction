// 第 6 章：插件接口（带事件订阅）
//
// 在上一章的基础上，PluginApi 多了一个 on_event：
// 插件用它告诉宿主“某个事件发生时，调用我这个函数”。

#pragma once

#include <cstdint>

#ifdef _WIN32
#define PLUGIN_EXPORT __declspec(dllexport)
#else
#define PLUGIN_EXPORT __attribute__((visibility("default")))
#endif

#define PLUGIN_API_VERSION 1

extern "C" {

// 命令和之前一样：接收参数串，不返回值。
typedef void (*CommandFn)(const char* args);

// 事件回调：接收事件类型和数据，不返回值。
// type 是事件名，比如 "file.saved"；payload 是附加信息。
typedef void (*EventFn)(const char* type, const char* payload);

typedef struct PluginCommand {
    const char* name;
    const char* help;
    CommandFn run;
} PluginCommand;

typedef struct PluginApi {
    uint32_t size;
    uint32_t version;
    void (*register_command)(const PluginCommand* cmd);

    // 订阅事件：type 是事件名，fn 是事件发生时调用的函数。
    void (*on_event)(const char* type, EventFn fn);

    void (*log_info)(const char* message);
} PluginApi;

PLUGIN_EXPORT const char* plugin_name();
PLUGIN_EXPORT int plugin_init(const PluginApi* api);
PLUGIN_EXPORT void plugin_shutdown();

}
