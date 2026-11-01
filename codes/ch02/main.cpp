// 第 2 章：主程序
//
// 和上一章相比，命令的处理逻辑被搬到了 commands.cpp。
// 这个文件只负责：读输入、判断是哪个命令、调用对应函数。
//
// 编译时要把两个源文件一起交给编译器：
//   cl /EHsc /std:c++17 /utf-8 main.cpp commands.cpp
// 或者：
//   g++ -std=c++17 main.cpp commands.cpp -o app
//
// 编译器会分别把两个 .cpp 编译成 .obj，再链接成一个 exe。

#include <iostream>
#include <string>

#include "commands.h"   // 拿到 cmd_hello / cmd_time 的声明

#ifdef _WIN32
#include <windows.h>
#endif

int main() {
#ifdef _WIN32
    SetConsoleOutputCP(CP_UTF8);   // 让控制台按 UTF-8 显示中文
#endif

    std::string line;

    while (true) {
        std::cout << "> ";
        if (!std::getline(std::cin, line)) break;
        if (line == "quit") break;

        // 命令表还是 if/else，但每一项只负责调用一个函数，
        // 具体做什么已经搬到了 commands.cpp。
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
