#!/bin/bash

# 网络关键词爬虫程序 - 图形化启动器 (Linux/Mac版本)
# 使用方法: ./run_gui.sh 或 bash run_gui.sh

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# 打印横幅
print_banner() {
    echo -e "${CYAN}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                    🕷️ 网络关键词爬虫程序 🕷️                    ║"
    echo "║                                                              ║"
    echo "║  图形化界面 • 易于使用 • 智能检测 • 自动安装                    ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# 检查Python环境
check_python() {
    echo -e "${BLUE}🔍 正在检查Python环境...${NC}"

    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
        echo -e "${GREEN}✅ 找到Python3${NC}"
    elif command -v python &> /dev/null; then
        PYTHON_CMD="python"
        echo -e "${GREEN}✅ 找到Python${NC}"
    else
        echo -e "${RED}❌ 错误: 未找到Python，请先安装Python 3.7+${NC}"
        echo ""
        echo -e "${YELLOW}💡 安装建议:${NC}"
        echo "    Ubuntu/Debian: sudo apt-get install python3 python3-pip"
        echo "    CentOS/RHEL: sudo yum install python3 python3-pip"
        echo "    macOS: brew install python3"
        echo "    或访问: https://www.python.org/downloads/"
        echo ""
        exit 1
    fi

    # 检查Python版本
    PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
    echo -e "${GREEN}✅ Python版本: $PYTHON_VERSION${NC}"

    # 检查版本是否满足要求
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

    if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 7 ]); then
        echo -e "${RED}❌ Python版本过低，需要Python 3.7或更高版本${NC}"
        exit 1
    fi
}

# 检查程序文件
check_files() {
    echo -e "${BLUE}🔍 正在检查程序文件...${NC}"

    if [ ! -f "gui_launcher.py" ]; then
        echo -e "${RED}❌ 错误: 找不到图形化启动器文件 gui_launcher.py${NC}"
        echo "   请确保所有程序文件都在同一目录下"
        exit 1
    fi

    echo -e "${GREEN}✅ 程序文件检查通过！${NC}"
}

# 检查图形环境
check_display() {
    echo -e "${BLUE}🔍 正在检查图形环境...${NC}"

    if [ -z "$DISPLAY" ] && [ "$(uname)" != "Darwin" ]; then
        echo -e "${YELLOW}⚠️  未检测到图形环境${NC}"
        echo -e "${BLUE}💡 如果您在服务器上运行，请使用命令行版本${NC}"
        echo "   命令行版本: python smart_launcher.py"
    else
        echo -e "${GREEN}✅ 图形环境检查通过！${NC}"
    fi
}

# 启动程序
launch_program() {
    echo -e "${BLUE}🚀 启动图形化界面...${NC}"
    echo ""

    # 运行图形化启动器
    $PYTHON_CMD gui_launcher.py

    local exit_code=$?

    echo ""
    echo -e "${CYAN}📋 程序执行完毕！${NC}"

    if [ $exit_code -eq 0 ]; then
        echo -e "${GREEN}✅ 程序正常退出${NC}"
    else
        echo -e "${YELLOW}⚠️  程序异常退出 (退出码: $exit_code)${NC}"
    fi

    echo ""
    echo -e "${YELLOW}💡 提示: 您也可以直接运行以下命令:${NC}"
    echo "   $PYTHON_CMD gui_launcher.py          - 启动图形化启动器"
    echo "   $PYTHON_CMD gui_crawler.py           - 启动图形化爬虫"
    echo "   $PYTHON_CMD smart_launcher.py        - 启动命令行启动器"
    echo ""
}

# 主函数
main() {
    print_banner

    # 检查Python环境
    check_python

    # 检查程序文件
    check_files

    # 检查图形环境
    check_display

    # 启动程序
    launch_program
}

# 错误处理
trap 'echo -e "\n${RED}⚠️  程序被中断${NC}"; exit 1' INT TERM

# 运行主函数
main "$@"
