// 第 1 章：二十行程序
//
// 这是全书的起点，一个只会响应几条命令的小程序。
// 它已经包含了后面所有章节都会用到的三个零件：
//   1. 一个循环，不停等待输入        —— 事件循环的雏形
//   2. 一张写死的命令表（if/else）   —— 注册表的雏形
//   3. 一个输出通道（屏幕）          —— 宿主提供的能力的雏形
//
// 编译（Windows，打开“开发者命令提示”后执行）：
//   cl /EHsc /std:c++17 /utf-8 main.cpp
// 编译（Linux 或 MinGW）：
//   g++ -std=c++17 main.cpp -o app
//
// 运行后依次输入 hello、time、随便写点什么、quit，观察输出。

#include <iostream>   // std::cout、std::cin：屏幕输出和键盘输入
#include <string>     // std::string：一串文字

#ifdef _WIN32
#include <windows.h>  // SetConsoleOutputCP：只在 Windows 上需要
#endif

int main() {
#ifdef _WIN32
    // Windows 控制台默认按 GBK 显示文字，而源文件是 UTF-8。
    // 不切换编码的话，下面的中文会显示成“浣犲ソ”这类乱码。
    // 这一行把控制台输出切到 UTF-8，Linux 和 macOS 不需要。
    SetConsoleOutputCP(CP_UTF8);
#endif

    std::string line;   // 用来装用户输入的一整行文字

    // 主循环：一直转，直到遇到 break。
    // 真实的软件也是这样的结构：等操作、处理、再等下一个操作。
    while (true) {
        std::cout << "> ";   // 打印提示符，告诉用户可以输入了

        // 从键盘读一整行，放进 line。
        // getline 返回“有没有读到”，读不到（比如用户按 Ctrl+Z）就退出循环。
        if (!std::getline(std::cin, line)) break;

        // 用户输入 quit，结束程序。
        if (line == "quit") break;

        // 下面是写死的命令表：一个名字对应一段处理逻辑。
        // 第 5 章会把它换成运行时可以增删的注册表。
        if (line == "hello") {
            std::cout << "你好，世界\n";
        } else if (line == "time") {
            std::cout << "现在该干活了\n";
        } else {
            // 不认识的命令，把用户输入原样带出来，方便排查。
            std::cout << "不认识的命令：" << line << "\n";
        }
    }

    return 0;   // 0 表示程序正常结束
}
