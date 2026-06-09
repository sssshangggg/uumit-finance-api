import httpx, json, os
from dotenv import load_dotenv
load_dotenv(r"C:\Users\MECHREVO\Documents\UUMit\finance-data-service\.env")
headers = {
    "X-Api-Key": os.getenv("UUMIT_API_KEY",""),
    "X-Platform-User-Id": os.getenv("UUMIT_USER_ID",""),
    "Content-Type": "application/json",
}

endpoints = [
    "/api/v1/data-marketplace/apis",
    "/api/v1/marketplace/my",
    "/api/v1/users/me/apis",
    "/api/v1/data-marketplace/my-apis",
]
for ep in endpoints:
    r = httpx.get(f"https://api.uumit.com{ep}", headers=headers, timeout=5)
    print(f"GET {ep}: {r.status_code} | {r.text[:150]}")
