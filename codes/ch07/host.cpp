// 第 7 章：宿主（Windows 版）
//
// 插件跑在独立进程 plugin_host.exe 里。
// 启动后先读它发来的 register 消息，填进远程命令表；
// 然后进入命令循环，用户输入的命令通过管道转发过去。
//
// Linux 的对应函数见同目录 README.md。

#include <windows.h>

#include <cstdio>
#include <cstring>
#include <iostream>
#include <map>
#include <string>

// 两根管道的宿主端
static HANDLE g_in = nullptr;    // 宿主写，插件读
static HANDLE g_out = nullptr;   // 插件写，宿主读

// 远程命令表：命令名 -> 说明。
// 这里存的是“转发信息”，不是函数指针。
static std::map<std::string, std::string> g_remote;

// 往插件写一行
static bool write_line(const std::string& text) {
    std::string line = text + "\n";
    DWORD written = 0;
    return WriteFile(g_in, line.c_str(), (DWORD)line.size(), &written, nullptr) != 0;
}

// 从插件读一行，最多等 timeout_ms 毫秒。
// 逐字节读，遇到换行返回，避免把多条消息混在一起。
static std::string read_line(int timeout_ms) {
    std::string line;
    DWORD start = GetTickCount();

    while (GetTickCount() - start < (DWORD)timeout_ms) {
        DWORD available = 0;
        if (PeekNamedPipe(g_out, nullptr, 0, nullptr, &available, nullptr) && available > 0) {
            char ch = 0;
            DWORD got = 0;
            if (ReadFile(g_out, &ch, 1, &got, nullptr) && got == 1) {
                if (ch == '\n') return line;
                if (ch != '\r') line.push_back(ch);
            }
        } else {
            Sleep(20);
        }
    }
    return line;
}

// 读插件启动时发来的注册消息，直到 ready。
static bool load_remote_commands() {
    while (true) {
        std::string line = read_line(3000);
        if (line.empty()) return false;
        if (line == "ready") return true;

        // 格式：register <名字> <说明>
        if (line.rfind("register ", 0) == 0) {
            std::string rest = line.substr(9);
            size_t space = rest.find(' ');
            std::string name = space == std::string::npos ? rest : rest.substr(0, space);
            std::string desc = space == std::string::npos ? "" : rest.substr(space + 1);
            g_remote[name] = desc;
        }
    }
}

int main() {
#ifdef _WIN32
    SetConsoleOutputCP(CP_UTF8);
#endif

    // 第一步：创建两根管道
    SECURITY_ATTRIBUTES sa{};
    sa.nLength = sizeof(sa);
    sa.bInheritHandle = TRUE;

    HANDLE in_read = nullptr, in_write = nullptr;
    HANDLE out_read = nullptr, out_write = nullptr;
    CreatePipe(&in_read, &in_write, &sa, 0);
    CreatePipe(&out_read, &out_write, &sa, 0);

    // 第二步：指定子进程的标准输入输出
    STARTUPINFOA si{};
    si.cb = sizeof(si);
    si.dwFlags = STARTF_USESTDHANDLES;
    si.hStdInput = in_read;
    si.hStdOutput = out_write;
    si.hStdError = out_write;

    // 第三步：启动子进程
    PROCESS_INFORMATION pi{};
    char cmd[] = "plugin_host.exe";
    if (!CreateProcessA(nullptr, cmd, nullptr, nullptr, TRUE, 0,
                        nullptr, nullptr, &si, &pi)) {
        std::printf("启动失败：%lu\n", GetLastError());
        return 1;
    }

    // 第四步：关掉宿主不需要的把手
    CloseHandle(in_read);
    CloseHandle(out_write);

    g_in = in_write;
    g_out = out_read;

    // 读注册消息，宿主这时才知道插件支持哪些命令
    if (!load_remote_commands()) {
        std::printf("插件没有完成注册\n");
        TerminateProcess(pi.hProcess, 1);
        return 1;
    }

    // 第五步：命令循环。命令不再查本地函数表，而是查远程命令表。
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

        if (line == "help") {
            for (const auto& pair : g_remote) {
                std::printf("  %-12s %s\n", pair.first.c_str(), pair.second.c_str());
            }
            continue;
        }

        // 查远程命令表
        if (g_remote.find(line) == g_remote.end()) {
            std::printf("未知命令：%s（输入 help 查看）\n", line.c_str());
            continue;
        }

        // 命令名发给插件进程
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
        std::printf("%s\n", reply.c_str());
        std::fflush(stdout);
    }

    // 收尾：先请它退出，等三秒，再强制结束
    write_line("quit");
    WaitForSingleObject(pi.hProcess, 3000);
    TerminateProcess(pi.hProcess, 0);

    CloseHandle(g_in);
    CloseHandle(pi.hProcess);
    CloseHandle(pi.hThread);
    CloseHandle(g_out);
    return 0;
}
