@echo off
setlocal
cd /d "%~dp0"

set "PYEXE="
if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" set "PYEXE=%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
if not defined PYEXE if exist "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" set "PYEXE=%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
if not defined PYEXE if exist "C:\Python312\python.exe" set "PYEXE=C:\Python312\python.exe"
if not defined PYEXE if exist "C:\Python311\python.exe" set "PYEXE=C:\Python311\python.exe"
if not defined PYEXE for /f "delims=" %%P in ('where python 2^>nul') do if not defined PYEXE set "PYEXE=%%P"
if not defined PYEXE (
  echo [ERROR] 没有找到 Python 3.10 以上版本。
  pause
  exit /b 1
)

echo [1/4] 检查依赖
"%PYEXE%" -c "import markdown, pymdownx, pygments, playwright, fitz, matplotlib, PIL" >nul 2>nul
if errorlevel 1 (
  "%PYEXE%" -m pip install -r book\build\requirements.txt
  if errorlevel 1 (
    echo [ERROR] 依赖安装失败。
    pause
    exit /b 1
  )
)

echo [2/4] 生成插图
"%PYEXE%" book\build\render_figures.py
if errorlevel 1 (
  echo [ERROR] 插图生成失败。
  pause
  exit /b 1
)

echo [3/4] 排版 PDF
"%PYEXE%" book\build\build.py
if errorlevel 1 (
  echo [ERROR] PDF 生成失败。如果 output\book.pdf 正被占用，请先关闭阅读器。
  pause
  exit /b 1
)

echo [4/4] 自检
"%PYEXE%" book\build\checks\verify_pdf_text.py
"%PYEXE%" book\build\checks\verify_repo.py

echo.
echo 完成：output\book.pdf
pause
