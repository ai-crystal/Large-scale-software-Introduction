// 插件进程：从标准输入读一行，执行，往标准输出写一行
#include <cstdio>
#include <iostream>
#include <string>

int main() {
    std::string line;
    while (std::getline(std::cin, line)) {
        if (line == "ping") {
            std::printf("pong\n");
            std::fflush(stdout);
        } else if (line == "hello") {
            std::printf("hello from plugin process\n");
            std::fflush(stdout);
        } else if (line == "crash") {
            // 故意制造崩溃，用来观察宿主的反应
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
