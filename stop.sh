#!/bin/bash

echo "=== 停止出行账本服务 ==="
echo ""

BACKEND_PIDS=$(ps aux | grep -v grep | grep "uvicorn main:app" | awk '{print $2}')
FRONTEND_PIDS=$(ps aux | grep -v grep | grep "vite.*5174" | awk '{print $2}')

if [ -z "$BACKEND_PIDS" ] && [ -z "$FRONTEND_PIDS" ]; then
    echo "✅ 没有运行中的服务"
    exit 0
fi

if [ -n "$BACKEND_PIDS" ]; then
    echo "🛑 停止后端服务..."
    for pid in $BACKEND_PIDS; do
        kill $pid 2>/dev/null && echo "  • 已停止 PID: $pid"
    done
fi

if [ -n "$FRONTEND_PIDS" ]; then
    echo "🛑 停止前端服务..."
    for pid in $FRONTEND_PIDS; do
        kill $pid 2>/dev/null && echo "  • 已停止 PID: $pid"
    done
fi

echo ""
echo "✅ 所有服务已停止"
