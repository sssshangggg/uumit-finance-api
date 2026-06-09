import httpx, json, os, sys
from dotenv import load_dotenv
load_dotenv(r"C:\Users\MECHREVO\Documents\UUMit\finance-data-service\.env")

headers = {
    "X-Api-Key": os.getenv("UUMIT_API_KEY",""),
    "X-Platform-User-Id": os.getenv("UUMIT_USER_ID",""),
    "Content-Type": "application/json",
}

# Step 1: Search for ALL our API names and collect IDs
names_to_find = [
    "AI-text-detection", "AI-probe-test",
]

# Step 2: Re-register the content tools and CAPTURE their IDs  
import re
from pathlib import Path

# Read skills-content.json
sp = Path(r"C:\Users\MECHREVO\Documents\UUMit\finance-data-service\uumit\skills-content.json")
with open(sp, "r", encoding="utf-8") as f:
    cfg = json.load(f)

url_base = cfg["base_url"]

print("=== Registering and capturing IDs ===")
new_ids = {}

for skill in cfg["skills"]:
    payload = {
        "name": skill["name"],
        "description": skill["description"],
        "category": skill["category"],
        "tags": skill.get("tags", []),
        "upstream_method": skill.get("method", "GET"),
        "upstream_url": url_base + skill.get("endpoint", ""),
        "request_schema": {"type": "object", "properties": {p: {"type": m.get("type","string"), "description": m.get("desc","")} for p,m in skill.get("params",{}).items()},
        "response_schema": {"type": "object"},
        "price_ut": str(skill["pricing"]["amount"]),
        "test_params": skill.get("test_params", {}),
        "detail_content": skill.get("detail", skill["description"]),
    }
    r = httpx.post("https://api.uumit.com/api/v1/data-marketplace/apis", json=payload, headers=headers, timeout=15)
    if r.status_code == 200:
        api_id = r.json().get("data", {}).get("id")
        new_ids[skill["name"]] = api_id
        print(f"  [OK] {skill['name']} -> {api_id}")
    else:
        print(f"  [FAIL] {skill['name']}: {r.status_code} {r.text[:100]}")

# Save IDs
id_path = Path(r"C:\Users\MECHREVO\Documents\UUMit\workflow\api_ids.json")
with open(id_path, "w", encoding="utf-8") as f:
    json.dump(new_ids, f, ensure_ascii=False, indent=2)
print(f"\nSaved {len(new_ids)} IDs to api_ids.json")
