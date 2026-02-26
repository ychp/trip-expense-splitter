# 出行账本 (Trip Expense Splitter) - AI助手指南

## 项目概述

**出行账本**是一个专为旅行团队设计的费用分摊管理系统，帮助多人出行时轻松管理共同支出、自动计算每人应付金额，并提供清晰的结算建议。

### 核心功能
- 行程管理（创建、编辑、删除行程）
- 成员管理（添加、删除行程成员）
- 钱包管理（记录成员初始投入和当前余额）
- 支出记录（支持多种分摊方式）
- 智能结算（自动计算最优结算方案）
- 数据分析（人均支出、分类占比、趋势分析）

## 技术栈

### 后端
- **框架**: FastAPI (Python 3.8+)
- **ORM**: SQLAlchemy
- **数据库**: MySQL 5.7+
- **数据验证**: Pydantic

### 前端
- **框架**: Vue.js 3
- **UI组件库**: Element Plus
- **图表库**: ECharts
- **CSS框架**: Tailwind CSS
- **构建工具**: Vite

## 项目结构

```
trip-expense-splitter/
├── backend/                 # 后端目录
│   ├── app/
│   │   ├── api/            # API路由
│   │   │   ├── trips.py    # 行程管理API
│   │   │   ├── members.py  # 成员管理API
│   │   │   ├── wallets.py  # 钱包管理API
│   │   │   ├── transactions.py  # 交易记录API
│   │   │   ├── stats.py    # 统计分析API
│   │   │   └── reconciliation.py  # 结算API
│   │   ├── models/         # 数据模型
│   │   │   ├── trip.py
│   │   │   ├── member.py
│   │   │   ├── wallet.py
│   │   │   ├── wallet_member.py
│   │   │   ├── transaction.py
│   │   │   ├── transaction_split.py
│   │   │   └── category.py
│   │   ├── schemas/        # Pydantic schemas
│   │   └── core/           # 核心配置
│   │       └── database.py # 数据库配置
│   ├── main.py             # 应用入口
│   └── init_db.py          # 数据库初始化
├── frontend/               # 前端目录
│   ├── src/
│   │   ├── views/          # 页面组件
│   │   │   ├── Dashboard.vue
│   │   │   ├── TripDetail.vue
│   │   │   ├── Wallets.vue
│   │   │   ├── Transactions.vue
│   │   │   └── Statistics.vue
│   │   ├── router/         # 路由配置
│   │   └── api/            # API封装
│   └── package.json
└── README.md
```

## 数据模型关系

```
Trip (行程)
├── Members (成员) 1:N
├── Wallets (钱包) 1:N
│   └── WalletMembers (钱包成员余额) 1:N
└── Transactions (交易记录) 1:N
    └── TransactionSplits (交易分摊) 1:N
```

## 核心业务流程

### 1. 创建行程
1. 用户创建行程（名称、描述、时间）
2. 添加行程成员
3. 创建行程钱包
4. 成员向钱包存入初始金额

### 2. 记录支出
1. 选择支出分类（交通、住宿、餐饮等）
2. 输入金额和付款人
3. 选择分摊方式：
   - **equal**: 平均分摊给所有成员
   - **ratio**: 按钱包余额比例分摊
   - **custom**: 自定义每人分摊比例
4. 系统自动计算每人分摊金额
5. 更新钱包余额和余额流水

### 3. 智能结算
1. 计算每人总支出
2. 计算平均值
3. 计算每人应付/应收金额
4. 生成最优结算方案（最少转账次数）

## API设计规范

### RESTful API
- `GET /api/{resource}` - 列表查询
- `POST /api/{resource}` - 创建资源
- `GET /api/{resource}/{id}` - 获取详情
- `PUT /api/{resource}/{id}` - 更新资源
- `DELETE /api/{resource}/{id}` - 删除资源

### 响应格式
```json
{
  "data": {},
  "message": "success",
  "code": 200
}
```

## 开发规范

### 后端规范
1. 使用Pydantic进行数据验证
2. 使用SQLAlchemy ORM操作数据库
3. API路由使用依赖注入获取数据库会话
4. 异常处理统一返回HTTPException

### 前端规范
1. 使用Composition API编写Vue组件
2. 使用Element Plus组件库
3. 使用Tailwind CSS进行样式设计
4. API调用使用axios封装

## 性能优化

### 已实施
- 数据库索引优化
- API查询优化（避免N+1问题）
- SQL聚合查询替代Python循环
- 内存缓存（统计API）

### 待优化
- Redis缓存
- 数据库连接池
- 前端懒加载

## 常见问题

### Q: 钱包余额如何计算？
A: 钱包余额 = 初始存入 - 支出分摊 + 其他成员转入

### Q: 分摊方式如何工作？
A: 
- **平均分摊**: 金额 ÷ 成员数
- **按比例分摊**: 金额 × (个人余额 / 总余额)
- **自定义分摊**: 手动设置每人比例

### Q: 结算算法原理？
A: 使用贪心算法，将欠款最多的人与收款最多的人配对，直到所有债务清零。

## 开发环境

### 启动后端
```bash
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 启动前端
```bash
cd frontend
npm run dev
```

### 访问地址
- 前端: http://localhost:5173
- 后端API: http://localhost:8000
- API文档: http://localhost:8000/docs

## 测试数据

Demo行程（ID: 5）包含：
- 行程: 云南7日游
- 成员: 张三、李四、王五、赵六
- 钱包: 旅行基金（余额¥7,750）
- 支出: 8笔交易记录
- 分类: 交通、住宿、餐饮、门票、购物、娱乐

## 贡献指南

1. Fork项目
2. 创建功能分支
3. 提交代码
4. 创建Pull Request

## 联系方式

如有问题，请通过GitHub Issues反馈。

---

**最后更新**: 2025-02-26
**版本**: 1.0.0
