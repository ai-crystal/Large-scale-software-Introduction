#ifdef _WIN32
#include <windows.h>
#endif

#include <iostream>
#include <string>
#include "commands.h"

int main() {
#ifdef _WIN32
    SetConsoleOutputCP(CP_UTF8);
#endif

    std::string line;
    while (true) {
        std::cout << "> ";
        if (!std::getline(std::cin, line)) break;
        if (line == "quit") break;
        if (line == "hello") {
            cmd_hello();
        } else if (line == "time") {
            cmd_time();
        } else {
            std::cout << "不认识的命令：" << line << "\n";
        }
    }
    return 0;
}
