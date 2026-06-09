import httpx, json, os
from dotenv import load_dotenv
load_dotenv(r"C:\Users\MECHREVO\Documents\UUMit\finance-data-service\.env")
headers = {
    "X-Api-Key": os.getenv("UUMIT_API_KEY",""),
    "X-Platform-User-Id": os.getenv("UUMIT_USER_ID",""),
}

# Try to find a working list endpoint with query params
tries = [
    "https://api.uumit.com/api/v1/data-marketplace/apis?status=draft",
    "https://api.uumit.com/api/v1/data-marketplace/apis/list?status=draft",
    "https://api.uumit.com/api/v1/marketplace/apis?owner=self",
    "https://api.uumit.com/api/v1/data-marketplace?status=draft",
]
for url in tries:
    r = httpx.get(url, headers=headers, timeout=5)
    print(f"{url.split('?')[0].split('/')[-1]}: {r.status_code} | {r.text[:120]}")
