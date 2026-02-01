#!/bin/bash

cd "$(dirname "$0")"

if [ ! -d "venv" ]; then
    echo "❌ 虚拟环境未找到，正在创建..."
    if command -v python3.12 &> /dev/null; then
        python3.12 -m venv venv
    else
        python3 -m venv venv
    fi
    
    source venv/bin/activate
    
    echo "⬇️ 正在安装依赖..."
    pip install --upgrade pip
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

echo "🚀 启动 KiroProxy..."
python run.py