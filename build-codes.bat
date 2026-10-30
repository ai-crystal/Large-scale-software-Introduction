@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"

set "OUT=build"
if not exist "%OUT%" mkdir "%OUT%"

rem ---------- 1. 找 MSVC ----------
set "VCVARS="
set "VSWHERE=%ProgramFiles(x86)%\Microsoft Visual Studio\Installer\vswhere.exe"
if exist "%VSWHERE%" (
  for /f "usebackq delims=" %%P in (`"%VSWHERE%" -latest -products * -requires Microsoft.VisualStudio.Component.VC.Tools.x86.x64 -property installationPath`) do set "VSPATH=%%P"
)
if defined VSPATH if exist "%VSPATH%\VC\Auxiliary\Build\vcvars64.bat" set "VCVARS=%VSPATH%\VC\Auxiliary\Build\vcvars64.bat"

if not defined VCVARS (
  for %%D in (
    "%ProgramFiles%\Microsoft Visual Studio\2022\Community"
    "%ProgramFiles%\Microsoft Visual Studio\2022\Professional"
    "%ProgramFiles%\Microsoft Visual Studio\2022\Enterprise"
    "%ProgramFiles%\Microsoft Visual Studio\2022\BuildTools"
    "%ProgramFiles(x86)%\Microsoft Visual Studio\2019\Community"
    "%ProgramFiles(x86)%\Microsoft Visual Studio\2019\Professional"
    "%ProgramFiles(x86)%\Microsoft Visual Studio\2019\Enterprise"
    "%ProgramFiles(x86)%\Microsoft Visual Studio\2019\BuildTools"
  ) do (
    if not defined VCVARS if exist "%%~D\VC\Auxiliary\Build\vcvars64.bat" set "VCVARS=%%~D\VC\Auxiliary\Build\vcvars64.bat"
  )
)

if not defined VCVARS (
  echo [ERROR] 没有找到 vcvars64.bat。
  echo 请安装 Visual Studio，并勾选“使用 C++ 的桌面开发”工作负载。
  exit /b 1
)

echo 使用 MSVC: %VCVARS%
call "%VCVARS%" >nul

rem ---------- 2. 补齐 Windows SDK 路径 ----------
rem 有的机器上 vcvars 没有把 UCRT 加进 INCLUDE，这里补一次，重复也无害。
set "SDKROOT=%ProgramFiles(x86)%\Windows Kits\10"
if exist "%SDKROOT%\Include" (
  for /f "delims=" %%D in ('dir /b /ad /o-n "%SDKROOT%\Include" 2^>nul') do (
    if not defined SDKV set "SDKV=%%D"
  )
)
if defined SDKV (
  set "INCLUDE=%INCLUDE%;%SDKROOT%\Include\%SDKV%\ucrt;%SDKROOT%\Include\%SDKV%\um;%SDKROOT%\Include\%SDKV%\shared"
  set "LIB=%LIB%;%SDKROOT%\Lib\%SDKV%\ucrt\x64;%SDKROOT%\Lib\%SDKV%\um\x64"
  echo 使用 Windows SDK: %SDKV%
)

set "CFLAGS=/nologo /EHsc /std:c++17 /utf-8 /wd4819"
set "FAIL="

for %%C in (ch01 ch02 ch03 ch04 ch05 ch06 ch07 ch08 ch09 ch10 ch11 ch12) do (
  if not exist "%OUT%\%%C" mkdir "%OUT%\%%C"
)
if not exist "%OUT%\ch03\plugins" mkdir "%OUT%\ch03\plugins"
if not exist "%OUT%\ch04\plugins" mkdir "%OUT%\ch04\plugins"
if not exist "%OUT%\ch05\plugins" mkdir "%OUT%\ch05\plugins"
if not exist "%OUT%\ch06\plugins" mkdir "%OUT%\ch06\plugins"
if not exist "%OUT%\ch12\plugins" mkdir "%OUT%\ch12\plugins"

echo.
echo [ch01] 二十行程序
cl %CFLAGS% /Fo:"%OUT%\ch01\\" codes\ch01\main.cpp /Fe:"%OUT%\ch01\app.exe"
if errorlevel 1 set "FAIL=1"

echo.
echo [ch02] 函数与多文件编译
cl %CFLAGS% /Fo:"%OUT%\ch02\\" codes\ch02\main.cpp codes\ch02\commands.cpp /Fe:"%OUT%\ch02\app.exe"
if errorlevel 1 set "FAIL=1"

echo.
echo [ch03] 第一个插件
cl %CFLAGS% /Fo:"%OUT%\ch03\\" /LD codes\ch03\hello_plugin.cpp /Fe:"%OUT%\ch03\plugins\hello_plugin.dll"
if errorlevel 1 set "FAIL=1"
cl %CFLAGS% /Fo:"%OUT%\ch03\\" codes\ch03\host.cpp /Fe:"%OUT%\ch03\host.exe"
if errorlevel 1 set "FAIL=1"

echo.
echo [ch04] 契约与命令注册
cl %CFLAGS% /Fo:"%OUT%\ch04\\" /LD codes\ch04\hello_plugin.cpp /Fe:"%OUT%\ch04\plugins\hello_plugin.dll"
if errorlevel 1 set "FAIL=1"
cl %CFLAGS% /Fo:"%OUT%\ch04\\" codes\ch04\host.cpp /Fe:"%OUT%\ch04\host.exe"
if errorlevel 1 set "FAIL=1"

echo.
echo [ch05] 注册表与卸载
cl %CFLAGS% /Fo:"%OUT%\ch05\\" /LD codes\ch05\hello_plugin.cpp /Fe:"%OUT%\ch05\plugins\hello_plugin.dll"
if errorlevel 1 set "FAIL=1"
cl %CFLAGS% /Fo:"%OUT%\ch05\\" /LD codes\ch05\notes_plugin.cpp /Fe:"%OUT%\ch05\plugins\notes_plugin.dll"
if errorlevel 1 set "FAIL=1"
cl %CFLAGS% /Fo:"%OUT%\ch05\\" codes\ch05\host.cpp codes\ch05\registry.cpp /Fe:"%OUT%\ch05\host.exe"
if errorlevel 1 set "FAIL=1"

echo.
echo [ch06] 事件与钩子
cl %CFLAGS% /Fo:"%OUT%\ch06\\" /LD codes\ch06\hello_plugin.cpp /Fe:"%OUT%\ch06\plugins\hello_plugin.dll"
if errorlevel 1 set "FAIL=1"
cl %CFLAGS% /Fo:"%OUT%\ch06\\" codes\ch06\host.cpp codes\ch06\events.cpp /Fe:"%OUT%\ch06\host.exe"
if errorlevel 1 set "FAIL=1"

echo.
echo [ch07] 进程隔离
cl %CFLAGS% /Fo:"%OUT%\ch07\\" codes\ch07\plugin_host.cpp /Fe:"%OUT%\ch07\plugin_host.exe"
if errorlevel 1 set "FAIL=1"
cl %CFLAGS% /Fo:"%OUT%\ch07\\" codes\ch07\host.cpp /Fe:"%OUT%\ch07\host.exe"
if errorlevel 1 set "FAIL=1"

echo.
echo [ch08] 模板与生成器（脚本，不需要编译）
echo        用 python codes\ch08\tools\new_plugin.py ^<name^> 生成新插件

echo.
echo [ch09] 假宿主与测试
cl %CFLAGS% /Fo:"%OUT%\ch09\\" codes\ch09\mock_host.cpp /Icodes\ch09\sdk\include /Fe:"%OUT%\ch09\mock_host.exe"
if errorlevel 1 set "FAIL=1"
cl %CFLAGS% /Fo:"%OUT%\ch09\\" codes\ch09\tests\test_registry.cpp codes\ch09\registry.cpp /Icodes\ch09\sdk\include /Fe:"%OUT%\ch09\test_registry.exe"
if errorlevel 1 set "FAIL=1"

echo.
echo [ch10] 打包与校验（脚本，不需要编译）
echo        用 python codes\ch10\pack.py ^<dir^> ^<out.zip^>

echo.
echo [ch11] 熔断与 RAII
cl %CFLAGS% /Fo:"%OUT%\ch11\\" codes\ch11\raii_demo.cpp /Fe:"%OUT%\ch11\raii_demo.exe"
if errorlevel 1 set "FAIL=1"
cl %CFLAGS% /Fo:"%OUT%\ch11\\" codes\ch11\breaker_demo.cpp /Fe:"%OUT%\ch11\breaker_demo.exe"
if errorlevel 1 set "FAIL=1"

echo.
echo [ch12] 完整最小外壳
cl %CFLAGS% /Fo:"%OUT%\ch12\\" /LD codes\ch12\plugins\hello\src\plugin.cpp /Icodes\ch12\sdk\include /Fe:"%OUT%\ch12\plugins\hello.dll"
if errorlevel 1 set "FAIL=1"
cl %CFLAGS% /Fo:"%OUT%\ch12\\" /LD codes\ch12\plugins\notes\src\plugin.cpp /Icodes\ch12\sdk\include /Fe:"%OUT%\ch12\plugins\notes.dll"
if errorlevel 1 set "FAIL=1"
cl %CFLAGS% /Fo:"%OUT%\ch12\\" codes\ch12\host\main.cpp codes\ch12\host\registry.cpp codes\ch12\host\events.cpp /Icodes\ch12\sdk\include /Fe:"%OUT%\ch12\host.exe"
if errorlevel 1 set "FAIL=1"

echo.
if defined FAIL (
  echo ============================================
  echo 有章节编译失败，请查看上面的错误信息。
  echo ============================================
  exit /b 1
)

echo ============================================
echo 全部编译完成，产物在 %OUT%\
echo.
echo 运行示例：
echo   %OUT%\ch01\app.exe
echo   %OUT%\ch02\app.exe
echo   %OUT%\ch03\host.exe          （在 %OUT%\ch03 目录里运行）
echo   %OUT%\ch12\host.exe          （在 %OUT%\ch12 目录里运行）
echo ============================================
exit /b 0
