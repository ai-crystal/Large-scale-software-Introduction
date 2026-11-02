// 第 6 章（第一阶段）：插件接口，只有事件订阅
//
// 相比第 5 章，PluginApi 末尾多了一个 on_event。
// 钩子相关的 register_hook 在第二阶段（codes/ch06-2）才加入。

#pragma once

#include <cstdint>

#ifdef _WIN32
#define PLUGIN_EXPORT __declspec(dllexport)
#else
#define PLUGIN_EXPORT __attribute__((visibility("default")))
#endif

#define PLUGIN_API_VERSION 1

extern "C" {

typedef void (*CommandFn)(const char* args);
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
    void (*log_info)(const char* message);

    // 订阅事件：type 是事件名，fn 是事件发生时调用的函数
    void (*on_event)(const char* type, EventFn fn);
} PluginApi;

PLUGIN_EXPORT const char* plugin_name();
PLUGIN_EXPORT int plugin_init(const PluginApi* api);
PLUGIN_EXPORT void plugin_shutdown();

}
