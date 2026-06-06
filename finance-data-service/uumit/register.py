"""
UUMit 技能一键注册脚本
读取 skills.json，批量注册到 UUMit 平台。
"""
import json
import os
import sys

import httpx

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "skills.json")
UUMIT_API_BASE = os.getenv("UUMIT_API_BASE", "https://api.uumit.com")
UUMIT_API_KEY = os.getenv("UUMIT_API_KEY", "")
UUMIT_USER_ID = os.getenv("UUMIT_USER_ID", "")


def load_skills() -> dict:
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def register_skill(skill: dict, client: httpx.Client, dry_run: bool = False) -> bool:
    """注册单个技能到 UUMit。"""
    url = f"{UUMIT_API_BASE}/api/v1/skills/"

    # 构建符合 UUMit API 的请求体
    # 字段参考: https://uumit.com/docs/guides/register-first-skill/
    payload = {
        "name": skill["name"],
        "description": skill["description"],
        "category": skill["category"],
        "pricing": {
            "model": skill["pricing"]["model"],
            "amount": skill["pricing"]["amount"],
            "currency": skill["pricing"].get("currency", "UT"),
        },
        "mode": skill.get("mode", "online"),
        "metadata": {
            "endpoint": skill.get("endpoint", ""),
            "method": skill.get("method", "GET"),
            "params": skill.get("params", {}),
        },
    }

    if dry_run:
        print(f"  [DRY RUN] POST {url} -> {skill['name']} ({skill['category']})")
        return True

    try:
        resp = client.post(
            url,
            json=payload,
            headers={
                "X-Api-Key": UUMIT_API_KEY,
                "X-Platform-User-Id": UUMIT_USER_ID,
                "Content-Type": "application/json",
            },
            timeout=30,
        )
        if resp.status_code in (200, 201):
            print(f"  [OK] {skill['name']} ({skill['category']})")
            return True
        else:
            print(f"  [FAIL] {skill['name']}: HTTP {resp.status_code} — {resp.text[:200]}")
            return False
    except Exception as e:
        print(f"  [ERR] {skill['name']}: {e}")
        return False


def main():
    dry_run = "--dry-run" in sys.argv or "-n" in sys.argv

    if dry_run:
        print("=== UUMit 技能注册 (DRY RUN 模式) ===\n")
    else:
        if not UUMIT_API_KEY:
            print("错误: 请设置环境变量 UUMIT_API_KEY")
            print("或者使用 --dry-run 模式预览注册内容")
            sys.exit(1)
        print("=== UUMit 技能注册 ===\n")

    config = load_skills()
    skills = config.get("skills", [])
    combos = config.get("combos", [])
    all_items = skills + combos

    print(f"共 {len(all_items)} 个技能待注册 ({len(skills)} 独立 + {len(combos)} 组合)\n")

    with httpx.Client() as client:
        success = 0
        fail = 0
        for item in all_items:
            ok = register_skill(item, client, dry_run=dry_run)
            if ok:
                success += 1
            else:
                fail += 1

    print(f"\n--- 注册结果: 成功 {success}, 失败 {fail} ---")


if __name__ == "__main__":
    main()
