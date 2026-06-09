import httpx, os
from dotenv import load_dotenv
load_dotenv(r"C:\Users\MECHREVO\Documents\UUMit\finance-data-service\.env")

headers = {
    "X-Api-Key": os.getenv("UUMIT_API_KEY"),
    "X-Platform-User-Id": os.getenv("UUMIT_USER_ID"),
}

keywords = [
    "炒股", "交易策略", "量化", "短线", "Prompt", "选股", 
    "AI交易", "交易系统", "趋势", "打板", "A股策略",
]

for kw in keywords:
    try:
        r = httpx.get("https://api.uumit.com/api/v1/marketplace/search",
                       params={"keyword": kw, "limit": 3}, headers=headers, timeout=8)
        d = r.json()
        items = d.get("data", {}).get("knowledge_store", {}).get("items", [])
        for item in items[:2]:
            title = item.get("title", "?")[:55]
            price = item.get("price_ut", "?")
            print(f"[{kw}] {price} UT | {title}")
    except Exception as e:
        print(f"[{kw}] err: {e}")
