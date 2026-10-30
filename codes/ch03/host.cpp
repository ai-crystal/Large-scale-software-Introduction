// 第 3 章的宿主：扫描 plugins 目录，加载动态库，调用三个函数
#ifdef _WIN32
#include <windows.h>
#endif

#include <cstdio>
#include <filesystem>
#include <string>
#include <vector>

#ifdef _WIN32
#include <windows.h>
using LibHandle = HMODULE;
static LibHandle open_lib(const std::string& p) { return LoadLibraryA(p.c_str()); }
static void* get_sym(LibHandle h, const char* n) { return (void*)GetProcAddress(h, n); }
static void close_lib(LibHandle h) { FreeLibrary(h); }
#else
#include <dlfcn.h>
using LibHandle = void*;
static LibHandle open_lib(const std::string& p) { return dlopen(p.c_str(), RTLD_NOW); }
static void* get_sym(LibHandle h, const char* n) { return dlsym(h, n); }
static void close_lib(LibHandle h) { dlclose(h); }
#endif

int main() {
#ifdef _WIN32
    SetConsoleOutputCP(CP_UTF8);
#endif

    std::vector<LibHandle> loaded;

    for (const auto& entry : std::filesystem::directory_iterator("plugins")) {
#ifdef _WIN32
        if (entry.path().extension() != ".dll") continue;
#else
        if (entry.path().extension() != ".so") continue;
#endif
        LibHandle h = open_lib(entry.path().string());
        if (!h) {
            std::printf("load failed: %s\n", entry.path().string().c_str());
            continue;
        }

        auto name = (const char*(*)())get_sym(h, "plugin_name");
        auto init = (int(*)())get_sym(h, "plugin_init");
        if (!name || !init) {
            std::printf("missing symbols\n");
            close_lib(h);
            continue;
        }

        std::printf("loaded %s\n", name());
        std::fflush(stdout);
        init();
        loaded.push_back(h);
    }

    for (auto h : loaded) {
        auto shut = (void(*)())get_sym(h, "plugin_shutdown");
        if (shut) shut();
        close_lib(h);
    }
    return 0;
}
