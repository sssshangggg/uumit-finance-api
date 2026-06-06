"""
Tushare Pro 数据源封装。
提供统一的查询接口和字段白名单，确保返回数据安全且标准化。
"""
import os
from typing import Optional

import pandas as pd
import tushare as ts

from .cache import cache

TOKEN = os.getenv("TUSHARE_TOKEN", "")
_pro: Optional[ts.pro_api] = None


def get_pro() -> ts.pro_api:
    global _pro
    if _pro is None:
        if not TOKEN:
            raise RuntimeError("TUSHARE_TOKEN 未设置，请在 .env 中配置")
        ts.set_token(TOKEN)
        _pro = ts.pro_api()
    return _pro


def _cached_query(func_name: str, **kwargs) -> pd.DataFrame:
    """带缓存的 Tushare 查询。"""
    cached = cache.get(func_name, kwargs)
    if cached is not None:
        return cached

    pro = get_pro()
    fn = getattr(pro, func_name, None)
    if fn is None:
        raise ValueError(f"Tushare 不支持接口: {func_name}")

    df: pd.DataFrame = fn(**kwargs)
    if df is None or df.empty:
        df = pd.DataFrame()

    cache.set(func_name, kwargs, df)
    return df


# ---- 股票接口 ----

STOCK_BASIC_FIELDS = [
    "ts_code", "name", "area", "industry", "market",
    "list_status", "list_date", "delist_date", "curr_type",
]

def query_stock_basic(ts_code: Optional[str] = None, list_status: str = "L") -> pd.DataFrame:
    kwargs = {"list_status": list_status, "fields": ",".join(STOCK_BASIC_FIELDS)}
    if ts_code:
        kwargs["ts_code"] = ts_code
    return _cached_query("stock_basic", **kwargs)


STOCK_DAILY_FIELDS = [
    "ts_code", "trade_date", "open", "high", "low", "close",
    "pre_close", "change", "pct_chg", "vol", "amount",
]

def query_daily(ts_code: str, start_date: Optional[str] = None,
                end_date: Optional[str] = None) -> pd.DataFrame:
    kwargs = {"ts_code": ts_code, "fields": ",".join(STOCK_DAILY_FIELDS)}
    if start_date:
        kwargs["start_date"] = start_date
    if end_date:
        kwargs["end_date"] = end_date
    return _cached_query("daily", **kwargs)


# ---- 财务指标 ----

INCOME_FIELDS = [
    "ts_code", "end_date", "report_type", "total_revenue",
    "revenue_qq", "n_income", "n_income_attr_p", "basic_eps", "diluted_eps",
]

def query_income(ts_code: str, start_date: Optional[str] = None,
                 end_date: Optional[str] = None) -> pd.DataFrame:
    kwargs = {"ts_code": ts_code, "fields": ",".join(INCOME_FIELDS)}
    if start_date:
        kwargs["start_date"] = start_date
    if end_date:
        kwargs["end_date"] = end_date
    return _cached_query("income", **kwargs)


BALANCE_FIELDS = [
    "ts_code", "end_date", "report_type", "total_assets",
    "total_liab", "total_hldr_eqy_exc_min_int", "undistr_porfit",
    "retained_earnings",
]

def query_balancesheet(ts_code: str, start_date: Optional[str] = None,
                        end_date: Optional[str] = None) -> pd.DataFrame:
    kwargs = {"ts_code": ts_code, "fields": ",".join(BALANCE_FIELDS)}
    if start_date:
        kwargs["start_date"] = start_date
    if end_date:
        kwargs["end_date"] = end_date
    return _cached_query("balancesheet", **kwargs)


# ---- 指数接口 ----

INDEX_DAILY_FIELDS = [
    "ts_code", "trade_date", "open", "high", "low", "close",
    "pre_close", "change", "pct_chg", "vol", "amount",
]

def query_index_daily(index_code: str, start_date: Optional[str] = None,
                       end_date: Optional[str] = None) -> pd.DataFrame:
    kwargs = {"ts_code": index_code, "fields": ",".join(INDEX_DAILY_FIELDS)}
    if start_date:
        kwargs["start_date"] = start_date
    if end_date:
        kwargs["end_date"] = end_date
    return _cached_query("index_daily", **kwargs)


INDEX_MEMBER_FIELDS = [
    "index_code", "index_name", "con_code", "con_name",
    "in_date", "out_date", "is_new",
]

def query_index_member(index_code: str, trade_date: Optional[str] = None) -> pd.DataFrame:
    kwargs = {"index_code": index_code, "fields": ",".join(INDEX_MEMBER_FIELDS)}
    if trade_date:
        kwargs["trade_date"] = trade_date
    return _cached_query("index_member", **kwargs)


# ---- 基金接口 ----

FUND_BASIC_FIELDS = [
    "ts_code", "name", "management", "custodian", "fund_type",
    "found_date", "status", "invest_type", "type", "benchmark",
]

def query_fund_basic(market: str = "E") -> pd.DataFrame:
    return _cached_query("fund_basic", market=market,
                         fields=",".join(FUND_BASIC_FIELDS))


# ---- 期货接口 ----

FUT_DAILY_FIELDS = [
    "ts_code", "trade_date", "open", "high", "low", "close",
    "pre_close", "change", "pct_chg", "vol", "amount",
]

def query_fut_daily(trade_date: Optional[str] = None,
                     ts_code: Optional[str] = None,
                     exchange: Optional[str] = None) -> pd.DataFrame:
    kwargs = {"fields": ",".join(FUT_DAILY_FIELDS)}
    if trade_date:
        kwargs["trade_date"] = trade_date
    if ts_code:
        kwargs["ts_code"] = ts_code
    if exchange:
        kwargs["exchange"] = exchange
    return _cached_query("fut_daily", **kwargs)


# ---- 宏观接口 ----

MACRO_INDICATORS = {
    "gdp": "gdp",          # 国内生产总值
    "cpi": "cpi",          # 消费者物价指数
    "ppi": "ppi",          # 生产者物价指数
    "m2": "msc_m2",        # 货币供应量M2
    "lpr": "shibor_lpr",   # 贷款市场报价利率
}

MACRO_CHINA_FIELDS = [
    "year", "quarter", "gdp", "gdp_yoy", "pi", "pi_yoy",
    "si", "si_yoy", "ti", "ti_yoy",
]

def query_macro_china(year: Optional[str] = None,
                       quarter: Optional[str] = None) -> pd.DataFrame:
    kwargs = {"fields": ",".join(MACRO_CHINA_FIELDS)}
    if year:
        kwargs["year"] = year
    if quarter:
        kwargs["quarter"] = quarter
    return _cached_query("macro_china" if not year else "macro_china", **kwargs)


# ---- 交易日历 ----

def query_trade_cal(exchange: str = "SSE", start_date: Optional[str] = None,
                     end_date: Optional[str] = None) -> pd.DataFrame:
    kwargs = {"exchange": exchange}
    if start_date:
        kwargs["start_date"] = start_date
    if end_date:
        kwargs["end_date"] = end_date
    return _cached_query("trade_cal", **kwargs)
