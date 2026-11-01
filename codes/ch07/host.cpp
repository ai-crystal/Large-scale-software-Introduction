// 第 7 章：宿主（Windows 版）
//
// 宿主启动 plugin_host.exe，通过两根管道一问一答。
// 等三秒没有回复，就认为插件卡住，直接结束它。
//
// 这里用的是 Windows API。Linux 的对应函数见同目录 README.md：
//   CreatePipe -> pipe
//   CreateProcess -> fork + execv
//   ReadFile/WriteFile -> read/write
//   WaitForSingleObject -> waitpid
//   TerminateProcess -> kill

#include <windows.h>

#include <cstdio>
#include <cstring>
#include <string>

int main() {
    // 让子进程能继承管道的把手。
    SECURITY_ATTRIBUTES sa{};
    sa.nLength = sizeof(sa);
    sa.bInheritHandle = TRUE;

    // 两根管道：
    //   in_read  / in_write   宿主写，子进程读
    //   out_read / out_write  子进程写，宿主读
    HANDLE in_read = nullptr, in_write = nullptr;
    HANDLE out_read = nullptr, out_write = nullptr;
    CreatePipe(&in_read, &in_write, &sa, 0);
    CreatePipe(&out_read, &out_write, &sa, 0);

    // 告诉系统：子进程的标准输入输出不要用控制台，用这两根管道。
    STARTUPINFOA si{};
    si.cb = sizeof(si);
    si.dwFlags = STARTF_USESTDHANDLES;
    si.hStdInput = in_read;
    si.hStdOutput = out_write;
    si.hStdError = out_write;

    PROCESS_INFORMATION pi{};
    char cmd[] = "plugin_host.exe";

    // 启动子进程。第五个参数 TRUE 表示允许继承把手。
    if (!CreateProcessA(nullptr, cmd, nullptr, nullptr, TRUE, 0,
                        nullptr, nullptr, &si, &pi)) {
        std::printf("启动失败：%lu\n", GetLastError());
        return 1;
    }

    // 宿主不需要这两头，关掉。
    // 不关的话，管道永远有一端开着，读数据时会一直等。
    CloseHandle(in_read);
    CloseHandle(out_write);

    // 发一句 ping。
    const char* msg = "ping\n";
    DWORD written = 0;
    WriteFile(in_write, msg, (DWORD)std::strlen(msg), &written, nullptr);

    // 轮询等待回复，最多三秒。
    // 不用阻塞的 ReadFile，因为它可能永远等下去。
    std::string reply;
    DWORD start = GetTickCount();
    while (GetTickCount() - start < 3000) {
        DWORD available = 0;

        // PeekNamedPipe 只查看有多少字节可读，不真的读走。
        if (PeekNamedPipe(out_read, nullptr, 0, nullptr, &available, nullptr) && available > 0) {
            char buffer[256]{};
            DWORD want = available < sizeof(buffer) - 1 ? available : (DWORD)sizeof(buffer) - 1;
            DWORD got = 0;

            // 真正读走，追加到 reply。
            if (ReadFile(out_read, buffer, want, &got, nullptr) && got > 0) {
                reply.append(buffer, got);
                if (reply.find('\n') != std::string::npos) break;
            }
        }
        Sleep(20);   // 没数据就歇 20 毫秒，别空转占满 CPU
    }

    if (reply.empty()) {
        // 三秒没回应，认为插件卡死，强制结束。
        std::printf("三秒没有回复，结束插件进程\n");
        TerminateProcess(pi.hProcess, 1);
    } else {
        std::printf("子进程回复：%s", reply.c_str());

        // 客气温和地让它退出，等三秒，再强制结束。
        const char* quit = "quit\n";
        WriteFile(in_write, quit, (DWORD)std::strlen(quit), &written, nullptr);
        WaitForSingleObject(pi.hProcess, 3000);
        TerminateProcess(pi.hProcess, 0);
    }

    // 关闭所有把手，释放资源。
    CloseHandle(in_write);
    CloseHandle(pi.hProcess);
    CloseHandle(pi.hThread);
    CloseHandle(out_read);
    return 0;
}
