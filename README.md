# UUMit 金融数据全栈能力包

> 面向 [UUMit](https://uumit.com) A2A 能力交易平台的金融数据 REST API 服务。
> 覆盖 A 股、指数、基金、期货、宏观经济，10 个技能一键上架，Agent 自动接单赚钱。

## 快速开始（3 步）

### 1. 拿 Tushare Token

访问 [tushare.pro/register](https://tushare.pro/register) 注册账号，
登录后进入「个人主页 → 接口TOKEN」，复制 token。

编辑 `finance-data-service/.env`：
```
TUSHARE_TOKEN=你的token粘贴在这里
```

### 2. 部署服务

**Docker 部署（推荐）：**
```bash
cd finance-data-service
docker compose up -d --build
```

**VPS 一键部署：**
```bash
cd finance-data-service
bash deploy.sh
```

**Render 一键部署：**
把项目推送到 GitHub，在 [render.com](https://render.com) 连接仓库即可（已配好 `render.yaml`）。

### 3. 上架 UUMit

```bash
cd finance-data-service
# 预览
python uumit/register.py --dry-run
# 正式注册（需设置 UUMIT_API_KEY 环境变量）
python uumit/register.py
```

## 11 个能力 + 定价

| 技能 | 端点 | 价格/次 |
|------|------|---------|
| A股基础列表 | `/api/v1/stock/list` | 0.5 UT |
| A股日线行情 | `/api/v1/stock/daily` | 0.5 UT |
| 利润表 | `/api/v1/stock/income` | 0.8 UT |
| 资产负债表 | `/api/v1/stock/balance` | 0.8 UT |
| 指数日线 | `/api/v1/index/daily` | 0.3 UT |
| 指数成分股 | `/api/v1/index/members` | 0.3 UT |
| 基金列表 | `/api/v1/fund/list` | 0.3 UT |
| 期货日线 | `/api/v1/futures/daily` | 0.5 UT |
| 宏观经济 | `/api/v1/macro/china` | 0.3 UT |
| 交易日历 | `/api/v1/calendar` | 0.1 UT |
| **量化数据包**（组合） | `/api/v1/combo/quant_basic` | **2 UT** |

## 项目结构

```
UUMit/
├── README.md                ← 你在这里
└── finance-data-service/
    ├── src/
    │   ├── server.py        ← FastAPI 主服务
    │   ├── tushare_client.py ← 数据源
    │   └── cache.py         ← 缓存层
    ├── uumit/
    │   ├── skills.json      ← 技能定义
    │   └── register.py      ← 一键上架
    ├── Dockerfile
    ├── docker-compose.yml
    ├── render.yaml          ← Render 部署配置
    ├── deploy.sh            ← VPS 部署脚本
    └── .env                 ← 放 Tushare Token
```
