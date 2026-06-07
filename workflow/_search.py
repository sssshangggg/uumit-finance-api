import httpx, json
headers = {
    "X-Api-Key": "tmHkMAh5LN1ygSdx05tYVz4qt_grFGuTIn6e3AEBjAtwxwdBQvGHsPjKgMamW9NP",
    "X-Platform-User-Id": "71e2c0fd-f489-476b-b79b-005de54b6ed7",
}
r = httpx.get("https://api.uumit.com/api/v1/marketplace/search", params={"keyword": "AI"}, headers=headers, timeout=10)
data = r.json()
print("Type:", type(data).__name__)
if isinstance(data, list):
    print("Count:", len(data))
    for item in data[:5]:
        name = item.get("name", "?")
        cat = item.get("category", "?")
        price = item.get("price_ut", "?")
        print(f"  {name} | {cat} | {price} UT")
elif isinstance(data, dict):
    keys = list(data.keys())
    print("Keys:", keys)
    for k in keys:
        v = data[k]
        if isinstance(v, list):
            print(f"  {k}: list of {len(v)}")
        else:
            print(f"  {k}: {str(v)[:100]}")
