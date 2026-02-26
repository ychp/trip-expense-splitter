# 出行账本 - 旅行费用分摊管理

一个专为旅行团队设计的费用分摊管理系统，帮助多人出行时轻松管理共同支出、自动计算每人应付金额，并提供清晰的结算建议。

## 功能特性

### 核心功能
- **行程管理** - 创建和管理多个旅行行程，支持设置行程时间、参与成员
- **钱包管理** - 每个行程独立的钱包系统，记录成员初始投入和当前余额
- **支出记录** - 记录每笔支出，支持多种分摊方式（平均分摊、按比例、自定义）
- **智能结算** - 自动计算每人应付/应收金额，提供最优结算方案

### 分摊方式
- **平均分摊** - 所有成员平均分担费用
- **按比例分摊** - 根据钱包余额比例自动计算
- **自定义分摊** - 手动设置每个人的分摊比例

### 数据分析
- **人均支出统计** - 查看每人总支出和与平均值的差异
- **分类占比分析** - 交通、住宿、餐饮等分类支出可视化
- **钱包余额追踪** - 实时查看每个成员的钱包余额和归属比例
- **结算建议** - 智能算法生成最少转账次数的结算方案

## 技术栈

### 后端
- FastAPI - 高性能Python Web框架
- SQLAlchemy - ORM数据库操作
- MySQL - 关系型数据库
- Pydantic - 数据验证

### 前端
- Vue.js 3 - 渐进式JavaScript框架
- Element Plus - Vue 3 UI组件库
- ECharts - 数据可视化图表库
- Tailwind CSS - 实用优先CSS框架

## 项目结构

```
trip-expense-splitter/
├── backend/                 # 后端目录
│   ├── app/
│   │   ├── api/            # API路由
│   │   ├── models/         # 数据模型
│   │   ├── schemas/        # Pydantic schemas
│   │   └── core/           # 核心配置
│   ├── main.py             # 应用入口
│   └── init_db.py          # 数据库初始化
├── frontend/               # 前端目录
│   ├── src/
│   │   ├── views/          # 页面组件
│   │   ├── router/         # 路由配置
│   │   └── api/            # API封装
│   └── package.json
└── README.md
```

## 快速开始

### 环境要求
- Python 3.8+
- Node.js 16+
- MySQL 5.7+

### 1. 克隆项目
```bash
git clone <repository-url>
cd trip-expense-splitter
```

### 2. 配置数据库
创建MySQL数据库：
```sql
CREATE DATABASE trip_expense DEFAULT CHARACTER SET utf8mb4;
```

### 3. 启动后端
```bash
cd backend
pip install -r requirements.txt
python init_db.py  # 初始化数据库表
python main.py     # 启动服务
```
后端API文档: http://localhost:8000/docs

### 4. 启动前端
```bash
cd frontend
npm install
npm run dev
```
前端访问地址: http://localhost:5173

## 使用指南

### 创建行程
1. 点击"新建行程"按钮
2. 输入行程名称（如"云南7日游"）
3. 设置行程时间和参与成员

### 创建钱包
1. 进入行程详情页
2. 点击"钱包配置"标签
3. 创建钱包并设置成员初始投入金额

### 记录支出
1. 进入"支出记录"页面
2. 点击"记一笔"按钮
3. 选择支出类型、金额、付款人
4. 选择分摊方式（平均/比例/自定义）

### 查看结算
1. 进入"统计分析"页面
2. 查看人均支出对比和分类占比
3. 查看"结算建议"了解谁需要向谁转账

## API端点

### 行程管理
- `GET /api/trips` - 获取行程列表
- `POST /api/trips` - 创建行程
- `GET /api/trips/{id}` - 获取行程详情
- `PUT /api/trips/{id}` - 更新行程
- `DELETE /api/trips/{id}` - 删除行程

### 成员管理
- `GET /api/members/trip/{trip_id}` - 获取行程成员
- `POST /api/members` - 添加成员
- `DELETE /api/members/{id}` - 删除成员

### 钱包管理
- `GET /api/wallets?trip_id={id}` - 获取行程钱包
- `POST /api/wallets` - 创建钱包
- `GET /api/wallets/{id}` - 获取钱包详情

### 支出记录
- `GET /api/transactions?trip_id={id}` - 获取支出记录
- `POST /api/transactions` - 创建支出记录
- `PUT /api/transactions/{id}` - 更新支出记录
- `DELETE /api/transactions/{id}` - 删除支出记录

### 统计分析
- `GET /api/stats/per-person/{trip_id}` - 人均支出统计
- `GET /api/stats/wallet-summary/{trip_id}` - 钱包汇总统计
- `GET /api/reconciliation/wallet/{wallet_id}` - 结算建议

## 数据模型

### 核心实体
- **Trip** - 行程（名称、时间、状态）
- **Member** - 成员（姓名、所属行程）
- **Wallet** - 钱包（名称、所属行程）
- **WalletMember** - 钱包成员余额（成员在特定钱包的余额）
- **Transaction** - 交易记录（支出/存款）
- **TransactionSplit** - 交易分摊（记录每人分摊金额）
- **Category** - 支出分类（交通、住宿、餐饮等）

## 开发计划

- [x] 基础项目架构搭建
- [x] 数据库模型设计
- [x] 核心API开发（行程、成员、钱包、交易）
- [x] 多种分摊方式实现
- [x] 智能结算算法
- [x] 前端页面开发
- [x] 数据可视化图表
- [x] API性能优化
- [ ] 数据导出功能
- [ ] 移动端适配
- [ ] 用户认证系统
- [ ] 多行程对比分析

## License

MIT
