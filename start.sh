#!/bin/bash

echo "=== 家庭账本平台启动脚本 ==="
echo ""

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到Python3,请先安装Python3"
    exit 1
fi

# 创建data目录
mkdir -p data

# 安装Python依赖
echo "步骤 1/3: 安装Python依赖..."
pip install -r requirements.txt

# 初始化数据库
echo ""
echo "步骤 2/3: 初始化数据库..."
cd backend
python init_db.py
cd ..

echo ""
echo "步骤 3/3: 启动服务..."
echo ""
echo "后端服务将在 http://localhost:8000 启动"
echo "API文档地址: http://localhost:8000/docs"
echo ""
echo "按 Ctrl+C 停止服务"
echo ""

# 启动后端服务
cd backend
uvicorn main:app --reload --port 8000
