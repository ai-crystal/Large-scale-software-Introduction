// 宿主：启动 plugin_host.exe，通过两根管道一问一答，带三秒超时
// 本文件是 Windows 版本；Linux 的对应函数见同目录 README.md
#include <windows.h>
#include <cstdio>
#include <cstring>
#include <string>

int main() {
    SECURITY_ATTRIBUTES sa{};
    sa.nLength = sizeof(sa);
    sa.bInheritHandle = TRUE;

    HANDLE in_read = nullptr, in_write = nullptr;
    HANDLE out_read = nullptr, out_write = nullptr;
    CreatePipe(&in_read, &in_write, &sa, 0);
    CreatePipe(&out_read, &out_write, &sa, 0);

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

    CloseHandle(in_read);
    CloseHandle(out_write);

    const char* msg = "ping\n";
    DWORD written = 0;
    WriteFile(in_write, msg, (DWORD)std::strlen(msg), &written, nullptr);

    std::string reply;
    DWORD start = GetTickCount();
    while (GetTickCount() - start < 3000) {
        DWORD available = 0;
        if (PeekNamedPipe(out_read, nullptr, 0, nullptr, &available, nullptr) && available > 0) {
            char buffer[256]{};
            DWORD want = available < sizeof(buffer) - 1 ? available : (DWORD)sizeof(buffer) - 1;
            DWORD got = 0;
            if (ReadFile(out_read, buffer, want, &got, nullptr) && got > 0) {
                reply.append(buffer, got);
                if (reply.find('\n') != std::string::npos) break;
            }
        }
        Sleep(20);
    }

    if (reply.empty()) {
        std::printf("三秒没有回复，结束插件进程\n");
        TerminateProcess(pi.hProcess, 1);
    } else {
        std::printf("子进程回复：%s", reply.c_str());
        const char* quit = "quit\n";
        WriteFile(in_write, quit, (DWORD)std::strlen(quit), &written, nullptr);
        WaitForSingleObject(pi.hProcess, 3000);
        TerminateProcess(pi.hProcess, 0);
    }

    CloseHandle(in_write);
    CloseHandle(pi.hProcess);
    CloseHandle(pi.hThread);
    CloseHandle(out_read);
    return 0;
}
