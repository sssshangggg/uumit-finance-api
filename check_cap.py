import httpx, os
from dotenv import load_dotenv
load_dotenv(r"C:\Users\MECHREVO\Documents\UUMit\finance-data-service\.env")

headers = {
    "X-Api-Key": os.getenv("UUMIT_API_KEY"),
    "X-Platform-User-Id": os.getenv("UUMIT_USER_ID"),
}

# Get the capability by ID
api_id = "41133a64-28b5-4327-b4cc-5085f1af5902"
r = httpx.get(f"https://api.uumit.com/api/v1/capabilities/{api_id}", headers=headers, timeout=10)
print(f"GET /capabilities/{api_id}: {r.status_code}")
print(r.text[:500])
print()

# Also try GET without ID
r = httpx.get("https://api.uumit.com/api/v1/capabilities", headers=headers, timeout=5)
print(f"GET /capabilities: {r.status_code} | {r.text[:200]}")
