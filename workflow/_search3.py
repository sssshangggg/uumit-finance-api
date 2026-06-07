import httpx, json
headers = {
    "X-Api-Key": "tmHkMAh5LN1ygSdx05tYVz4qt_grFGuTIn6e3AEBjAtwxwdBQvGHsPjKgMamW9NP",
    "X-Platform-User-Id": "71e2c0fd-f489-476b-b79b-005de54b6ed7",
}
r = httpx.get("https://api.uumit.com/api/v1/marketplace/search", 
               params={"keyword": "AI检测"}, headers=headers, timeout=10)
data = r.json()
items = data.get("data", {}).get("knowledge_store", {}).get("items", [])
if items:
    # Print full first item to understand structure
    first = items[0]
    print("Keys:", list(first.keys()))
    for k, v in first.items():
        print(f"  {k}: {str(v)[:120]}")
    print()
    # Print all item names
    for item in items[:10]:
        title = item.get("title", item.get("name", "?"))
        price = item.get("price_ut", item.get("price", "?"))
        print(f"  {title} | {price} UT")
