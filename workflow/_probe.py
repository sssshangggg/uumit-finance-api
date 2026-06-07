import httpx, json, os, sys
from dotenv import load_dotenv
load_dotenv()

headers = {
    "X-Api-Key": os.getenv("UUMIT_API_KEY", ""),
    "X-Platform-User-Id": os.getenv("UUMIT_USER_ID", ""),
    "Content-Type": "application/json",
}

# Re-register one API and capture the full response
url_base = "https://shirt-conjoined-rasping.ngrok-free.dev"
payload = {
    "name": "AI-test-probe",
    "description": "test probe to get response",
    "category": "content",
    "tags": ["test"],
    "upstream_method": "GET",
    "upstream_url": url_base + "/api/v1/tools/hot-topics?limit=5",
    "request_schema": {"type": "object", "properties": {}},
    "response_schema": {"type": "object"},
    "price_ut": "1",
    "detail_content": "test",
}

r = httpx.post("https://api.uumit.com/api/v1/data-marketplace/apis", 
                json=payload, headers=headers, timeout=15)
print(f"Status: {r.status_code}")
resp = r.json()
print(json.dumps(resp, ensure_ascii=False, indent=2)[:1000])
