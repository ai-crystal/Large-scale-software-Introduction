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
} PluginApi;

PLUGIN_EXPORT const char* plugin_name();
PLUGIN_EXPORT int plugin_init(const PluginApi* api);
PLUGIN_EXPORT void plugin_shutdown();

}
