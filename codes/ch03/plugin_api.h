#pragma once

#ifdef _WIN32
#define PLUGIN_EXPORT __declspec(dllexport)
#else
#define PLUGIN_EXPORT __attribute__((visibility("default")))
#endif

extern "C" {
    PLUGIN_EXPORT const char* plugin_name();
    PLUGIN_EXPORT int plugin_init();
    PLUGIN_EXPORT void plugin_shutdown();
}
