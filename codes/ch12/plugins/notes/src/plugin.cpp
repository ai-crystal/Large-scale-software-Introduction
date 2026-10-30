#include "plugin_api.h"
#include <cstdio>

static void run_note(const char* args) {
    std::printf("note: %s\n", args ? args : "（空）");
    std::fflush(stdout);
}

static const PluginCommand kCommands[] = {
    { "note", "记录一句话", run_note },
};

extern "C" PLUGIN_EXPORT const char* plugin_name() { return "notes"; }

extern "C" PLUGIN_EXPORT int plugin_init(const PluginApi* api) {
    if (!api || api->version != PLUGIN_API_VERSION) return 1;
    for (const auto& cmd : kCommands) api->register_command(&cmd);
    return 0;
}

extern "C" PLUGIN_EXPORT void plugin_shutdown() {}
