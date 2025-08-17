#!/bin/bash

# 设置UTF-8编码
export LANG=zh_CN.UTF-8
export LC_ALL=zh_CN.UTF-8

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 检查是否在正确的MaiBot-Plus目录中
if [ ! -f "onekey_linux.py" ]; then
    echo "❌ 错误：未找到onekey_linux.py文件！"
    echo
    echo "请确保此脚本位于MaiBot-Plus项目根目录中"
    echo "当前目录：$SCRIPT_DIR"
    echo
    echo "正确的目录结构应该包含："
    echo "  - onekey_linux.py"
    echo "  - Bot/requirements.txt"
    echo "  - Adapter/requirements.txt"
    echo "  - Matcha-Adapter/requirements.txt"
    echo
    read -p "按任意键退出..."
    exit 1
fi

echo "========================================"
echo "       MaiBot-Plus 首次启动配置"
echo "========================================"
echo
echo "本程序将为您完成以下操作："
echo "  • 创建Python虚拟环境"
echo "  • 安装所有必要的依赖包"
echo "  • 初始化运行环境"
echo
echo " 首次运行可能需要几分钟时间，请耐心等待"
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
    echo "检测到在压缩包中运行！"
    echo
    echo "请先解压缩文件到本地目录再运行此脚本"
    echo "直接在压缩包中运行会导致程序异常"
    echo
    echo "按任意键退出，请解压后重新运行"
    read -n 1 -s
    exit 1
fi

# 删除旧的依赖安装标记文件（如果存在）
if [ -f ".deps_installed" ]; then
    rm ".deps_installed"
    echo "已清理旧的安装标记"
fi

echo "步骤1：检查Python环境..."

# 检查系统Python
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "错误：未找到Python！"
    echo
    echo "请先安装Python 3.8或更高版本："
    echo "Ubuntu/Debian: sudo apt install python3 python3-pip python3-venv"
    echo "CentOS/RHEL: sudo yum install python3 python3-pip"
    echo "Arch Linux: sudo pacman -S python python-pip"
    echo
    read -p "按任意键退出..."
    exit 1
fi

# 优先使用python3，如果没有则使用python
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
else
    PYTHON_CMD="python"
fi

PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | cut -d' ' -f2)
echo "✅ 找到Python $PYTHON_VERSION"

echo
echo "步骤2：创建虚拟环境..."

# 删除现有虚拟环境（如果存在）
if [ -d ".venv" ]; then
    echo " 删除现有虚拟环境..."
    rm -rf ".venv"
fi

# 创建新的虚拟环境
echo "创建新的虚拟环境..."
$PYTHON_CMD -m venv .venv

if [ $? -ne 0 ]; then
    echo "❌ 虚拟环境创建失败！"
    echo
    echo "可能的原因："
    echo "- Python版本过低（需要3.8+）"
    echo "- 磁盘空间不足"
    echo "- 权限不足"
    echo "- 缺少python3-venv包"
    echo
    echo "建议："
    echo "- Ubuntu/Debian: sudo apt install python3-venv"
    echo "- 或尝试使用sudo运行此脚本"
    read -p "按任意键退出..."
    exit 1
fi

echo "✅ 虚拟环境创建成功"

# 检查虚拟环境
VENV_PATH="$SCRIPT_DIR/.venv"
PYTHON_PATH="$VENV_PATH/bin/python"
PIP_PATH="$VENV_PATH/bin/pip"

if [ ! -f "$PYTHON_PATH" ]; then
    echo "❌ 虚拟环境验证失败！"
    read -p "按任意键退出..."
    exit 1
fi

echo
echo "步骤3：安装依赖包..."
echo

SUCCESS_COUNT=0
TOTAL_COUNT=0

for dir in "Bot" "Adapter" "Matcha-Adapter"; do
    if [ -f "$dir/requirements.txt" ]; then
        TOTAL_COUNT=$((TOTAL_COUNT + 1))
        echo "正在安装 $dir 的依赖包..."
        
        # 显示requirements.txt内容预览
        echo "   依赖文件：$dir/requirements.txt"
        
        "$PIP_PATH" install -r "$dir/requirements.txt" --no-cache-dir --disable-pip-version-check
        
        if [ $? -eq 0 ]; then
            echo "✅ $dir 依赖包安装完成"
            SUCCESS_COUNT=$((SUCCESS_COUNT + 1))
        else
            echo "❌ $dir 依赖包安装失败"
            echo "   请检查网络连接或依赖包是否存在问题"
        fi
        echo
    else
        echo " 未找到 $dir/requirements.txt，跳过"
    fi
done

echo "安装总结："
echo "   成功：$SUCCESS_COUNT/$TOTAL_COUNT 个模块"
echo

if [ $SUCCESS_COUNT -lt $TOTAL_COUNT ]; then
    echo " 部分依赖安装失败，但可以继续使用"
    echo "   如遇到问题，请重新运行此脚本"
else
    echo "✅ 所有依赖安装完成！"
fi

# 创建安装完成标记
echo "Environment initialized on $(date)" > ".deps_installed"
echo "Python: $PYTHON_VERSION" >> ".deps_installed"
echo "Modules: $SUCCESS_COUNT/$TOTAL_COUNT" >> ".deps_installed"

echo
echo "步骤4：启动主程序..."
echo

# 直接启动主程序
"$PYTHON_PATH" onekey_linux.py

echo
echo "========================================"
echo "   MaiBot-Plus 环境配置完成！"
echo
echo "   下次使用请直接运行："
echo "   \"./启动一键包程序.sh\""
echo
echo "  如需重新配置环境，请重新运行此脚本"
echo "========================================"
echo
read -p "按任意键退出..."