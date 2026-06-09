import httpx, os
from dotenv import load_dotenv
load_dotenv(r"C:\Users\MECHREVO\Documents\UUMit\finance-data-service\.env")

headers = {
    "X-Api-Key": os.getenv("UUMIT_API_KEY"),
    "X-Platform-User-Id": os.getenv("UUMIT_USER_ID"),
}

# Search for our product
r = httpx.get("https://api.uumit.com/api/v1/marketplace/search",
               params={"keyword": "每日财经头条", "limit": 10}, headers=headers, timeout=10)
d = r.json()
items = d.get("data", {}).get("knowledge_store", {}).get("items", [])
print(f"Found {len(items)} items")
for item in items:
    print(f"  title={item.get('title','?')[:60]}")
    print(f"  id={item.get('id','?')[:40]}")
    print(f"  price={item.get('price_ut','?')}")
    print(f"  status={item.get('content_review_status','?')}")
    print()

if not items:
    print("Full response:")
    print(str(d)[:500])
