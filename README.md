# 家庭账本平台

一个基于 Python + FastAPI + Vue.js 的家庭财务管理系统。

## 功能特性

- 账户管理 - 支持多种账户类型(现金、银行卡、支付宝、微信等)
- 收支流水录入 - 快速记录日常收入和支出
- 分类管理 - 灵活的分类体系,支持自定义
- 统计分析 - 多维度数据分析和可视化
- 报表导出 - 导出Excel进行进一步分析

## 技术栈

### 后端
- FastAPI - 现代化的Python Web框架
- SQLAlchemy - ORM数据库操作
- SQLite - 轻量级数据库
- Pydantic - 数据验证

### 前端
- Vue.js 3 - 渐进式JavaScript框架
- Element Plus - Vue 3 UI组件库
- ECharts - 数据可视化图表库

## 项目结构

```
family-finance/
├── backend/                 # 后端目录
│   ├── app/
│   │   ├── api/            # API路由
│   │   ├── models/         # 数据模型
│   │   ├── schemas/        # Pydantic schemas
│   │   └── core/           # 核心配置
│   ├── main.py             # 应用入口
│   └── init_db.py          # 数据库初始化
├── frontend/               # 前端目录
└── data/                   # SQLite数据库文件
```

## 快速开始

### 1. 安装Python依赖

```bash
cd backend
pip install -r ../requirements.txt
```

### 2. 初始化数据库

```bash
cd backend
python init_db.py
```

### 3. 启动后端服务

```bash
cd backend
uvicorn main:app --reload --port 8000
```

后端API文档: http://localhost:8000/docs

### 4. 安装前端依赖

```bash
cd frontend
npm install
```

### 5. 启动前端服务

```bash
cd frontend
npm run dev
```

前端访问地址: http://localhost:5173

## API端点

### 账户管理
- GET /api/accounts - 获取账户列表
- POST /api/accounts - 创建账户
- PUT /api/accounts/{id} - 更新账户
- DELETE /api/accounts/{id} - 删除账户

### 分类管理
- GET /api/categories - 获取分类列表
- POST /api/categories - 创建分类
- PUT /api/categories/{id} - 更新分类
- DELETE /api/categories/{id} - 删除分类

### 流水管理
- GET /api/transactions - 获取流水列表
- POST /api/transactions - 创建流水
- PUT /api/transactions/{id} - 更新流水
- DELETE /api/transactions/{id} - 删除流水

### 统计分析
- GET /api/statistics/summary - 收支汇总
- GET /api/statistics/by-category - 分类统计
- GET /api/statistics/trend - 趋势分析
- GET /api/statistics/accounts - 账户统计

## 开发计划

- [x] 基础项目架构搭建
- [x] 数据库模型设计
- [x] 核心API开发
- [x] 数据统计分析
- [ ] 前端页面开发
- [ ] 数据可视化图表
- [ ] 数据导出功能
- [ ] 移动端适配

## License

MIT
