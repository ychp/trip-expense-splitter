# 出行账本 (Trip Expense Splitter) - AI助手指南

## 项目概述

**出行账本**是一个专为旅行团队设计的费用分摊管理系统，帮助多人出行时轻松管理共同支出、自动计算每人应付金额，并提供清晰的结算建议。

**扫描结论**（2026-02-27更新）：
- ✅ 项目采用前后端分离架构，结构清晰
- ✅ 后端使用FastAPI + SQLAlchemy + MySQL，前端使用Vue 3 + Element Plus
- ✅ 实现了完整的CRUD操作和RESTful API设计
- ✅ 支持三种分摊方式：平均分摊、按比例分摊、自定义分摊
- ✅ 智能结算算法使用贪心算法实现最少转账次数
- ✅ 提供了8个页面和完整的路由系统
- ✅ 包含统计分析模块，支持人均支出、分类占比等可视化
- ✅ 提供便捷的启动脚本（start-all.sh）
- ⚠️ 前端API调用硬编码了localhost:8000，可优化为环境变量
- ⚠️ 缺少用户认证和权限管理
- ⚠️ 缺少单元测试和集成测试

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
- **ORM**: SQLAlchemy 2.0+
- **数据库**: MySQL 5.7+
- **数据验证**: Pydantic 2.5+
- **ASGI服务器**: Uvicorn
- **数据库驱动**: PyMySQL
- **其他依赖**: python-dateutil, python-multipart, cryptography

### 前端
- **框架**: Vue.js 3.4+
- **UI组件库**: Element Plus 2.5+
- **图表库**: ECharts 5.4+
- **CSS框架**: Tailwind CSS 3.4+
- **构建工具**: Vite 5.0+
- **路由**: Vue Router 4.2+
- **HTTP客户端**: Axios 1.6+
- **图标**: @element-plus/icons-vue

## 项目结构

```
trip-expense-splitter/
├── backend/                      # 后端目录
│   ├── app/
│   │   ├── api/                 # API路由模块
│   │   │   ├── trips.py         # 行程管理API
│   │   │   ├── members.py       # 成员管理API
│   │   │   ├── wallets.py       # 钱包管理API
│   │   │   ├── transactions.py  # 交易记录API
│   │   │   ├── categories.py    # 支出分类API
│   │   │   ├── stats.py         # 统计分析API
│   │   │   ├── wallet_flows.py  # 余额流水API
│   │   │   └── reconciliation.py # 结算建议API
│   │   ├── models/              # SQLAlchemy数据模型
│   │   │   ├── trip.py          # 行程模型
│   │   │   ├── member.py        # 成员模型
│   │   │   ├── wallet.py        # 钱包模型
│   │   │   ├── wallet_member.py # 钱包成员关联
│   │   │   ├── wallet_flow.py   # 余额流水模型
│   │   │   ├── transaction.py   # 交易记录模型
│   │   │   ├── transaction_split.py # 交易分摊模型
│   │   │   ├── category.py      # 支出分类模型
│   │   │   ├── trip_stats.py    # 行程统计模型
│   │   │   ├── member_stats.py  # 成员统计模型
│   │   │   └── wallet_stats.py  # 钱包统计模型
│   │   ├── schemas/             # Pydantic验证模式
│   │   │   ├── trip.py
│   │   │   ├── member.py
│   │   │   ├── wallet.py
│   │   │   ├── wallet_flow.py
│   │   │   ├── transaction.py
│   │   │   ├── category.py
│   │   │   └── reconciliation.py
│   │   ├── services/            # 业务逻辑服务
│   │   │   └── stats_service.py # 统计服务
│   │   └── core/                # 核心配置
│   │       ├── config.py        # 配置文件
│   │       └── database.py      # 数据库会话
│   ├── main.py                  # FastAPI应用入口
│   ├── init_db.py               # 数据库初始化脚本
│   ├── init_stats.py            # 统计数据初始化
│   ├── migrate_stats_tables.py  # 统计表迁移脚本
│   ├── check_storage.py         # 存储检查脚本
│   ├── start.sh                 # 后端启动脚本
│   └── .env.example             # 环境变量示例
├── frontend/                    # 前端目录
│   ├── src/
│   │   ├── views/               # Vue页面组件
│   │   │   ├── Dashboard.vue    # 仪表盘（首页）
│   │   │   ├── Trips.vue        # 行程列表
│   │   │   ├── TripDetail.vue   # 行程详情
│   │   │   ├── Members.vue      # 成员管理
│   │   │   ├── Wallets.vue      # 钱包管理
│   │   │   ├── Transactions.vue # 交易记录
│   │   │   ├── Categories.vue   # 分类管理
│   │   │   └── Statistics.vue   # 统计分析
│   │   ├── router/              # 路由配置
│   │   │   └── index.js         # 路由定义
│   │   ├── api/                 # API调用封装
│   │   │   ├── index.js         # Axios实例配置
│   │   │   ├── categories.js    # 分类API
│   │   │   └── transactions.js  # 交易API
│   │   ├── App.vue              # 根组件
│   │   ├── main.js              # 应用入口
│   │   └── style.css            # 全局样式
│   ├── index.html               # HTML模板
│   ├── vite.config.js           # Vite配置
│   ├── tailwind.config.js       # Tailwind CSS配置
│   ├── postcss.config.js        # PostCSS配置
│   ├── package.json             # NPM依赖配置
│   └── start.sh                 # 前端启动脚本
├── start-all.sh                 # 一键启动所有服务
├── stop.sh                      # 停止所有服务
├── status.sh                    # 查看服务状态
├── requirements.txt             # Python依赖
├── AGENTS.md                    # AI助手指南（本文件）
├── README.md                    # 项目说明文档
└── LICENSE                      # 开源协议
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

### 已实现的API端点

**行程管理** (`/api/trips`)
- `GET /api/trips/` - 获取所有行程
- `POST /api/trips/` - 创建新行程
- `GET /api/trips/{id}` - 获取行程详情
- `PUT /api/trips/{id}` - 更新行程
- `DELETE /api/trips/{id}` - 删除行程

**成员管理** (`/api/members`)
- `GET /api/members/trip/{trip_id}` - 获取行程所有成员
- `POST /api/members/` - 添加成员
- `DELETE /api/members/{id}` - 删除成员

**钱包管理** (`/api/wallets`)
- `GET /api/wallets/` - 获取钱包列表（支持trip_id查询）
- `POST /api/wallets/` - 创建钱包
- `GET /api/wallets/{id}` - 获取钱包详情
- `PUT /api/wallets/{id}` - 更新钱包
- `DELETE /api/wallets/{id}` - 删除钱包

**交易记录** (`/api/transactions`)
- `GET /api/transactions/` - 获取交易列表（支持trip_id, wallet_id查询）
- `POST /api/transactions/` - 创建交易记录
- `GET /api/transactions/{id}` - 获取交易详情
- `PUT /api/transactions/{id}` - 更新交易记录
- `DELETE /api/transactions/{id}` - 删除交易记录

**支出分类** (`/api/categories`)
- `GET /api/categories/` - 获取所有分类
- `POST /api/categories/` - 创建分类
- `DELETE /api/categories/{id}` - 删除分类

**统计分析** (`/api/stats`)
- `GET /api/stats/per-person/{trip_id}` - 人均支出统计
- `GET /api/stats/wallet-summary/{wallet_id}` - 钱包汇总统计

**余额流水** (`/api/wallet-flows`)
- `GET /api/wallet-flows/wallet/{wallet_id}` - 获取钱包流水记录

**结算建议** (`/api/reconciliation`)
- `GET /api/reconciliation/wallet/{wallet_id}` - 钱包结算建议
- `GET /api/reconciliation/trip/{trip_id}` - 行程结算建议
- `GET /api/reconciliation/settlements/{wallet_id}` - 获取结算列表

### 前端路由

| 路径 | 名称 | 组件 | 说明 |
|------|------|------|------|
| `/` | Dashboard | Dashboard.vue | 仪表盘首页，显示行程概览和最近支出 |
| `/trips` | Trips | Trips.vue | 行程列表页面 |
| `/trips/:id` | TripDetail | TripDetail.vue | 行程详情页面 |
| `/transactions` | Transactions | Transactions.vue | 交易记录列表 |
| `/statistics` | Statistics | Statistics.vue | 统计分析页面 |
| `/wallets` | Wallets | Wallets.vue | 钱包管理页面 |
| `/categories` | Categories | Categories.vue | 支出分类管理页面 |

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

### 一键启动所有服务
```bash
./start-all.sh
```
该脚本会自动：
1. 检查Python和Node.js环境
2. 创建Python虚拟环境并安装依赖
3. 初始化数据库
4. 启动后端服务（端口8000）
5. 启动前端服务（端口5173或5174）

### 单独启动后端
```bash
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 单独启动前端
```bash
cd frontend
npm run dev
```

### 访问地址
- 前端应用: http://localhost:5173 (或5174)
- 后端API: http://localhost:8000
- API文档: http://localhost:8000/docs
- 健康检查: http://localhost:8000/health

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

## 架构设计要点

### 分层架构
项目采用经典的三层架构：

**表示层（Presentation Layer）**
- Vue.js 3组件负责UI展示和用户交互
- Vue Router管理单页应用路由
- Axios封装HTTP请求

**业务逻辑层（Business Logic Layer）**
- FastAPI路由处理器（app/api/）
- Services层封装复杂业务逻辑（app/services/）
- Pydantic schemas负责数据验证

**数据访问层（Data Access Layer）**
- SQLAlchemy ORM映射数据库表
- Database session管理（app/core/database.py）
- 模型定义（app/models/）

### 关键设计模式

**依赖注入**
```python
# FastAPI依赖注入获取数据库会话
from app.core.database import get_db

@router.get("/trips/{id}")
def get_trip(id: int, db: Session = Depends(get_db)):
    return db.query(Trip).filter(Trip.id == id).first()
```

**Repository模式**
- SQLAlchemy session作为Repository
- 统一的CRUD操作接口

**DTO模式**
- Pydantic schemas作为数据传输对象
- 自动验证请求数据

### 结算算法详解

项目使用**贪心算法**实现智能结算：

```python
def calculate_settlements(wallet_members, db):
    # 1. 计算平均余额
    total_balance = sum(wm.balance for wm in wallet_members)
    avg_balance = total_balance / len(wallet_members)
    
    # 2. 分组：欠款人 vs 收款人
    debtors = []    # 余额 < 平均值
    creditors = []  # 余额 > 平均值
    
    # 3. 排序：按金额降序
    debtors_sorted = sorted(debtors, key=lambda x: x["debt_amount"], reverse=True)
    creditors_sorted = sorted(creditors, key=lambda x: x["credit_amount"], reverse=True)
    
    # 4. 配对：贪心匹配
    while debtors and creditors:
        amount = min(debtor["debt_amount"], creditor["credit_amount"])
        # 记录转账建议
        settlements.append({"from": debtor, "to": creditor, "amount": amount})
```

**算法优势**：
- 最小化转账次数
- 时间复杂度 O(n log n)
- 适合小规模团队（<20人）

### 数据库设计亮点

**统计数据预计算**
- `trip_stats`, `member_stats`, `wallet_stats` 表
- 避免实时聚合查询
- 提升统计API响应速度

**余额流水追踪**
- `wallet_flows` 表记录每次余额变更
- 支持审计和历史追溯
- 便于排查计算错误

**交易分摊表**
- `transaction_splits` 支持多维度分摊
- 灵活支持equal/ratio/custom三种模式
- 每笔分摊独立记录

---

**最后更新**: 2026-02-27
**版本**: 1.0.0
