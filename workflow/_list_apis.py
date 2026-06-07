import httpx, json
headers = {
    "X-Api-Key": "tmHkMAh5LN1ygSdx05tYVz4qt_grFGuTIn6e3AEBjAtwxwdBQvGHsPjKgMamW9NP",
    "X-Platform-User-Id": "71e2c0fd-f489-476b-b79b-005de54b6ed7",
}

# Try to list our own APIs to get IDs
r = httpx.get("https://api.uumit.com/api/v1/data-marketplace/apis", headers=headers, timeout=10)
data = r.json()
print(f"Status: {r.status_code}")
if isinstance(data, dict):
    for k, v in data.items():
        if isinstance(v, list):
            print(f"{k}: list of {len(v)}")
            for item in v[:3]:
                print(f"  id={item.get('id','?')} name={item.get('name','?')} status={item.get('status','?')}")
        elif isinstance(v, dict):
            print(f"{k}: {list(v.keys())[:5]}")
        else:
            print(f"{k}: {str(v)[:200]}")
