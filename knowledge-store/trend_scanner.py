# TrendScanner — A股短线量化信号检测
# 检测两种买入形态：箱体突破 + MA5 回踩
# 依赖：pandas，数据源接 Tushare / AKShare

import pandas as pd
import numpy as np

def trend_scan(df: pd.DataFrame, commission: float = 0.0003, slippage: float = 0.001):
    """
    对单只股票的日线数据检测买入信号。

    参数:
        df: DataFrame, 需含 open/high/low/close/volume 列，按日期升序
        commission: 手续费率，默认万三
        slippage: 滑点，默认 0.1%

    返回:
        list[dict]: 信号列表，含 date/type/strength/entry_price/stop_loss
    """

    df = df.copy()
    df["ma5"] = df["close"].rolling(5).mean()
    df["ma20"] = df["close"].rolling(20).mean()
    df["vol_ma5"] = df["volume"].rolling(5).mean()
    df["ret"] = df["close"].pct_change()
    df["high_15d"] = df["high"].rolling(15).max()

    signals = []

    for i in range(20, len(df)):
        row = df.iloc[i]
        prev = df.iloc[i - 1]

        # ====== 形态 A: 箱体突破 ======
        recent_15 = df.iloc[i - 14 : i + 1]
        big_up = (recent_15["ret"] > 0.07).any()
        cum_ret = (1 + recent_15["ret"]).prod() - 1

        if big_up or cum_ret > 0.15:
            high_recent = recent_15["high"].max()
            breakout = row["close"] > high_recent or row["ret"] > 0.05
            volume_ok = row["volume"] > row["vol_ma5"] * 1.15

            if breakout:
                strength = 0.88 if volume_ok else 0.65
                entry = row["close"] * (1 + slippage)
                stop = entry * 0.95
                signals.append({
                    "date": str(df.index[i])[:10],
                    "type": "box_breakout",
                    "strength": round(strength, 2),
                    "entry_price": round(entry, 2),
                    "stop_loss": round(stop, 2),
                    "has_volume": volume_ok,
                })

        # ====== 形态 B: MA5 回踩 ======
        ma5_up = row["ma5"] > row["ma20"]
        near_ma5 = abs(row["close"] - row["ma5"]) / row["ma5"] < 0.02

        # 近10日触碰MA5次数
        touch_count = 0
        for j in range(max(0, i - 9), i + 1):
            r = df.iloc[j]
            if abs(r["low"] - r["ma5"]) / r["ma5"] < 0.01:
                touch_count += 1

        rebound = row["low"] <= row["ma5"] * 1.01 and row["close"] > row["open"]
        rebound_pct = (row["close"] - row["low"]) / row["low"] if row["low"] > 0 else 0

        if ma5_up and near_ma5 and touch_count <= 2 and rebound and rebound_pct > 0.015:
            strength = 0.85 if touch_count <= 2 else 0.70
            entry = row["close"] * (1 + slippage)
            stop = entry * 0.97
            signals.append({
                "date": str(df.index[i])[:10],
                "type": "ma5_pullback",
                "strength": round(strength, 2),
                "entry_price": round(entry, 2),
                "stop_loss": round(stop, 2),
                "touch_count": touch_count,
            })

    # 扣除手续费
    for s in signals:
        s["entry_price"] = round(s["entry_price"] * (1 + commission), 2)

    return signals


# ====== 使用示例 ======
if __name__ == "__main__":
    # 从 Tushare 获取数据
    # import tushare as ts
    # ts.set_token("your_token")
    # pro = ts.pro_api()
    # df = pro.daily(ts_code="000001.SZ", start_date="20260101", end_date="20260607")
    # df = df.sort_values("trade_date")

    # 用模拟数据演示
    np.random.seed(42)
    dates = pd.date_range("2026-01-01", periods=60, freq="B")
    base = 100
    prices = [base]
    for _ in range(59):
        prices.append(prices[-1] * (1 + np.random.normal(0.001, 0.02)))
    df = pd.DataFrame({
        "open":  [p * (1 + np.random.normal(0, 0.005)) for p in prices],
        "high":  [p * (1 + abs(np.random.normal(0, 0.01))) for p in prices],
        "low":   [p * (1 - abs(np.random.normal(0, 0.01))) for p in prices],
        "close": prices,
        "volume": np.random.randint(1e7, 5e8, 60),
    }, index=dates)

    signals = trend_scan(df)
    for s in signals:
        print(f"{s['date']} | {s['type']:15s} | 强度={s['strength']} | 入场={s['entry_price']} | 止损={s['stop_loss']}")
