#!/bin/bash
# 极简时钟启动脚本

echo "正在启动极简时钟..."

# 检查 Python 是否安装
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到 Python3，请先安装 Python3"
    exit 1
fi

# 检查依赖是否安装
if ! python3 -c "import pygame" &> /dev/null; then
    echo "正在安装依赖..."
    pip3 install -r requirements.txt
fi

# 运行时钟程序
python3 clock.py

