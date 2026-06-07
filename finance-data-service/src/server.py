"""
UUMit 金融数据服务 — FastAPI 主服务
提供 9 个独立数据 API + 1 个组合编排端点
"""
import os
from datetime import date, timedelta
from typing import Optional

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import pandas as pd

from . import tushare_client as tc
from .content_tools import detect_ai_text, verify_viral, fetch_hot_topics

app = FastAPI(
    title="UUMit Finance Data Service",
    description="面向 UUMit A2A 能力网络的金融数据 REST API。覆盖 A 股、指数、基金、期货、宏观经济。",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# -- 全局异常处理 --

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    msg = str(exc)
    if "频率超限" in msg or "frequency" in msg.lower():
        return JSONResponse(
            status_code=429,
            content={"error": "rate_limited", "detail": msg},
        )
    if "token" in msg.lower() or "凭证" in msg or "权限" in msg:
        return JSONResponse(
            status_code=403,
            content={"error": "auth_error", "detail": msg},
        )
    return JSONResponse(
        status_code=500,
        content={"error": "internal_error", "detail": msg},
    )


# ── 工具函数 ──────────────────────────────────────────

def _df_to_records(df: pd.DataFrame) -> list[dict]:
    if df is None or df.empty:
        return []
    df = df.replace({float('nan'): None, float('inf'): None, float('-inf'): None})
    return df.to_dict(orient="records")

def _default_dates(days_back: int = 30):
    end = date.today().strftime("%Y%m%d")
    start = (date.today() - timedelta(days=days_back)).strftime("%Y%m%d")
    return start, end

class HealthResponse(BaseModel):
    status: str
    version: str

class ComboQuantRequest(BaseModel):
    ts_code: str = Field(..., description="股票代码，如 000001.SZ", examples=["000001.SZ"])
    days: int = Field(30, ge=1, le=365, description="回溯天数")

class ComboQuantResponse(BaseModel):
    ts_code: str
    stock_info: Optional[dict] = None
    daily_bars: list = []
    income: list = []
    balance: list = []


# ── 元信息 ────────────────────────────────────────────

@app.get("/", response_model=HealthResponse)
def root():
    return {"status": "ok", "version": "1.0.0"}


# ── ① 股票列表 ──────────────────────────────────────

@app.get("/api/v1/stock/list", tags=["股票"],
          summary="获取 A 股股票基础列表",
          description="返回沪深京全部（或按状态过滤）的股票代码、名称、行业、地区等基础信息。")
def stock_list(
    list_status: str = Query("L", description="上市状态: L=上市 D=退市 P=暂停上市"),
    ts_code: Optional[str] = Query(None, description="指定股票代码，如 000001.SZ"),
):
    df = tc.query_stock_basic(ts_code=ts_code, list_status=list_status)
    return {"count": len(df), "data": _df_to_records(df)}


# ── ② 日线行情 ──────────────────────────────────────

@app.get("/api/v1/stock/daily", tags=["股票"],
          summary="获取股票日线行情",
          description="返回指定股票的开高低收、涨跌幅、成交量、成交额。默认最近 30 个交易日。")
def stock_daily(
    ts_code: str = Query(..., description="股票代码"),
    start_date: Optional[str] = Query(None, description="起始日期 YYYYMMDD"),
    end_date: Optional[str] = Query(None, description="结束日期 YYYYMMDD"),
):
    if not start_date:
        start_date, end_date = _default_dates(30)
    elif not end_date:
        end_date = date.today().strftime("%Y%m%d")
    df = tc.query_daily(ts_code, start_date, end_date)
    return {"ts_code": ts_code, "count": len(df), "data": _df_to_records(df)}


# ── ③ 基本面 ──────────────────────────────────────────

@app.get("/api/v1/stock/basic", tags=["股票"],
          summary="获取股票基本信息（单一股票）",
          description="返回单只股票的名称、行业、地区、上市日期等。")
def stock_basic(ts_code: str = Query(..., description="股票代码")):
    df = tc.query_stock_basic(ts_code=ts_code)
    if df.empty:
        raise HTTPException(404, f"未找到股票: {ts_code}")
    return {"data": _df_to_records(df)[0]}


# ── ④ 财务利润表 ──────────────────────────────────────

@app.get("/api/v1/stock/income", tags=["财务"],
          summary="获取利润表数据",
          description="返回营业收入、净利润、每股收益等核心利润指标。")
def stock_income(
    ts_code: str = Query(..., description="股票代码"),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
):
    df = tc.query_income(ts_code, start_date, end_date)
    return {"ts_code": ts_code, "count": len(df), "data": _df_to_records(df)}


# ── ⑤ 资产负债表 ──────────────────────────────────────

@app.get("/api/v1/stock/balance", tags=["财务"],
          summary="获取资产负债表数据",
          description="返回总资产、总负债、股东权益等指标。")
def stock_balance(
    ts_code: str = Query(..., description="股票代码"),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
):
    df = tc.query_balancesheet(ts_code, start_date, end_date)
    return {"ts_code": ts_code, "count": len(df), "data": _df_to_records(df)}


# ── ⑥ 指数日线 ────────────────────────────────────────

@app.get("/api/v1/index/daily", tags=["指数"],
          summary="获取指数日线行情",
          description="支持上证综指(000001.SH)、深证成指(399001.SZ)、沪深300(000300.SH)等。")
def index_daily(
    index_code: str = Query(..., description="指数代码，如 000300.SH"),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
):
    if not start_date:
        start_date, end_date = _default_dates(30)
    elif not end_date:
        end_date = date.today().strftime("%Y%m%d")
    df = tc.query_index_daily(index_code, start_date, end_date)
    return {"index_code": index_code, "count": len(df), "data": _df_to_records(df)}


# ── ⑦ 指数成分股 ──────────────────────────────────────

@app.get("/api/v1/index/members", tags=["指数"],
          summary="获取指数成分股列表",
          description="返回指定指数当前的成分股构成。")
def index_members(
    index_code: str = Query(..., description="指数代码"),
    trade_date: Optional[str] = Query(None, description="查询日期"),
):
    df = tc.query_index_member(index_code, trade_date)
    return {"index_code": index_code, "count": len(df), "data": _df_to_records(df)}


# ── ⑧ 基金列表 ────────────────────────────────────────

@app.get("/api/v1/fund/list", tags=["基金"],
          summary="获取公募基金基础列表",
          description="返回基金代码、名称、管理人、类型等信息。")
def fund_list(market: str = Query("E", description="市场: E=场内 O=场外")):
    df = tc.query_fund_basic(market)
    return {"count": len(df), "data": _df_to_records(df)}


# ── ⑨ 期货日线 ────────────────────────────────────────

@app.get("/api/v1/futures/daily", tags=["期货"],
          summary="获取期货日线行情",
          description="返回主力合约或指定品种的日线数据。支持按交易所过滤。")
def futures_daily(
    trade_date: Optional[str] = Query(None, description="交易日期 YYYYMMDD"),
    ts_code: Optional[str] = Query(None, description="合约代码"),
    exchange: Optional[str] = Query(None, description="交易所: CFFEX/DCE/SHFE/CZCE/INE"),
):
    df = tc.query_fut_daily(trade_date=trade_date, ts_code=ts_code, exchange=exchange)
    return {"count": len(df), "data": _df_to_records(df)}


# ── ⑩ 宏观经济 ────────────────────────────────────────

@app.get("/api/v1/macro/china", tags=["宏观"],
          summary="获取中国宏观经济指标",
          description="返回 GDP、CPI、PPI 等中国核心宏观数据。")
def macro_china(
    year: Optional[str] = Query(None, description="年份"),
    quarter: Optional[str] = Query(None, description="季度"),
):
    df = tc.query_macro_china(year, quarter)
    return {"count": len(df), "data": _df_to_records(df)}


# ── (11) 交易日历 ─────────────────────────────────────

@app.get("/api/v1/calendar", tags=["工具"],
          summary="获取交易日历",
          description="返回上交所/深交所/中金所交易日历。")
def trade_calendar(
    exchange: str = Query("SSE", description="交易所: SSE/SZSE/CFFEX"),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
):
    if not start_date:
        start_date, end_date = _default_dates(90)
    df = tc.query_trade_cal(exchange, start_date, end_date)
    return {"exchange": exchange, "count": len(df), "data": _df_to_records(df)}


# ── ★ 组合编排：量化基础数据包 ─────────────────────────

@app.post("/api/v1/combo/quant_basic", tags=["组合编排"],
           summary="量化基础数据包",
           description="一次调用返回：股票信息 + 最近 N 日日线 + 最新利润表 + 最新资产负债表。适合 Agent 一键获取量化分析所需全量基础数据。",
           response_model=ComboQuantResponse)
def combo_quant_basic(req: ComboQuantRequest):
    start, end = _default_dates(req.days)

    # 并行获取四项数据
    basic_df = tc.query_stock_basic(ts_code=req.ts_code)
    daily_df = tc.query_daily(req.ts_code, start, end)
    income_df = tc.query_income(req.ts_code)
    balance_df = tc.query_balancesheet(req.ts_code)

    stock_info = None
    if not basic_df.empty:
        stock_info = _df_to_records(basic_df)[0]

    return ComboQuantResponse(
        ts_code=req.ts_code,
        stock_info=stock_info,
        daily_bars=_df_to_records(daily_df),
        income=_df_to_records(income_df)[:4] if not income_df.empty else [],
        balance=_df_to_records(balance_df)[:4] if not balance_df.empty else [],
    )


# ── 启动入口 ──────────────────────────────────────────


# -- ★ 聚合端点：金融数据主题包 -- 

from enum import Enum

class FinancePack(str, Enum):
    stock_deep = "stock_deep"
    market_overview = "market_overview"
    macro_brief = "macro_brief"
    all_in_one = "all_in_one"

class FinancePackResponse(BaseModel):
    pack: str
    description: str
    data: dict = {}

@app.post("/api/v1/combo/finance-pack", tags=["组合编排"],
           summary="金融数据主题包（整合入口）",
           description="一个端点覆盖全部金融数据。按 pack 参数选择主题：stock_deep=A股深度 / market_overview=市场全景 / macro_brief=宏观简报 / all_in_one=全能包。",
           response_model=FinancePackResponse)
def finance_pack(
    pack: FinancePack = Query(..., description="主题包类型"),
    ts_code: Optional[str] = Query(None, description="股票代码（stock_deep/all_in_one 需要）"),
    index_code: Optional[str] = Query("000300.SH", description="指数代码"),
    exchange: Optional[str] = Query("SSE", description="交易所"),
):
    result = {}
    
    if pack in (FinancePack.stock_deep, FinancePack.all_in_one):
        if not ts_code:
            raise HTTPException(400, "stock_deep/all_in_one 需要 ts_code 参数")
        result["stock_basic"] = _df_to_records(tc.query_stock_basic(ts_code=ts_code))
        result["stock_daily"] = _df_to_records(tc.query_daily(ts_code, *_default_dates(30)))
        result["stock_income"] = _df_to_records(tc.query_income(ts_code))[:4]
        result["stock_balance"] = _df_to_records(tc.query_balancesheet(ts_code))[:4]
    
    if pack in (FinancePack.market_overview, FinancePack.all_in_one):
        result["index_daily"] = _df_to_records(tc.query_index_daily(index_code, *_default_dates(30)))
        result["futures_daily"] = _df_to_records(tc.query_fut_daily(exchange=exchange))[:20]
        result["fund_list"] = _df_to_records(tc.query_fund_basic())[:20]
    
    if pack in (FinancePack.macro_brief, FinancePack.all_in_one):
        result["macro_china"] = _df_to_records(tc.query_macro_china())[:20]
        result["trade_calendar"] = _df_to_records(tc.query_trade_cal(exchange, *_default_dates(90)))[:10]
    
    descriptions = {
        "stock_deep": "单只A股完整数据：基本信息 + 30日日线 + 利润表 + 资产负债表",
        "market_overview": "市场全景：指数行情 + 期货日线 + 基金列表",
        "macro_brief": "宏观简报：GDP/CPI/PPI + 交易日历",
        "all_in_one": "全能数据包：以上全部",
    }
    
    return FinancePackResponse(
        pack=pack.value,
        description=descriptions.get(pack.value, ""),
        data=result,
    )


# -- ★ AI 内容工具 API --


class AIDetectRequest(BaseModel):
    text: str = Field(..., description="待检测文本", min_length=10)

class AIDetectResponse(BaseModel):
    score: float
    verdict: str
    details: dict = {}

@app.post("/api/v1/tools/detect-ai", tags=["AI内容工具"],
           summary="AI 文本检测",
           description="检测文本是否为 AI 生成。基于句子结构、过渡词密度、AI 句式模式匹配等启发式规则。返回 0-100 分数和详细分析。")
def tool_detect_ai(req: AIDetectRequest):
    return detect_ai_text(req.text)

class ViralVerifyRequest(BaseModel):
    content: str = Field(..., description="待验证的文章内容", min_length=50)

@app.post("/api/v1/tools/viral-verify", tags=["AI内容工具"],
           summary="爆款内容验证",
           description="六维度爆款要素评分：好奇心缺口、情绪共鸣、价值/实用性、关联/时效性、叙事/节奏、反直觉/新颖性。纯规则引擎，即时返回评分和优化建议。")
def tool_viral_verify(req: ViralVerifyRequest):
    return verify_viral(req.content)

@app.get("/api/v1/tools/hot-topics", tags=["AI内容工具"],
          summary="实时热点选题",
          description="从 TopHub 抓取当前全网热榜，返回 TOP 20 话题。适合内容创作者、自媒体 Agent 快速选题。")
def tool_hot_topics(limit: int = Query(20, ge=5, le=50, description="返回数量")):
    topics = fetch_hot_topics(limit)
    return {"count": len(topics), "source": "TopHub", "topics": topics}


if __name__ == "__main__":
    import uvicorn
    host = os.getenv("SERVER_HOST", "0.0.0.0")
    port = int(os.getenv("SERVER_PORT", "8800"))
    uvicorn.run("src.server:app", host=host, port=port, reload=True)
