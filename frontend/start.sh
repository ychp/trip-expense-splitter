#!/bin/bash

cd "$(dirname "$0")/.."

echo "=== 家庭账本 - 前端服务启动 ==="
echo ""

if ! command -v node &> /dev/null; then
    echo "❌ 错误: 未找到 Node.js,请先安装 Node.js"
    exit 1
fi

if ! command -v npm &> /dev/null; then
    echo "❌ 错误: 未找到 npm,请先安装 Node.js 和 npm"
    exit 1
fi

echo "📦 检查并安装依赖..."
if [ ! -d "frontend/node_modules" ]; then
    echo "安装前端依赖..."
    cd frontend
    npm install
    cd ..
fi

echo ""
echo "🚀 启动前端开发服务器..."
echo "前端地址: http://localhost:5174"
echo ""
echo "按 Ctrl+C 停止服务"
echo "============================================"
echo ""

cd frontend
npm run dev
