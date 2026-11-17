@echo off
setlocal
cd /d "%~dp0"
set "PYEXE="
for /f "delims=" %%P in ('where python 2^>nul') do if not defined PYEXE set "PYEXE=%%P"
if not defined PYEXE (
  echo [ERROR] 没有找到 Python。
  pause
  exit /b 1
)

if /i "%1"=="vol1" goto v1
if /i "%1"=="vol2" goto v2
if /i "%1"=="vol3" goto v3

echo 用法: build-book.bat vol1 ^| vol2 ^| vol3
exit /b 1

:v1
"%PYEXE%" books\build\build.py --book books\vol1-basics
exit /b %errorlevel%

:v2
"%PYEXE%" books\build\build.py --book books\vol2-architecture
exit /b %errorlevel%

:v3
"%PYEXE%" books\build\build.py --book books\vol3-engineering
exit /b %errorlevel%
