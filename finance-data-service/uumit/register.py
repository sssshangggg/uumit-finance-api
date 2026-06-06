"""
UUMit 数据广场 API 批量上架脚本
读取 skills.json，批量注册到 UUMit 数据广场。
"""
import json
import os
import sys
import httpx

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "skills.json")

for i, arg in enumerate(sys.argv):
    if arg == "--file" and i + 1 < len(sys.argv):
        CONFIG_PATH = sys.argv[i + 1]
        sys.argv.pop(i)
        sys.argv.pop(i)
        break

UUMIT_API_BASE = os.getenv("UUMIT_API_BASE", "https://api.uumit.com")
UUMIT_API_KEY = os.getenv("UUMIT_API_KEY", "")
UUMIT_USER_ID = os.getenv("UUMIT_USER_ID", "")


def load_skills():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def build_request_schema(skill):
    """把 params 转成数据广场的 request_schema 格式"""
    params = skill.get("params", {})
    required = []
    properties = {}
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
    return schema


def build_response_schema(skill):
    """通用响应结构"""
    return {
        "type": "object",
        "properties": {
            "count": {"type": "integer", "description": "返回数据条数"},
            "data": {"type": "array", "description": "数据记录列表"},
        },
    }


def register_to_marketplace(skill, client, dry_run=False):
    """注册单个 API 到数据广场"""
    url = f"{UUMIT_API_BASE}/api/v1/data-marketplace/apis"

    payload = {
        "name": skill["name"],
        "description": skill["description"],
        "category": skill["category"],
        "tags": skill.get("tags", []),
        "upstream_method": skill.get("method", "GET"),
        "request_schema": build_request_schema(skill),
        "response_schema": build_response_schema(skill),
        "price_ut": str(skill["pricing"]["amount"]),
        "detail_content": skill.get("detail", skill["description"]),
    }

    if dry_run:
        print("  [DRY RUN] POST {} -> {} ({} UT)".format(
            url.split("/apis")[0], skill["name"], payload["price_ut"]))
        return True

    try:
        resp = client.post(url, json=payload, headers={
            "X-Api-Key": UUMIT_API_KEY,
            "X-Platform-User-Id": UUMIT_USER_ID,
            "Content-Type": "application/json",
        }, timeout=30)
        if resp.status_code in (200, 201):
            print("  [OK] {} | {} UT".format(skill["name"], payload["price_ut"]))
            return True
        else:
            print("  [FAIL] {}: HTTP {} - {}".format(
                skill["name"], resp.status_code, resp.text[:200]))
            return False
    except Exception as e:
        print("  [ERR] {}: {}".format(skill["name"], e))
        return False


def main():
    dry_run = "--dry-run" in sys.argv or "-n" in sys.argv

    if dry_run:
        print("=== UUMit 数据广场上架 (DRY RUN) ===\n")
    else:
        if not UUMIT_API_KEY:
            print("error: UUMIT_API_KEY not set")
            sys.exit(1)
        print("=== UUMit 数据广场上架 ===\n")

    config = load_skills()
    skills = config.get("skills", [])
    combos = config.get("combos", [])
    all_items = skills + combos

    print("共 {} 个 API ({} 独立 + {} 组合)\n".format(
        len(all_items), len(skills), len(combos)))

    with httpx.Client() as client:
        ok = 0
        fail = 0
        for item in all_items:
            if register_to_marketplace(item, client, dry_run=dry_run):
                ok += 1
            else:
                fail += 1

    print("\n--- 结果: {} OK, {} FAIL ---".format(ok, fail))


if __name__ == "__main__":
    main()
