@echo off
setlocal
cd /d "%~dp0"

set "PYEXE="
if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" set "PYEXE=%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
if not defined PYEXE if exist "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" set "PYEXE=%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
if not defined PYEXE if exist "C:\Python312\python.exe" set "PYEXE=C:\Python312\python.exe"
if not defined PYEXE for /f "delims=" %%P in ('where python 2^>nul') do if not defined PYEXE set "PYEXE=%%P"
if not defined PYEXE (
  echo [ERROR] 没有找到 Python 3.10 以上版本。
  pause
  exit /b 1
)

echo [1/3] 检查依赖
"%PYEXE%" -c "import markdown, pymdownx, pygments, playwright, fitz, matplotlib, PIL" >nul 2>nul
if errorlevel 1 (
  "%PYEXE%" -m pip install -r books\build\requirements.txt
  if errorlevel 1 (
    echo [ERROR] 依赖安装失败。
    pause
    exit /b 1
  )
)

if /i "%1"=="figures" goto figures

echo [2/3] 生成插图
"%PYEXE%" books\build\render_figures.py
if errorlevel 1 (
  echo [ERROR] 插图生成失败。
  pause
  exit /b 1
)

echo [3/3] 构建全部册
"%PYEXE%" books\build\build.py --all
if errorlevel 1 (
  echo [ERROR] 构建失败。如果 PDF 正被阅读器打开，请先关闭。
  pause
  exit /b 1
)

echo.
echo 完成，PDF 在 output\
if not "%1"=="" pause
exit /b 0

:figures
echo 只重画插图
"%PYEXE%" books\build\render_figures.py
exit /b 0
