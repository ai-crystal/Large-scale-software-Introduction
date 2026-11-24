@echo off
setlocal
cd /d "%~dp0"

set "PYEXE="
if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" set "PYEXE=%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
if not defined PYEXE if exist "%LOCALAPPDATA%\Programs\Python\Python313\python.exe" set "PYEXE=%LOCALAPPDATA%\Programs\Python\Python313\python.exe"
if not defined PYEXE if exist "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" set "PYEXE=%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
if not defined PYEXE if exist "C:\Python312\python.exe" set "PYEXE=C:\Python312\python.exe"
if not defined PYEXE for /f "delims=" %%P in ('where python 2^>nul') do if not defined PYEXE set "PYEXE=%%P"
if not defined PYEXE (
  echo [ERROR] Python 3.10+ not found.
  pause
  exit /b 1
)

if /i "%1"=="vol1" goto v1
if /i "%1"=="vol2" goto v2
if /i "%1"=="vol3" goto v3
if /i "%1"=="vol4" goto v4

echo usage: build-book.bat vol1 ^| vol2 ^| vol3 ^| vol4
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

:v4
"%PYEXE%" books\build\build.py --book books\vol4-patterns
exit /b %errorlevel%
