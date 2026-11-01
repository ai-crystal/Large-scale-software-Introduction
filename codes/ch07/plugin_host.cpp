// 第 7 章：插件进程
//
// 这是一个独立的小程序，宿主会启动它，然后通过标准输入输出和它对话。
// 它不知道宿主的存在，只做一件事：读一行，执行，写一行。
//
// 这样做的好处：它崩溃或死循环时，宿主不受影响，可以直接把它杀掉。

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

    std::string line;

    // 从标准输入读一行。宿主关掉管道时，getline 返回失败，循环结束。
    while (std::getline(std::cin, line)) {
        // 去掉行尾的 \r（Windows 管道可能带）。
        while (!line.empty() && (line.back() == '\r' || line.back() == ' ')) {
            line.pop_back();
        }

        if (line == "ping") {
            // 最简单的应答，用来验证通道是通的。
            std::printf("pong\n");
            std::fflush(stdout);
        } else if (line == "hello") {
            std::printf("hello from plugin process\n");
            std::fflush(stdout);
        } else if (line == "crash") {
            // 故意制造一次非法内存访问，用来观察宿主的反应。
            // 这个进程会立刻退出，但宿主仍然活着。
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
