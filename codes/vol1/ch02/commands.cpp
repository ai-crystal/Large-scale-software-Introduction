// 第 2 章：命令模块的实现
//
// 这个文件里放两个命令的具体实现。
// 它单独编译成一个目标文件（Windows 上是 commands.obj），
// 最后由链接器把它和 main.obj 拼在一起。

#include "commands.h"   // 包含自己的声明，保证声明和定义一致
#include <iostream>     // std::cout

// 对应 commands.h 里的 void cmd_hello();
// 函数体是“定义”，有完整的大括号。
void cmd_hello() {
    std::cout << "你好，世界\n";
}

// 对应 commands.h 里的 void cmd_time();
void cmd_time() {
    std::cout << "现在该干活了\n";
}
