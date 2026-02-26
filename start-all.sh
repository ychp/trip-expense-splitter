#!/bin/bash

cd "$(dirname "$0")"

echo "=== 出行账本 - 启动所有服务 ==="
echo ""

function cleanup() {
    echo ""
    echo "============================================"
    echo "🛑 正在停止所有服务..."
    
    if [ -n "$BACKEND_PID" ]; then
        echo "停止后端服务 (PID: $BACKEND_PID)"
        kill $BACKEND_PID 2>/dev/null
    fi
    
    if [ -n "$FRONTEND_PID" ]; then
        echo "停止前端服务 (PID: $FRONTEND_PID)"
        kill $FRONTEND_PID 2>/dev/null
    fi
    
    echo "✅ 所有服务已停止"
    exit 0
}

trap cleanup SIGINT SIGTERM

echo "📦 检查依赖..."

if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 Python3"
    exit 1
fi

if ! command -v node &> /dev/null; then
    echo "❌ 错误: 未找到 Node.js"
    exit 1
fi

if ! command -v npm &> /dev/null; then
    echo "❌ 错误: 未找到 npm"
    exit 1
fi

echo "✅ 依赖检查通过"
echo ""

echo "🗄️  初始化数据库..."
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
fi

source venv/bin/activate
pip install -q -r requirements.txt
python backend/init_db.py

echo ""

if [ ! -d "frontend/node_modules" ]; then
    echo "📦 安装前端依赖..."
    cd frontend
    npm install
    cd ..
fi

echo "============================================"
echo "🚀 启动服务..."
echo "============================================"
echo ""

echo "🔧 启动后端服务..."
cd backend
python3 -m uvicorn main:app --reload --port 8000 --host 0.0.0.0 > /tmp/family-finance-backend.log 2>&1 &
BACKEND_PID=$!
cd ..

echo "⏳ 等待后端服务启动..."
sleep 3

if ps -p $BACKEND_PID > /dev/null; then
    echo "✅ 后端服务已启动 (PID: $BACKEND_PID)"
else
    echo "❌ 后端服务启动失败"
    tail -20 /tmp/family-finance-backend.log
    exit 1
fi

echo ""
echo "🎨 启动前端服务..."
cd frontend
npm run dev > /tmp/family-finance-frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..

echo "⏳ 等待前端服务启动..."
sleep 3

if ps -p $FRONTEND_PID > /dev/null; then
    echo "✅ 前端服务已启动 (PID: $FRONTEND_PID)"
else
    echo "❌ 前端服务启动失败"
    tail -20 /tmp/family-finance-frontend.log
    cleanup
fi

echo ""
echo "============================================"
echo "🎉 所有服务启动成功!"
echo "============================================"
echo ""
echo "📍 访问地址:"
echo "  • 前端应用: http://localhost:5174"
echo "  • 后端 API: http://localhost:8000"
echo "  • API 文档: http://localhost:8000/docs"
echo ""
echo "📝 日志文件:"
echo "  • 后端日志: /tmp/family-finance-backend.log"
echo "  • 前端日志: /tmp/family-finance-frontend.log"
echo ""
echo "按 Ctrl+C 停止所有服务"
echo "============================================"
echo ""

for pid in $BACKEND_PID $FRONTEND_PID; do
    wait $pid 2>/dev/null
done
