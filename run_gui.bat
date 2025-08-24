@echo off
chcp 65001 >nul
title 网络关键词爬虫程序 - 图形化启动器
color 0B

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    🕷️ 网络关键词爬虫程序 🕷️                    ║
echo ║                                                              ║
echo ║  图形化界面 • 易于使用 • 智能检测 • 自动安装                    ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo 🔍 正在检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: 未找到Python，请先安装Python 3.7+
    echo.
    echo 💡 安装建议:
    echo    1. 访问 https://www.python.org/downloads/
    echo    2. 下载并安装Python 3.7或更高版本
    echo    3. 安装时勾选"Add Python to PATH"
    echo.
    pause
    exit /b 1
)

echo ✅ Python环境检查通过！
echo.

echo 🔍 正在检查程序文件...
if not exist "gui_launcher.py" (
    echo ❌ 错误: 找不到图形化启动器文件 gui_launcher.py
    echo    请确保所有程序文件都在同一目录下
    pause
    exit /b 1
)

echo ✅ 程序文件检查通过！
echo.

echo 🚀 启动图形化界面...
echo.

REM 运行图形化启动器
python gui_launcher.py

echo.
echo 📋 程序执行完毕！
echo 💡 提示: 您也可以直接运行以下命令:
echo    python gui_launcher.py          - 启动图形化启动器
echo    python gui_crawler.py           - 启动图形化爬虫
echo    python smart_launcher.py        - 启动命令行启动器
echo.

pause
