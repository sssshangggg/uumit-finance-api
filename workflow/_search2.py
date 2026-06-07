import httpx, json
headers = {
    "X-Api-Key": "tmHkMAh5LN1ygSdx05tYVz4qt_grFGuTIn6e3AEBjAtwxwdBQvGHsPjKgMamW9NP",
    "X-Platform-User-Id": "71e2c0fd-f489-476b-b79b-005de54b6ed7",
}

# Search for various keywords
keywords = ["AI检测", "改写", "爆款", "验证", "文章生成", "写作", "内容"]
for kw in keywords:
    r = httpx.get("https://api.uumit.com/api/v1/marketplace/search", 
                   params={"keyword": kw}, headers=headers, timeout=10)
    data = r.json()
    total = data.get("data", {}).get("total", 0)
    items = data.get("data", {}).get("knowledge_store", {}).get("items", [])
    names = [it.get("name", "?")[:40] for it in items[:5]]
    print(f"[{kw}] total={total} | top5={names}")
