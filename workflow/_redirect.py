import httpx, json, os
from dotenv import load_dotenv
load_dotenv(r"C:\Users\MECHREVO\Documents\UUMit\finance-data-service\.env")
headers = {
    "X-Api-Key": os.getenv("UUMIT_API_KEY",""),
    "X-Platform-User-Id": os.getenv("UUMIT_USER_ID",""),
}
# Follow 307 redirect
r = httpx.get("https://api.uumit.com/api/v1/data-marketplace", headers=headers, timeout=5, follow_redirects=True)
print(f"Status: {r.status_code} | URL: {r.url}")
print(f"Body: {r.text[:300]}")
