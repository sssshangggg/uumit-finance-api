import httpx, os
from dotenv import load_dotenv
load_dotenv(r"C:\Users\MECHREVO\Documents\UUMit\finance-data-service\.env")

headers = {
    "X-Api-Key": os.getenv("UUMIT_API_KEY"),
    "X-Platform-User-Id": os.getenv("UUMIT_USER_ID"),
    "Content-Type": "application/json",
}

test = {"title": "probe", "description": "test", "price_ut": "1", "tags": ["test"]}

# Knowledge store endpoints
endpoints = [
    ("POST", "/api/v1/knowledge-store/products"),
    ("POST", "/api/v1/knowledge-store/items"),
    ("POST", "/api/v1/marketplace/products"),
    ("POST", "/api/v1/marketplace/items"),
    ("POST", "/api/v1/knowledge"),
    ("POST", "/api/v1/products"),
    ("POST", "/api/v1/marketplace/publish"),
    ("POST", "/api/v1/store/products"),
    ("POST", "/api/v1/marketplace/knowledge-store"),
]

for method, ep in endpoints:
    try:
        r = httpx.post(f"https://api.uumit.com{ep}", json=test, headers=headers, timeout=5)
        print(f"{method} {ep}: {r.status_code} | {r.text[:120]}")
    except Exception as e:
        print(f"{method} {ep}: {e}")
