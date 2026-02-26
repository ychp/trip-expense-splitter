#!/bin/bash

cd "$(dirname "$0")/.."

echo "=== 家庭账本 - 后端服务启动 ==="
echo ""

if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 Python3,请先安装 Python3"
    exit 1
fi

echo "📦 检查并安装依赖..."
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
fi

source venv/bin/activate

echo "安装/更新 Python 依赖..."
pip3 install -q -r requirements.txt

echo ""
echo "🗄️  初始化数据库..."
python backend/init_db.py

echo ""
echo "🚀 启动后端服务..."
echo "后端地址: http://localhost:8001"
echo "API 文档: http://localhost:8001/docs"
echo ""
echo "按 Ctrl+C 停止服务"
echo "============================================"
echo ""

cd backend
uvicorn main:app --reload --port 8000 --host 0.0.0.0
