"""UUMit 知识商品自动化工作流
热榜抓取 -> 财经选题筛选 -> 金融数据注入 -> 简报生成 -> 爆款验证

用法:
    python workflow/pipeline.py              # 全流程
    python workflow/pipeline.py --brief      # 仅数据简报
    python workflow/pipeline.py --verify     # 仅爆款验证
"""

import argparse, json, os, re, sys
from datetime import datetime
from pathlib import Path
import httpx

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_ROOT / "output"
POSTS_DIR = OUTPUT_DIR / "defou-stanley-posts"
VERIFIED_DIR = OUTPUT_DIR / "viral-verified-posts"
FINANCE_API = os.getenv("FINANCE_API_URL", "http://localhost:8800")
TOPHUB_URL = "https://tophub.today/hot"
UA = "Mozilla/5.0 (compatible; UUMit/1.0)"

# 财经话题关键词
FINANCE_KW = [
    "股", "金融", "经济", "基金", "A股", "央行", "房价", "利率", "人民币", "美元",
    "黄金", "银行", "保险", "理财", "投资", "上市", "IPO", "财报", "GDP",
    "CPI", "降息", "加息", "通胀", "美股", "港股", "科技股", "新能源", "芯片",
    "关税", "贸易", "消费", "补贴", "楼市", "地产", "就业", "工资", "税收",
    "茅台", "宁德", "比亚迪", "特斯拉", "华为", "小米", "腾讯", "阿里",
    "裁员", "破产", "并购", "融资", "估值", "市值", "出口", "崩盘", "暴跌",
    "暴涨", "涨停", "跌停", "油价", "车价", "产能", "供应链",
]

# 关键词到股票代码的映射
STOCK_KW_MAP = {
    "比亚迪": ["002594.SZ"], "长城": ["601633.SH"], "上汽": ["600104.SH"],
    "长安": ["000625.SZ"], "宁德": ["300750.SZ"], "茅台": ["600519.SH"],
    "小米": ["01810.HK"], "腾讯": ["00700.HK"], "阿里": ["09988.HK"],
    "银行": ["600036.SH", "601398.SH"], "地产": ["000002.SZ"],
    "芯片": ["688981.SH"], "新能源": ["300750.SZ", "002594.SZ"],
    "车": ["002594.SZ", "601633.SH"], "AI": ["688256.SH"],
}

# ============ 步骤 1: 热榜抓取 ============

def fetch_tophub(limit: int = 40) -> list[dict]:
    """从 TopHub 抓取热榜。"""
    print("[1/5] 抓取 TopHub 热榜...", end=" ")
    r = httpx.get(TOPHUB_URL, headers={"User-Agent": UA}, timeout=15)
    r.raise_for_status()
    text = r.text

    items = []
    li_pat = re.compile(r'<li class="child-item">(.*?)</li>', re.DOTALL)
    for li in li_pat.finditer(text):
        block = li.group(1)
        rank_m = re.search(r'<span[^>]*>\s*(\d+)\s*</span>', block)
        title_m = re.search(r'<p class="medium-txt">\s*<a[^>]*>(.*?)</a>', block, re.DOTALL)
        link_m = re.search(r'<p class="medium-txt">\s*<a href="([^"]*)"', block)
        small_m = re.search(r'<p class="small-txt">\s*(.*?)\s*</p>', block, re.DOTALL)

        if title_m:
            title = re.sub(r'<[^>]*>', '', title_m.group(1)).strip()
            source, hot = "", ""
            if small_m:
                parts = [p.strip() for p in re.split(r'[\u00b7\u2027]', small_m.group(1))]
                source = parts[0] if parts else ""
                hot = parts[1].strip() if len(parts) > 1 else ""
            items.append({
                "rank": rank_m.group(1) if rank_m else "?",
                "title": title, "link": link_m.group(1) if link_m else "",
                "source": source, "hot": hot,
            })
        if len(items) >= limit:
            break
    print(f"{len(items)} 条")
    return items


# ============ 步骤 2: 财经选题筛选 ============

def filter_finance(items: list[dict]) -> list[dict]:
    """筛选财经相关话题。"""
    print("[2/5] 筛选财经话题...", end=" ")
    finance = [it for it in items if any(kw in it["title"] for kw in FINANCE_KW)]
    print(f"{len(finance)} 条")
    return finance


# ============ 步骤 3: 金融数据注入 ============

def infer_stocks(topics: list[dict]) -> list[str]:
    """从话题推断相关股票代码。"""
    codes = set()
    for t in topics:
        for kw, stocks in STOCK_KW_MAP.items():
            if kw in t["title"]:
                codes.update(stocks)
    return list(codes)[:6]


def query_finance_data(codes: list[str]) -> dict:
    """查询金融数据服务 API。"""
    print(f"[3/5] 查询金融数据 ({len(codes)} 只)...")
    data = {}
    for code in codes:
        try:
            resp = httpx.get(f"{FINANCE_API}/api/v1/stock/daily",
                             params={"ts_code": code}, timeout=10)
            if resp.status_code == 200:
                body = resp.json()
                recs = body.get("data", [])
                data[code] = {
                    "count": len(recs),
                    "latest": recs[-1] if recs else None,
                    "last_5": recs[-5:] if len(recs) >= 5 else recs,
                }
                print(f"    {code}: {len(recs)} 条")
            else:
                print(f"    {code}: HTTP {resp.status_code}")
                data[code] = {"error": f"HTTP {resp.status_code}"}
        except Exception as e:
            print(f"    {code}: {e}")
            data[code] = {"error": str(e)}
    return data


# ============ 步骤 4: 内容简报 & AI Prompt ============

def build_brief(topics: list[dict], fin_data: dict) -> dict:
    """构建内容简报，供 AI 生成使用。"""
    print("[4/5] 构建内容简报...", end=" ")

    data_summary = []
    for code, info in fin_data.items():
        if "latest" in info and info["latest"]:
            lt = info["latest"]
            data_summary.append({
                "code": code,
                "close": lt.get("close"),
                "pct_chg": lt.get("pct_chg"),
                "last_5": [
                    {"date": r.get("trade_date"), "close": r.get("close"), "pct": r.get("pct_chg")}
                    for r in info.get("last_5", [])
                ],
            })

    brief = {
        "generated_at": datetime.now().isoformat(),
        "topics": topics[:5],
        "finance_data": data_summary,
        "content_prompt": _build_prompt(topics, data_summary),
    }
    print(f"{len(topics)} 选题")
    return brief


def _build_prompt(topics: list[dict], data_summary: list[dict]) -> str:
    """生成 AI 创作 prompt。"""
    import json as _json
    topics_text = "\n".join(
        f"- #{t['rank']} [{t['source']}] {t['title']} ({t['hot']})"
        for t in topics[:5]
    )
    data_text = _json.dumps(data_summary, ensure_ascii=False, indent=2)

    return f"""你是 Defou x Stanley 风格的内容专家。基于以下素材生成一篇知识商品文章。

## 热点话题
{topics_text}

## 金融数据
{data_text}

## 创作要求
1. 选出最能形成「矛盾叙事」的 1-2 个话题组合
2. 将金融数据作为论证锚点嵌入文章
3. Defou x Stanley 风格: 极简、锋利、反直觉、短句分行、留白
4. 四段结构: 现象 -> 分析 -> 隐喻 -> 认知升级
5. 结尾有「被戳中」的刺痛感
6. 800-1200 字，简体中文
7. 标题: 数字 + 对比 + 反差
"""


# ============ 步骤 5: 爆款验证 ============

def verify_article(article_path: Path) -> str:
    """六维度爆款要素评分。"""
    print(f"[5/5] 验证: {article_path.name}")
    content = article_path.read_text(encoding="utf-8")

    sc = {
        "curiosity": _score_curiosity(content),
        "emotion": _score_emotion(content),
        "value": _score_value(content),
        "relevance": _score_relevance(content),
        "pacing": _score_pacing(content),
        "novelty": _score_novelty(content),
    }
    total = sum(sc.values())
    labels = ["好奇心缺口", "情绪共鸣", "价值/实用", "关联/时效", "叙事/节奏", "反直觉/新颖"]
    keys = ["curiosity", "emotion", "value", "relevance", "pacing", "novelty"]

    rows = "\n".join(
        f"| {labels[i]} | {sc[k]} | {'优秀' if sc[k] >= 7 else '可提升'} |"
        for i, k in enumerate(keys)
    )

    return f"""# 爆款要素验证报告

## 评分卡

| 要素 | 得分 | 评价 |
| :--- | :---: | :--- |
{rows}

**总体评分: {total}/100**

## 改进建议
- 数据密度: {'充足' if sc['value'] >= 7 else '建议增加具体数据点'}
- 情感冲击: {'到位' if sc['emotion'] >= 7 else '建议加入人物故事'}
- 节奏把控: {'优秀' if sc['pacing'] >= 7 else '建议拆分长段'}
- 新颖度: {'有洞察' if sc['novelty'] >= 7 else '建议找更刁钻的角度'}

---
*验证时间: {datetime.now().strftime("%Y-%m-%d %H:%M")}*
"""


# ---- 评分辅助函数 ----

def _score_curiosity(c: str) -> int:
    s = 5
    lines = c.strip().split("\n")
    title = lines[0] if lines else ""
    if re.search(r'\d', title): s += 1
    if any(w in title for w in ["vs", "崩", "爆", "跌", "涨"]): s += 1
    if "?" in title or "？" in title: s += 1
    early = "\n".join(lines[:5])
    if any(w in early for w in ["你以为", "其实", "不是", "真正"]): s += 1
    return min(s, 10)

def _score_emotion(c: str) -> int:
    s = 5
    for w in ["焦虑", "恐惧", "崩溃", "绝望", "刺痛", "残忍", "暴赚", "疯抢", "清醒"]:
        if w in c: s += 0.5
    return min(int(s), 10)

def _score_value(c: str) -> int:
    s = 5
    if re.search(r'\d+(\.\d+)?\s*(元|万|亿|%|英镑|美元)', c): s += 2
    if "|" in c: s += 1
    if re.search(r'\d+\s*倍', c): s += 1
    return min(s, 10)

def _score_relevance(c: str) -> int:
    s = 5
    if "TopHub" in c or "热榜" in c: s += 2
    if re.search(r'\d{8}', c): s += 1
    if any(w in c for w in ["今日", "本周", "一季度"]): s += 1
    return min(s, 10)

def _score_pacing(c: str) -> int:
    lines = [l for l in c.strip().split("\n") if l.strip()]
    short = sum(1 for l in lines if len(l.strip()) < 20)
    ratio = short / max(len(lines), 1)
    s = 5
    if ratio > 0.6: s += 2
    if ratio > 0.8: s += 3
    return min(s, 10)

def _score_novelty(c: str) -> int:
    s = 5
    for w in ["其实", "你以为", "本质上", "背后", "真正", "镜像", "隐喻", "参差"]:
        if w in c: s += 0.5
    if "结构性" in c: s += 1
    return min(int(s), 10)


# ============ 主流程 ============

def run_full():
    """全流程: 抓取 -> 筛选 -> 数据 -> 简报 -> 验证。"""
    POSTS_DIR.mkdir(parents=True, exist_ok=True)
    VERIFIED_DIR.mkdir(parents=True, exist_ok=True)

    items = fetch_tophub()
    topics = filter_finance(items)
    if not topics:
        print("未找到财经话题，跳过。")
        return

    codes = infer_stocks(topics)
    fin_data = query_finance_data(codes) if codes else {}
    brief = build_brief(topics, fin_data)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    bp = OUTPUT_DIR / f"brief_{ts}.json"
    bp.write_text(json.dumps(brief, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  简报: {bp}")

    pp = OUTPUT_DIR / f"prompt_{ts}.md"
    pp.write_text(brief["content_prompt"], encoding="utf-8")
    print(f"  Prompt: {pp}")

    # 验证已有文章
    mds = list(POSTS_DIR.glob("*.md"))
    if mds:
        latest = max(mds, key=lambda f: f.stat().st_mtime)
        report = verify_article(latest)
        rp = VERIFIED_DIR / f"verified_{ts}_{latest.name}"
        rp.write_text(report, encoding="utf-8")
        print(f"  验证: {rp}")

    print(f"\n完成！输出目录: {OUTPUT_DIR}")


def run_brief_only():
    """仅生成简报。"""
    items = fetch_tophub()
    topics = filter_finance(items)
    if not topics:
        print("未找到财经话题")
        return
    codes = infer_stocks(topics)
    fin_data = query_finance_data(codes) if codes else {}
    brief = build_brief(topics, fin_data)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    bp = OUTPUT_DIR / f"brief_{ts}.json"
    bp.write_text(json.dumps(brief, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n简报: {bp}")
    print(f"内容 Prompt:\n{brief['content_prompt']}")


def run_verify_only():
    """仅验证已有文章。"""
    mds = list(POSTS_DIR.glob("*.md"))
    if not mds:
        print("posts 目录下无文章。")
        return
    VERIFIED_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    for f in mds:
        report = verify_article(f)
        rp = VERIFIED_DIR / f"verified_{ts}_{f.name}"
        rp.write_text(report, encoding="utf-8")
        print(f"  {rp}")


def main():
    p = argparse.ArgumentParser(description="UUMit 知识商品自动化工作流")
    p.add_argument("--brief", action="store_true", help="仅生成数据简报")
    p.add_argument("--verify", action="store_true", help="仅爆款验证")
    args = p.parse_args()
    if args.verify: run_verify_only()
    elif args.brief: run_brief_only()
    else: run_full()


if __name__ == "__main__":
    main()
