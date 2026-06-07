# A股量化选股实战框架

## 概述

本框架面向有 Python 基础的投资者，提供一套完整的 A 股量化选股方法论。从数据获取、因子构建、策略回测到实盘执行，每一环节都配有可运行的代码。学习完本框架后，你将能独立搭建一套日均 30 分钟维护的半自动选股系统。

**适用人群**：有 Python 基础，想用量化方法替代主观选股的投资者。
**先修知识**：Python pandas、numpy 基础，了解股票基本概念（开盘价、收盘价、成交量）。
**交付内容**：本知识包 + 附赠 5 个可直接运行的 Python 策略脚本。

---

## 第一章：量化选股的核心逻辑

### 1.1 为什么量化

主观选股的三个致命缺陷：

1. **确认偏误**：买入后只看利好消息，忽略风险信号
2. **情绪干扰**：恐慌时割肉，狂热时追高
3. **样本不足**：人脑能同时跟踪的股票不超过 20 只

量化选股通过 **规则化 + 全市场扫描 + 统计验证** 解决这三个问题。你不再问"这只股票好不好"，而是问"符合条件 X 的股票历史上表现如何"。

### 1.2 因子投资的基本框架

因子（Factor）就是股票的某个可量化特征。A 股市场被学术和业界反复验证的有效因子：

| 因子类别 | 具体因子 | A股有效性 | 逻辑 |
|---------|---------|----------|------|
| 动量 | 20日涨跌幅 | ★★★★ | 涨的继续涨（A股追涨特性强） |
| 反转 | 5日跌幅度 | ★★★ | 短期超跌反弹 |
| 波动率 | 20日波动率 | ★★★★ | 低波动股票长期跑赢高波动 |
| 成交量 | 量比（5日均量/20日均量） | ★★★ | 放量上涨是可靠信号 |
| 基本面 | 市盈率倒数（E/P） | ★★★ | 低估值长期有效 |
| 情绪 | 换手率变化 | ★★★ | 换手率突增预示方向变化 |

### 1.3 单因子 vs 多因子

单因子策略简单但不够稳健。专业量化采用多因子打分法：

```
综合得分 = w1 × 动量得分 + w2 × 波动率得分 + w3 × 估值得分 + w4 × 成交量得分
```

其中 w1~w4 是各因子的权重，通过历史回测确定最优配比。本框架的默认权重为：

```
w1(动量)=0.30, w2(低波动)=0.25, w3(估值)=0.25, w4(量价)=0.20
```

---

## 第二章：数据获取与预处理

### 2.1 连接 Tushare 数据源

```python
import tushare as ts
import pandas as pd
import numpy as np

# 设置你的 Tushare Token
pro = ts.pro_api("your_token_here")

# 获取全市场股票列表
df_stocks = pro.stock_basic(exchange="", list_status="L", 
    fields="ts_code,name,industry,area,list_date")
print(f"全市场上市股票：{len(df_stocks)} 只")
```

### 2.2 批量获取日线数据

A 股 5000+ 只股票，逐个请求太慢。用以下批量获取方案：

```python
def get_daily_batch(ts_codes, start_date, end_date):
    """批量获取多只股票日线数据"""
    all_data = []
    batch_size = 100  # Tushare 单次最多 100 只
    
    for i in range(0, len(ts_codes), batch_size):
        batch = ts_codes[i:i+batch_size]
        codes_str = ",".join(batch)
        df = pro.daily(ts_code=codes_str, start_date=start_date, 
                       end_date=end_date)
        all_data.append(df)
    
    return pd.concat(all_data, ignore_index=True)

# 示例：获取沪深300成分股最近60个交易日数据
# codes = ["000001.SZ", "000002.SZ", "600000.SH", ...]
# df = get_daily_batch(codes, "20260401", "20260607")
```

### 2.3 数据清洗

A 股数据常见问题及处理：

```python
def clean_stock_data(df):
    """清洗股票日线数据"""
    # 1. 去除停牌日（成交量为0）
    df = df[df["vol"] > 0].copy()
    
    # 2. 去除ST股票和上市不足60天的新股
    # ST股波动异常，新股数据不足
    
    # 3. 计算必要字段
    df["trade_date"] = pd.to_datetime(df["trade_date"])
    df = df.sort_values(["ts_code", "trade_date"])
    
    # 4. 去除涨跌停日（A股涨跌停会扭曲因子计算）
    df["is_limit_up"] = df["pct_chg"] >= 9.9
    df["is_limit_down"] = df["pct_chg"] <= -9.9
    df = df[~(df["is_limit_up"] | df["is_limit_down"])]
    
    return df
```

---

## 第三章：因子计算与标准化

### 3.1 动量因子

```python
def calc_momentum_factor(df, window=20):
    """计算动量因子：过去 N 日涨跌幅"""
    df = df.copy()
    df["ret_1d"] = df.groupby("ts_code")["pct_chg"].shift(1)
    
    # N日累计收益
    df["momentum"] = df.groupby("ts_code")["pct_chg"].transform(
        lambda x: x.rolling(window).mean()
    ) * window / 100  # 转换为累计收益率
    
    return df
```

### 3.2 低波动因子

低波动异象（Low Volatility Anomaly）：低波动股票长期跑赢高波动股票。这是全球范围内最稳健的因子之一。

```python
def calc_volatility_factor(df, window=20):
    """计算波动率因子（取倒数，波动越低得分越高）"""
    df = df.copy()
    
    # 日收益率的标准差
    df["volatility"] = df.groupby("ts_code")["pct_chg"].transform(
        lambda x: x.rolling(window).std()
    )
    
    # 低波动 = 高得分，取负值
    df["low_vol"] = -df["volatility"]
    
    return df
```

### 3.3 估值因子（需结合财务数据）

```python
def calc_valuation_factor(daily_df, basic_df):
    """计算估值因子：E/P（市盈率倒数）"""
    # basic_df 来自 stock_basic 或 daily_basic 接口
    # 这里用 daily_basic 的 pe 字段
    
    df = daily_df.merge(basic_df[["ts_code", "trade_date", "pe"]], 
                        on=["ts_code", "trade_date"], how="left")
    
    # E/P = 1/PE，PE越低E/P越高得分越高
    df["ep"] = 1 / df["pe"].replace(0, np.nan)
    df["ep"] = df["ep"].clip(0, 0.2)  # 截断极端值
    
    return df
```

### 3.4 量价因子

```python
def calc_volume_factor(df, short=5, long=20):
    """成交量因子：短期均量 / 长期均量"""
    df = df.copy()
    
    df["vol_ma5"] = df.groupby("ts_code")["vol"].transform(
        lambda x: x.rolling(short).mean()
    )
    df["vol_ma20"] = df.groupby("ts_code")["vol"].transform(
        lambda x: x.rolling(long).mean()
    )
    
    df["volume_ratio"] = df["vol_ma5"] / df["vol_ma20"]
    
    # 量价配合：放量+上涨 = 加分
    df["vol_price"] = df["volume_ratio"] * np.sign(df["pct_chg"])
    
    return df
```

### 3.5 因子标准化（极其重要）

不同因子的量纲差异巨大（例如 PE 是几十，波动率是零点几），必须标准化到同一尺度：

```python
def normalize_factors(df, factor_cols):
    """对因子进行截面标准化（cross-sectional z-score）"""
    df = df.copy()
    
    for col in factor_cols:
        # 按日期分组，每组内做 z-score 标准化
        mean = df.groupby("trade_date")[col].transform("mean")
        std = df.groupby("trade_date")[col].transform("std")
        df[f"{col}_z"] = (df[col] - mean) / std.replace(0, 1)
        
        # 去极值：限制在 ±3 标准差内
        df[f"{col}_z"] = df[f"{col}_z"].clip(-3, 3)
    
    return df
```

---

## 第四章：多因子打分与选股

### 4.1 综合得分计算

```python
def calculate_composite_score(df):
    """计算多因子综合得分"""
    # 默认权重
    weights = {
        "momentum_z": 0.30,     # 动量 30%
        "low_vol_z": 0.25,      # 低波动 25%
        "ep_z": 0.25,           # 估值 25%
        "vol_price_z": 0.20,    # 量价 20%
    }
    
    df["composite_score"] = sum(
        df[col] * weight for col, weight in weights.items()
    )
    
    return df
```

### 4.2 选股逻辑

```python
def select_stocks(df, top_n=30, min_score=1.0):
    """根据综合得分选股"""
    # 按日期分组，每组内选 Top N
    result = df.groupby("trade_date").apply(
        lambda g: g.nlargest(top_n, "composite_score")
    ).reset_index(drop=True)
    
    # 过滤掉得分过低的
    result = result[result["composite_score"] > min_score]
    
    return result[["trade_date", "ts_code", "composite_score"]]
```

---

## 第五章：回测系统

### 5.1 回测框架

```python
class SimpleBacktest:
    """简易回测框架"""
    
    def __init__(self, initial_capital=100000, commission=0.0003):
        self.initial = initial_capital
        self.capital = initial_capital
        self.commission = commission  # 万三佣金
        self.positions = {}  # {ts_code: (买入价, 股数)}
        self.records = []   # 每日记录
    
    def trade(self, date, signals, price_df):
        """
        执行交易
        signals: 当日应持有的股票代码列表
        price_df: 当日收盘价（用于模拟买入/卖出价）
        """
        current_stocks = set(self.positions.keys())
        target_stocks = set(signals)
        
        # 卖出不在目标列表中的持仓
        for code in current_stocks - target_stocks:
            if code in price_df.index:
                sell_price = price_df.loc[code, "close"]
                buy_price, shares = self.positions[code]
                profit = (sell_price - buy_price) * shares
                profit -= sell_price * shares * self.commission
                self.capital += sell_price * shares - sell_price * shares * self.commission
                del self.positions[code]
        
        # 等权买入目标股票
        cash_per_stock = self.capital / max(len(target_stocks), 1)
        for code in target_stocks - current_stocks:
            if code in price_df.index:
                buy_price = price_df.loc[code, "close"]
                shares = int(cash_per_stock / buy_price / 100) * 100  # A股100股整数倍
                if shares > 0:
                    cost = buy_price * shares * (1 + self.commission)
                    self.capital -= cost
                    self.positions[code] = (buy_price, shares)
        
        # 记录当日净值
        total_value = self.capital + sum(
            price_df.loc[c, "close"] * s if c in price_df.index else b * s
            for c, (b, s) in self.positions.items()
        )
        self.records.append({
            "date": date,
            "nav": total_value,
            "positions": len(self.positions)
        })
    
    def summary(self):
        """回测结果汇总"""
        df = pd.DataFrame(self.records)
        df["daily_return"] = df["nav"].pct_change()
        
        total_return = (df["nav"].iloc[-1] / self.initial - 1) * 100
        annual_return = (1 + total_return / 100) ** (252 / len(df)) - 1
        sharpe = df["daily_return"].mean() / df["daily_return"].std() * np.sqrt(252)
        max_drawdown = (df["nav"] / df["nav"].cummax() - 1).min() * 100
        
        print(f"总收益率: {total_return:.2f}%")
        print(f"年化收益: {annual_return*100:.2f}%")
        print(f"夏普比率: {sharpe:.2f}")
        print(f"最大回撤: {max_drawdown:.2f}%")
        
        return df
```

### 5.2 回测注意事项

- **生存者偏差**：回测时需包含已退市股票，否则结果虚高
- **未来函数**：确保因子计算只使用当日及之前的数据
- **交易成本**：A 股印花税 0.05%（卖出单边）+ 佣金 0.03% + 滑点约 0.1%

---

## 第六章：实盘执行

### 6.1 每日操作流程

```
08:30  获取前一日行情数据，计算因子得分
09:00  生成今日目标持仓列表
09:25  集合竞价结束后确认执行计划
09:30-10:00  执行开盘调仓（卖出不在列表的，买入新增的）
15:00  收盘后记录当日盈亏
```

### 6.2 风险控制规则

```python
RISK_RULES = {
    "max_position_per_stock": 0.10,   # 单只股票不超过总仓位 10%
    "max_sector_exposure": 0.30,      # 单一行业不超过 30%
    "stop_loss": -0.08,               # 单只股票止损线 -8%
    "max_drawdown_close": -0.15,      # 总回撤 15% 清仓休息
    "min_holding_days": 5,            # 最短持有 5 天（减少频繁交易）
}
```

### 6.3 策略失效的判断标准

任何量化策略都会失效。当出现以下信号时需暂停策略：

1. **连续 3 个月跑输基准指数**（如沪深300）超过 5%
2. **最大回撤突破历史回测最大回撤的 1.5 倍**
3. **月胜率降至 40% 以下**

---

## 第七章：附赠策略代码

本知识包附赠 5 个可直接运行的 Python 策略脚本：

### 策略1：双均线动量策略
5 日均线上穿 20 日均线买入，下穿卖出。适合趋势明显的市场。

### 策略2：低波动选股策略
选 20 日波动率最低的 20 只股票，月度调仓。适合震荡市和熊市。

### 策略3：多因子打分选股（本框架核心）
综合动量、波动率、估值、量价四因子，周度调仓 Top 30。

### 策略4：财报超预期策略
季报发布后，实际 EPS 超过一致预期 10% 以上的股票，持有 60 天。

### 策略5：行业轮动策略
用 ETF 替代个股，月度计算各行业动量得分，持有最强 3 个行业。

---

## 附录：常用 Tushare 接口速查

| 接口 | 用途 | 参数 |
|------|------|------|
| `pro.daily()` | 日线行情 | ts_code, start_date, end_date |
| `pro.daily_basic()` | 每日指标（PE/PB/换手率） | ts_code, trade_date |
| `pro.income()` | 利润表 | ts_code, start_date, end_date |
| `pro.balancesheet()` | 资产负债表 | ts_code, start_date, end_date |
| `pro.index_daily()` | 指数日线 | ts_code, start_date, end_date |
| `pro.fund_daily()` | 基金日线 | ts_code, start_date, end_date |

---

## 学习计划建议

| 天数 | 任务 |
|------|------|
| 第1天 | 通读全文，理解因子逻辑 |
| 第2天 | 配置 Tushare Token，跑通数据获取代码 |
| 第3天 | 运行策略1（双均线），在 10 只股票上回测 |
| 第4天 | 运行策略3（多因子），对比策略1效果 |
| 第5天 | 调参数，看哪个因子权重对结果影响最大 |
| 第6天 | 加入风险控制规则，看回撤是否改善 |
| 第7天 | 用最新数据跑一次模拟调仓，验证可行性 |

---

> **免责声明**：本框架仅供学习和研究使用，不构成投资建议。历史回测结果不代表未来收益。股市有风险，投资需谨慎。
