import httpx, json, os
from dotenv import load_dotenv
load_dotenv(r"C:\Users\MECHREVO\Documents\UUMit\finance-data-service\.env")
headers = {
    "X-Api-Key": os.getenv("UUMIT_API_KEY",""),
    "X-Platform-User-Id": os.getenv("UUMIT_USER_ID",""),
    "Content-Type": "application/json",
}
api_id = "f5316411-94a0-4715-ba21-af48b6771c7c"

# Get current state
r = httpx.get(f"https://api.uumit.com/api/v1/data-marketplace/apis/{api_id}", headers=headers, timeout=10)
d = r.json().get("data", {})
print(f"Current status: {d.get('status')}")

# Try submitting with different status values
for status in ["submitted", "pending", "pending_review", "review", "published", "online"]:
    r = httpx.put(f"https://api.uumit.com/api/v1/data-marketplace/apis/{api_id}", 
                  json={"status": status}, headers=headers, timeout=10)
    new_status = r.json().get("data", {}).get("status", "?")
    print(f"  status={status} -> {new_status} (HTTP {r.status_code})")
    if new_status != "draft":
        break

# Clean up the probe
r = httpx.delete(f"https://api.uumit.com/api/v1/data-marketplace/apis/{api_id}", headers=headers, timeout=10)
print(f"Deleted probe: {r.status_code}")
