import httpx, json, os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(r"C:\Users\MECHREVO\Documents\UUMit\finance-data-service\.env")

headers = {
    "X-Api-Key": os.getenv("UUMIT_API_KEY",""),
    "X-Platform-User-Id": os.getenv("UUMIT_USER_ID",""),
    "Content-Type": "application/json",
}

sp = Path(r"C:\Users\MECHREVO\Documents\UUMit\finance-data-service\uumit\skills-content.json")
with open(sp, "r", encoding="utf-8") as f:
    cfg = json.load(f)

url_base = cfg["base_url"]
new_ids = {}

for skill in cfg["skills"]:
    # Build request_schema
    params = skill.get("params", {})
    properties = {}
    required = []
    for key, meta in params.items():
        prop = {"type": meta.get("type", "string"), "description": meta.get("desc", "")}
        if "enum" in meta:
            prop["enum"] = meta["enum"]
        if "default" in meta:
            prop["default"] = meta["default"]
        if meta.get("required"):
            required.append(key)
        properties[key] = prop
    schema = {"type": "object", "properties": properties}
    if required:
        schema["required"] = required

    payload = {
        "name": skill["name"],
        "description": skill["description"],
        "category": skill["category"],
        "tags": skill.get("tags", []),
        "upstream_method": skill.get("method", "GET"),
        "upstream_url": url_base + skill.get("endpoint", ""),
        "request_schema": schema,
        "response_schema": {"type": "object"},
        "price_ut": str(skill["pricing"]["amount"]),
        "test_params": skill.get("test_params", {}),
        "detail_content": skill.get("detail", skill["description"]),
    }
    r = httpx.post("https://api.uumit.com/api/v1/data-marketplace/apis", json=payload, headers=headers, timeout=15)
    if r.status_code == 200:
        api_id = r.json().get("data", {}).get("id")
        new_ids[skill["name"]] = api_id
        print(f"OK {skill['name']} -> {api_id}")
    else:
        print(f"FAIL {skill['name']}: {r.status_code}")

id_path = Path(r"C:\Users\MECHREVO\Documents\UUMit\workflow\api_ids.json")
with open(id_path, "w", encoding="utf-8") as f:
    json.dump(new_ids, f, ensure_ascii=False, indent=2)
print(f"Saved {len(new_ids)} IDs")
