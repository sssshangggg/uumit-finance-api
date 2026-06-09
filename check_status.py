import httpx, json, os
from dotenv import load_dotenv
load_dotenv(r"C:\Users\MECHREVO\Documents\UUMit\finance-data-service\.env")

headers = {
    "X-Api-Key": os.getenv("UUMIT_API_KEY"),
    "X-Platform-User-Id": os.getenv("UUMIT_USER_ID"),
}

api_id = "41133a64-28b5-4327-b4cc-5085f1af5902"
r = httpx.get(f"https://api.uumit.com/api/v1/capabilities/{api_id}", headers=headers, timeout=10)
d = r.json()
data = d.get("data", {})
# Print all keys
print("Fields:", list(data.keys()))
# Print key values
for k in data:
    if k not in ["detail_content", "description"]:
        print(f"  {k}: {data[k]}")
