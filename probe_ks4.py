import httpx, os
from dotenv import load_dotenv
load_dotenv(r"C:\Users\MECHREVO\Documents\UUMit\finance-data-service\.env")

headers = {
    "X-Api-Key": os.getenv("UUMIT_API_KEY"),
    "X-Platform-User-Id": os.getenv("UUMIT_USER_ID"),
}

# Try file upload endpoint
upload_endpoints = [
    ("POST", "/api/v1/upload"),
    ("POST", "/api/v1/files/upload"),
    ("POST", "/api/v1/knowledge-store/upload"),
    ("POST", "/api/v1/assets/upload"),
]

for method, ep in upload_endpoints:
    try:
        r = httpx.post(f"https://api.uumit.com{ep}", headers=headers, timeout=5)
        print(f"{method} {ep}: {r.status_code} | {r.text[:120]}")
    except Exception as e:
        print(f"{method} {ep}: {e}")

# Also try: maybe knowledge store IS capabilities but with different fields
# Look at one knowledge store item's full structure
r = httpx.get("https://api.uumit.com/api/v1/marketplace/search",
               params={"keyword": "短视频爆款内容生产工作流", "limit": 1}, headers=headers, timeout=8)
d = r.json()
items = d.get("data", {}).get("knowledge_store", {}).get("items", [])
if items:
    item = items[0]
    print("\nKnowledge store item fields:")
    for k, v in item.items():
        if k not in ["description"]:
            print(f"  {k}: {str(v)[:100]}")
