#!/bin/bash

# 设置UTF-8编码
export LANG=zh_CN.UTF-8
export LC_ALL=zh_CN.UTF-8

echo "========================================"
echo "      MaiBot-Plus 一键启动程序"
echo "========================================"
echo

# 检测是否在临时目录中运行
CURRENT_PATH="$(pwd)"
IN_ARCHIVE=0

if echo "$CURRENT_PATH" | grep -qi "temp"; then
    IN_ARCHIVE=1
elif echo "$CURRENT_PATH" | grep -qi "tmp"; then
    IN_ARCHIVE=1
elif echo "$CURRENT_PATH" | grep -qi "\.tar"; then
    IN_ARCHIVE=1
elif echo "$CURRENT_PATH" | grep -qi "\.zip"; then
    IN_ARCHIVE=1
elif echo "$CURRENT_PATH" | grep -qi "\.gz"; then
    IN_ARCHIVE=1
fi

if [ "$IN_ARCHIVE" -eq 1 ]; then
    echo "❌ 检测到在压缩包中运行！"
    echo
    echo "请先解压缩文件到本地目录再运行此脚本"
    echo
    read -n 1 -s
    exit 1
fi

# 保存当前目录并切换到脚本目录
CURRENT_DIR="$(pwd)"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 检查是否在正确的MaiBot-Plus目录中
if [ ! -f "onekey_linux.py" ]; then
    echo "❌ 错误：未找到onekey_linux.py文件！"
    echo
    echo "请确保此脚本位于MaiBot-Plus项目根目录中"
    echo "当前目录：$SCRIPT_DIR"
    echo
    read -p "按任意键退出..."
    exit 1
fi

# 检查虚拟环境和依赖标记
VENV_PATH="$SCRIPT_DIR/.venv"
PYTHON_PATH="$VENV_PATH/bin/python"
DEPS_CHECK_FILE="$SCRIPT_DIR/.deps_installed"

echo "检查运行环境..."

if [ ! -f "$PYTHON_PATH" ]; then
    echo "❌ 虚拟环境未找到！"
    echo
    echo "请先运行 \"./首次启动点我.sh\" 初始化环境"
    echo
    read -p "按任意键退出..."
    exit 1
fi

if [ ! -f "$DEPS_CHECK_FILE" ]; then
    echo "❌ 依赖未安装！"
    echo
    echo "请先运行 \"./首次启动点我.sh\" 安装依赖"
    echo
    read -p "按任意键退出..."
    exit 1
fi

echo "✅ 环境检查通过"
echo
echo "启动 MaiBot-Plus 管理程序..."
echo "========================================"

# 启动onekey_linux.py
"$PYTHON_PATH" onekey_linux.py
EXIT_CODE=$?

# 如果程序异常退出，显示错误信息
if [ $EXIT_CODE -ne 0 ]; then
    echo
    echo "========================================"
    echo "程序异常退出，错误代码：$EXIT_CODE"
    echo
    echo "如果遇到依赖问题，请重新运行："
    echo "   \"./首次启动点我.sh\""
    echo "========================================"
fi

echo
echo "按任意键退出..."
read -n 1 -s