# UUMit 金融数据全栈能力包

> 面向 UUMit A2A 能力交易平台的金融数据 REST API 服务。覆盖 A 股、指数、基金、期货、宏观经济六大板块，一次部署，10 个能力一键上架。

## 为什么做这个

UUMit 数据广场目前只有 **24 个 API**，金融板块仅包含 KYC 身份验证类（身份证实名、手机号三要素、银行卡三要素、风控评分）。**没有任何金融市场数据 API。**

这意味着：第一个把成体系的金融数据铺上去的人，就是品类的先行者。这也是本项目的位置。

## 能力清单

### 独立数据 API（9 个）

| # | 技能名称 | 端点 | 价格 |
|---|---------|------|------|
| 1 | A股股票基础列表 | `GET /api/v1/stock/list` | 0.5 UT/次 |
| 2 | A股日线行情 | `GET /api/v1/stock/daily` | 0.5 UT/次 |
| 3 | A股利润表查询 | `GET /api/v1/stock/income` | 0.8 UT/次 |
| 4 | A股资产负债表查询 | `GET /api/v1/stock/balance` | 0.8 UT/次 |
| 5 | 指数日线行情 | `GET /api/v1/index/daily` | 0.3 UT/次 |
| 6 | 指数成分股查询 | `GET /api/v1/index/members` | 0.3 UT/次 |
| 7 | 公募基金列表 | `GET /api/v1/fund/list` | 0.3 UT/次 |
| 8 | 期货日线行情 | `GET /api/v1/futures/daily` | 0.5 UT/次 |
| 9 | 中国宏观经济指标 | `GET /api/v1/macro/china` | 0.3 UT/次 |

### 辅助工具（1 个）

| # | 技能名称 | 端点 | 价格 |
|---|---------|------|------|
| 10 | 交易日历查询 | `GET /api/v1/calendar` | 0.1 UT/次 |

### 能力组合（1 个）

| # | 组合名称 | 端点 | 价格 | 串接的 API |
|---|---------|------|------|-----------|
| 11 | 量化投资基础数据包 | `POST /api/v1/combo/quant_basic` | 2 UT/次 | ①+②+③+④ |

## 快速开始

### 1. 环境准备

```bash
# 克隆并进入目录
cd finance-data-service

# 复制环境变量配置
cp .env.example .env
# 编辑 .env，填入你的 Tushare Token
# TUSHARE_TOKEN=你的token（注册地址: https://tushare.pro）

# 安装依赖（Python 3.9+）
pip install -r requirements.txt
```

### 2. 启动服务

```bash
cd src
python server.py
# 服务运行在 http://0.0.0.0:8800
# Swagger 文档: http://localhost:8800/docs
```

### 3. 验证端点

```bash
# 健康检查
curl http://localhost:8800/

# 获取股票列表
curl "http://localhost:8800/api/v1/stock/list?list_status=L"

# 查询平安银行日线
curl "http://localhost:8800/api/v1/stock/daily?ts_code=000001.SZ"

# 量化基础数据包（一键获取全量）
curl -X POST "http://localhost:8800/api/v1/combo/quant_basic" \
  -H "Content-Type: application/json" \
  -d '{"ts_code":"000001.SZ","days":30}'
```

### 4. 注册到 UUMit

```bash
# 设置 UUMit API Key
export UUMIT_API_KEY=你的key

# 预览注册内容（不实际提交）
python uumit/register.py --dry-run

# 正式注册所有技能
python uumit/register.py
```

## 部署到公网

服务需要公网可访问，UUMit 的 Agent 才能调用。推荐方式：

- **Railway / Render / Fly.io**：直接部署，自动获得 HTTPS 域名
- **云服务器 + Nginx**：反向代理到本地端口
- **Cloudflare Tunnel**：无需公网 IP，免费穿透

部署后将 `uumit/skills.json` 中的 `base_url` 改为你的公网地址。

## 数据覆盖

| 板块 | 来源 | 覆盖范围 |
|------|------|---------|
| A 股行情 + 基本面 | Tushare Pro | 全部沪深京上市公司 |
| 财务数据 | Tushare Pro | 2005 年至今 |
| 指数 | Tushare Pro | 沪深300/中证500/上证50 等 |
| 基金 | Tushare Pro | 场内+场外公募基金 |
| 期货 | Tushare Pro | 中金所/大商所/上期所/郑商所/能源中心 |
| 宏观经济 | Tushare Pro | GDP/CPI/PPI |

## 架构

```
finance-data-service/
├── src/
│   ├── server.py          # FastAPI 主服务（11 个端点）
│   ├── tushare_client.py  # Tushare Pro 数据源封装
│   └── cache.py           # 内存 TTL 缓存（默认 5 分钟）
├── uumit/
│   ├── skills.json        # 所有技能定义（含参数、定价、分类）
│   └── register.py        # 一键注册到 UUMit
├── docs/
│   └── openapi.yaml       # OpenAPI 3.1 规范
├── .env.example
└── requirements.txt
```

## 定价策略

- 基础查询（日线/列表/日历）：0.1–0.5 UT/次
- 财务报表（利润表/资产负债表）：0.8 UT/次
- 组合编排（一次获取4个API结果）：2 UT/次（比单独调用4次总价2.6 UT便宜23%）

## 扩展路线

- [ ] 接入 yfinance → 美股/港股数据
- [ ] 接入 akshare → 更多免费数据源
- [ ] WebSocket 实时行情推送
- [ ] 技术指标计算（MACD/RSI/布林带）
- [ ] 估值模型接口（DCF/PE/PB 对比）
- [ ] Grafana 数据看板集成
