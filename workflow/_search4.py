import httpx, json
headers = {
    "X-Api-Key": "tmHkMAh5LN1ygSdx05tYVz4qt_grFGuTIn6e3AEBjAtwxwdBQvGHsPjKgMamW9NP",
    "X-Platform-User-Id": "71e2c0fd-f489-476b-b79b-005de54b6ed7",
}

# Search for API services in text/content domain
keywords = ["文本检测", "改写API", "验证API", "内容API", "文本API", "API", "检测API"]
for kw in keywords:
    r = httpx.get("https://api.uumit.com/api/v1/marketplace/search", 
                   params={"keyword": kw, "limit": 5}, headers=headers, timeout=10)
    data = r.json()
    items = data.get("data", {}).get("knowledge_store", {}).get("items", [])
    total = data.get("data", {}).get("total", 0)
    titles = [it.get("title", "?")[:50] for it in items[:3]]
    print(f"[{kw}] total={total} | {titles}")
