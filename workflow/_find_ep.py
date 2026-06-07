import httpx, json
headers = {
    "X-Api-Key": "tmHkMAh5LN1ygSdx05tYVz4qt_grFGuTIn6e3AEBjAtwxwdBQvGHsPjKgMamW9NP",
    "X-Platform-User-Id": "71e2c0fd-f489-476b-b79b-005de54b6ed7",
}
# Try different endpoints to list our APIs
endpoints = [
    "/api/v1/data-marketplace/apis",
    "/api/v1/data-marketplace/apis/list",
    "/api/v1/data-marketplace/list",
    "/api/v1/data-marketplace/my",
    "/api/v1/apis",
]
for ep in endpoints:
    try:
        r = httpx.get(f"https://api.uumit.com{ep}", headers=headers, timeout=5)
        print(f"GET {ep}: {r.status_code} | {r.text[:150]}")
    except Exception as e:
        print(f"GET {ep}: {e}")
