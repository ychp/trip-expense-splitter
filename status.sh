#!/bin/bash

echo "=== 出行账本服务状态 ==="
echo ""

BACKEND_RUNNING=false
FRONTEND_RUNNING=false

BACKEND_PID=$(ps aux | grep -v grep | grep "uvicorn main:app" | awk '{print $2}')
FRONTEND_PID=$(ps aux | grep -v grep | grep "vite.*5174" | awk '{print $2}')

if [ -n "$BACKEND_PID" ]; then
    BACKEND_RUNNING=true
    BACKEND_PORT=$(lsof -p $BACKEND_PID 2>/dev/null | grep LISTEN | awk '{print $9}' | head -1)
fi

if [ -n "$FRONTEND_PID" ]; then
    FRONTEND_RUNNING=true
    FRONTEND_PORT=$(lsof -p $FRONTEND_PID 2>/dev/null | grep LISTEN | awk '{print $9}' | head -1)
fi

echo "后端服务:"
if [ "$BACKEND_RUNNING" = true ]; then
    echo "  状态: ✅ 运行中"
    echo "  PID: $BACKEND_PID"
    echo "  地址: ${BACKEND_PORT:-http://localhost:8000}"
else
    echo "  状态: ❌ 未运行"
fi

echo ""
echo "前端服务:"
if [ "$FRONTEND_RUNNING" = true ]; then
    echo "  状态: ✅ 运行中"
    echo "  PID: $FRONTEND_PID"
    echo "  地址: ${FRONTEND_PORT:-http://localhost:5174}"
else
    echo "  状态: ❌ 未运行"
fi

echo ""
echo "============================================"

if [ "$BACKEND_RUNNING" = true ] || [ "$FRONTEND_RUNNING" = true ]; then
    echo "📝 快捷命令:"
    echo "  • 查看后端日志: tail -f /tmp/family-finance-backend.log"
    echo "  • 查看前端日志: tail -f /tmp/family-finance-frontend.log"
    echo "  • 停止所有服务: ./stop.sh"
fi
