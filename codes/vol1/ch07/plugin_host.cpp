// 第 7 章：插件进程
//
// 启动时先“注册命令”，再进入对话循环。
// 注册消息是普通文本，每行一条：
//   register <命令名> <说明>
// 全部发完后发一行 ready，告诉宿主可以开始接收用户命令了。

#include <cstdio>
#include <iostream>
#include <string>

#ifdef _WIN32
#include <windows.h>
#endif

int main() {
#ifdef _WIN32
    SetConsoleOutputCP(CP_UTF8);
#endif

    // 注册这个进程能处理的命令。宿主收到后会填进自己的命令表。
    std::printf("register hello 打印问候\n");
    std::printf("register ping 测试通道\n");
    std::printf("ready\n");
    std::fflush(stdout);

    std::string line;

    // 对话循环：读一行，执行，写一行结果。
    while (std::getline(std::cin, line)) {
        while (!line.empty() && (line.back() == '\r' || line.back() == ' ')) {
            line.pop_back();
        }

        if (line == "ping") {
            std::printf("pong\n");
            std::fflush(stdout);
        } else if (line == "hello") {
            std::printf("hello from plugin process\n");
            std::fflush(stdout);
        } else if (line == "crash") {
            // 故意制造非法内存访问，观察宿主能不能活下来
            volatile int* p = nullptr;
            *p = 1;
        } else if (line == "quit") {
            break;
        } else {
            std::printf("error unknown\n");
            std::fflush(stdout);
        }
    }

    return 0;
}
