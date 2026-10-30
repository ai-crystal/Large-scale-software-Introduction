// 第 1 章：二十行程序
// 编译（Windows）：cl /EHsc /std:c++17 /utf-8 main.cpp
// 编译（Linux）：g++ -std=c++17 main.cpp -o app

#include <iostream>
#include <string>

int main() {
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
