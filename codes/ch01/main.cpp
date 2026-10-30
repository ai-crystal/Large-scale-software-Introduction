// 第 1 章：二十行程序
// 编译（Windows）：cl /EHsc /std:c++17 /utf-8 main.cpp
// 编译（Linux）：g++ -std=c++17 main.cpp -o app

#ifdef _WIN32
#include <windows.h>
#endif

#include <iostream>
#include <string>

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
            std::cout << "你好，世界\n";
        } else if (line == "time") {
            std::cout << "现在该干活了\n";
        } else {
            std::cout << "不认识的命令：" << line << "\n";
        }
    }
    return 0;
}
