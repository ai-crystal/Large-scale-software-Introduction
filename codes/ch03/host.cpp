// 第 3 章：宿主
//
// 宿主做四件事：
//   1. 扫描 plugins 目录，找到动态库
//   2. 打开动态库，拿到一个“把手”
//   3. 按名字取出三个导出函数
//   4. 调用初始化，最后调用清理
//
// 这是全书的第一个插件加载器。它还没有版本检查、没有注册命令、
// 没有隔离，但已经能证明“不重新编译主程序也能加功能”。

#include <cstdio>
#include <filesystem>   // C++17 的文件系统：遍历目录
#include <string>
#include <vector>

#ifdef _WIN32
#include <windows.h>
#endif

// 两个平台加载动态库的函数名不一样，用一个统一的把手类型包起来，
// 后面的代码就不用到处写 #ifdef。
#ifdef _WIN32
using LibHandle = HMODULE;   // Windows 的动态库把手
// LoadLibraryA：按路径加载 DLL，失败返回空
static LibHandle open_lib(const std::string& p) { return LoadLibraryA(p.c_str()); }
// GetProcAddress：按名字取函数地址
static void* get_sym(LibHandle h, const char* n) { return (void*)GetProcAddress(h, n); }
// FreeLibrary：卸载 DLL
static void close_lib(LibHandle h) { FreeLibrary(h); }
#else
using LibHandle = void*;     // Linux 的动态库把手
// dlopen：加载 .so，RTLD_NOW 表示现在就解析所有符号
static LibHandle open_lib(const std::string& p) { return dlopen(p.c_str(), RTLD_NOW); }
// dlsym：按名字取函数地址
static void* get_sym(LibHandle h, const char* n) { return dlsym(h, n); }
// dlclose：卸载 .so
static void close_lib(LibHandle h) { dlclose(h); }
#endif

int main() {
#ifdef _WIN32
    SetConsoleOutputCP(CP_UTF8);   // 中文输出用 UTF-8
#endif

    // 记录已经加载成功的库，退出时统一卸载。
    // 卸载顺序通常是后进先出，所以最后用反向遍历。
    std::vector<LibHandle> loaded;

    // 遍历 plugins 目录下的每一个条目。
    for (const auto& entry : std::filesystem::directory_iterator("plugins")) {
        // 只处理动态库：Windows 看 .dll，Linux 看 .so。
#ifdef _WIN32
        if (entry.path().extension() != ".dll") continue;
#else
        if (entry.path().extension() != ".so") continue;
#endif

        // 打开动态库。失败就跳过，不中断其他插件。
        LibHandle h = open_lib(entry.path().string());
        if (!h) {
            std::printf("load failed: %s\n", entry.path().string().c_str());
            continue;
        }

        // 取两个必需的函数。
        // 这里的类型写法 (const char*(*)()) 是一个函数指针：
        // 指向“不接收参数、返回 const char*”的函数。
        auto name = (const char*(*)())get_sym(h, "plugin_name");
        auto init = (int(*)())get_sym(h, "plugin_init");

        // 缺任何一个都说明这不是一个合法的插件，关掉它。
        if (!name || !init) {
            std::printf("missing symbols\n");
            close_lib(h);
            continue;
        }

        // 先打印名字，再初始化，能看出加载顺序。
        std::printf("loaded %s\n", name());
        std::fflush(stdout);
        init();

        // 记下来，退出时统一清理。
        loaded.push_back(h);
    }

    // 反向遍历：最后加载的最先卸载。
    for (auto h : loaded) {
        // plugin_shutdown 是可选的，取不到就跳过。
        auto shut = (void(*)())get_sym(h, "plugin_shutdown");
        if (shut) shut();
        close_lib(h);
    }

    return 0;
}
