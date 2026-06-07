"""UUMit 数据广场 API 批量上架脚本"""
import json, os, sys, httpx

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "skills.json")
for i, arg in enumerate(sys.argv):
    if arg == "--file" and i + 1 < len(sys.argv):
        CONFIG_PATH = sys.argv[i + 1]
        sys.argv.pop(i); sys.argv.pop(i)
        break

UUMIT_API_KEY = os.getenv("UUMIT_API_KEY", "")
UUMIT_USER_ID = os.getenv("UUMIT_USER_ID", "")
UUMIT_API_BASE = os.getenv("UUMIT_API_BASE", "https://api.uumit.com")


def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def build_request_schema(skill):
    params = skill.get("params", {})
    required, properties = [], {}
    for key, meta in params.items():
        prop = {"type": meta.get("type", "string"), "description": meta.get("desc", "")}
        if "enum" in meta: prop["enum"] = meta["enum"]
        if "default" in meta: prop["default"] = meta["default"]
        if meta.get("required"): required.append(key)
        properties[key] = prop
    schema = {"type": "object", "properties": properties}
    if required: schema["required"] = required
    return schema


def register(skill, client, base_url, dry_run):
    url = f"{UUMIT_API_BASE}/api/v1/data-marketplace/apis"
    payload = {
        "name": skill["name"],
        "description": skill["description"],
        "category": skill["category"],
        "tags": skill.get("tags", []),
        "upstream_method": skill.get("method", "GET"),
        "upstream_url": base_url + skill.get("endpoint", ""),
        "request_schema": build_request_schema(skill),
        "response_schema": {"type": "object", "properties": {"count": {"type": "integer"}, "data": {"type": "array"}}},
        "price_ut": str(skill["pricing"]["amount"]),
        "detail_content": skill.get("detail", skill["description"]),
    }
    if dry_run:
        print(f"  [DRY RUN] {skill['name']} | {payload['price_ut']} UT")
        return True
    try:
        resp = client.post(url, json=payload, headers={
            "X-Api-Key": UUMIT_API_KEY, "X-Platform-User-Id": UUMIT_USER_ID,
            "Content-Type": "application/json"}, timeout=30)
        if resp.status_code in (200, 201):
            print(f"  [OK] {skill['name']} | {payload['price_ut']} UT")
            return True
        print(f"  [FAIL] {skill['name']}: HTTP {resp.status_code} - {resp.text[:200]}")
        return False
    except Exception as e:
        print(f"  [ERR] {skill['name']}: {e}")
        return False


def main():
    dry_run = "--dry-run" in sys.argv or "-n" in sys.argv
    print(f"=== UUMit {'DRY RUN' if dry_run else '数据广场上架'} ===\n")

    if not dry_run and not UUMIT_API_KEY:
        print("error: UUMIT_API_KEY not set"); sys.exit(1)

    cfg = load_config()
    skills = cfg.get("skills", [])
    combos = cfg.get("combos", [])
    base_url = cfg.get("base_url", "")
    all_items = skills + combos

    print(f"共 {len(all_items)} 个 API ({len(skills)} + {len(combos)} 组合)\n")

    with httpx.Client() as client:
        ok = fail = 0
        for item in all_items:
            if register(item, client, base_url, dry_run): ok += 1
            else: fail += 1
    print(f"\n--- {ok} OK, {fail} FAIL ---")


if __name__ == "__main__":
    main()
