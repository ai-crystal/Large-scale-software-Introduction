# 第 7 章：进程隔离

`plugin_host.cpp` 是插件进程，`host.cpp` 是宿主。宿主启动插件进程，通过两根管道发一句 `ping`，读一句 `pong`，三秒没有回复就结束进程。

## 编译运行（Windows）

```bat
cl /EHsc /std:c++17 /utf-8 plugin_host.cpp
cl /EHsc /std:c++17 /utf-8 host.cpp
host.exe
```

预期输出：

```text
子进程回复：pong
```

把 `host.cpp` 里的 `ping` 换成 `crash`，可以看到插件进程崩溃，宿主仍然正常退出。

## Linux 对应写法

| 步骤 | Windows | Linux |
|---|---|---|
| 创建管道 | `CreatePipe` | `pipe` |
| 启动进程 | `CreateProcess` | `fork` + `execv` |
| 重定向输入输出 | `STARTUPINFO` | `dup2` |
| 读 | `ReadFile` | `read` |
| 写 | `WriteFile` | `write` |
| 等待 | `WaitForSingleObject` | `waitpid` |
| 强制结束 | `TerminateProcess` | `kill` + `SIGKILL` |
