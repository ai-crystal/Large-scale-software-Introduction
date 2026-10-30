#include <iostream>
#include <string>
#include "commands.h"

int main() {
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
