// 第 7 章：宿主（Windows 版）
//
// 第 6 章的命令循环还在：用户输入命令，宿主处理。
// 区别是 hello / ping 这两条命令不再由同进程的插件函数执行，
// 而是通过管道发给 plugin_host.exe，等它回复。
//
// 这样既保留了“程序接收命令”的主线，又能演示进程隔离：
// 插件崩了或卡住，宿主可以把它杀掉，自己继续运行。
//
// Linux 的对应函数见同目录 README.md：
//   CreatePipe -> pipe
//   CreateProcess -> fork + execv
//   ReadFile/WriteFile -> read/write
//   WaitForSingleObject -> waitpid
//   TerminateProcess -> kill

#include <windows.h>

#include <cstdio>
#include <cstring>
#include <iostream>
#include <string>

// 两根管道的宿主端
static HANDLE g_in = nullptr;    // 宿主写，插件读
static HANDLE g_out = nullptr;   // 插件写，宿主读

// 往插件写一行
static bool write_line(const std::string& text) {
    std::string line = text + "\n";
    DWORD written = 0;
    return WriteFile(g_in, line.c_str(), (DWORD)line.size(), &written, nullptr) != 0;
}

// 从插件读一行，最多等 timeout_ms 毫秒。
// 用 PeekNamedPipe 轮询，避免阻塞的 ReadFile 永远等下去。
static std::string read_line(int timeout_ms) {
    std::string reply;
    DWORD start = GetTickCount();

    while (GetTickCount() - start < (DWORD)timeout_ms) {
        DWORD available = 0;
        if (PeekNamedPipe(g_out, nullptr, 0, nullptr, &available, nullptr) && available > 0) {
            char buffer[256]{};
            DWORD want = available < sizeof(buffer) - 1 ? available : (DWORD)sizeof(buffer) - 1;
            DWORD got = 0;
            if (ReadFile(g_out, buffer, want, &got, nullptr) && got > 0) {
                reply.append(buffer, got);
                if (reply.find('\n') != std::string::npos) break;
            }
        }
        Sleep(20);
    }
    return reply;
}

int main() {
#ifdef _WIN32
    SetConsoleOutputCP(CP_UTF8);
#endif

    // 让子进程能继承管道把手
    SECURITY_ATTRIBUTES sa{};
    sa.nLength = sizeof(sa);
    sa.bInheritHandle = TRUE;

    HANDLE in_read = nullptr, in_write = nullptr;
    HANDLE out_read = nullptr, out_write = nullptr;
    CreatePipe(&in_read, &in_write, &sa, 0);
    CreatePipe(&out_read, &out_write, &sa, 0);

    // 子进程的标准输入输出改成这两根管道
    STARTUPINFOA si{};
    si.cb = sizeof(si);
    si.dwFlags = STARTF_USESTDHANDLES;
    si.hStdInput = in_read;
    si.hStdOutput = out_write;
    si.hStdError = out_write;

    PROCESS_INFORMATION pi{};
    char cmd[] = "plugin_host.exe";
    if (!CreateProcessA(nullptr, cmd, nullptr, nullptr, TRUE, 0,
                        nullptr, nullptr, &si, &pi)) {
        std::printf("启动失败：%lu\n", GetLastError());
        return 1;
    }

    // 宿主不需要这两头
    CloseHandle(in_read);
    CloseHandle(out_write);

    g_in = in_write;
    g_out = out_read;

    // 命令循环：和第 5、6 章一样，只是命令被转发给另一个进程
    std::string line;
    while (true) {
        std::printf("> ");
        std::fflush(stdout);

        if (!std::getline(std::cin, line)) break;
        while (!line.empty() && (line.back() == '\r' || line.back() == ' ')) {
            line.pop_back();
        }
        if (line == "quit") break;
        if (line.empty()) continue;

        if (line != "hello" && line != "ping") {
            std::printf("未知命令：%s（试试 hello、ping、crash）\n", line.c_str());
            continue;
        }

        // 发给插件进程
        if (!write_line(line)) {
            std::printf("管道已关闭\n");
            break;
        }

        // 等回复，最多三秒
        std::string reply = read_line(3000);
        if (reply.empty()) {
            std::printf("三秒没有回复，结束插件进程\n");
            TerminateProcess(pi.hProcess, 1);
            break;
        }
        std::printf("%s", reply.c_str());
        std::fflush(stdout);
    }

    // 客气温和地让它退出，等三秒，再强制结束
    write_line("quit");
    WaitForSingleObject(pi.hProcess, 3000);
    TerminateProcess(pi.hProcess, 0);

    CloseHandle(g_in);
    CloseHandle(pi.hProcess);
    CloseHandle(pi.hThread);
    CloseHandle(g_out);
    return 0;
}
