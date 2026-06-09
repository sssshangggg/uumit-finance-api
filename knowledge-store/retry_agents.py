# -*- coding: utf-8 -*-
import json, httpx, os
from dotenv import load_dotenv
load_dotenv()

UUMIT_API_KEY = os.getenv("UUMIT_API_KEY", "tmHkMAh5LN1ygSdx05tYVz4qt_grFGuTIn6e3AEBjAtwxwdBQvGHsPjKgMamW9NP")
UUMIT_USER_ID = os.getenv("UUMIT_USER_ID", "71e2c0fd-f489-476b-b79b-005de54b6ed7")
API_BASE = "https://api.uumit.com"
headers = {
    "X-Api-Key": UUMIT_API_KEY,
    "X-Platform-User-Id": UUMIT_USER_ID,
    "Content-Type": "application/json",
}

retry = [
    {
        "title": "多平台内容格式适配Agent（一稿多用排版+发布策略）",
        "description": "输入一篇长文，自动输出适配多个主流内容平台的版本：短图文平台（结构化+话题标签）、短视频口播稿（口语化+节奏切分）、长文平台（分段+金句提取）、问答平台（深度拓展+引用格式）、社交动态（短文案+配图建议）。附各平台最佳发布时间表和发布顺序策略。专注内容格式转换，不涉及自动发布。",
        "category": "digital_asset",
        "tags": ["内容分发", "格式适配", "自媒体", "多平台", "排版", "AI Agent", "工作流"],
        "capability_type": "data",
        "delivery_mode": "instant",
        "pricing_model": "fixed",
        "price_ut": "3900",
        "has_deliverable": True,
    },
    {
        "title": "个人IP年度内容日历Agent（栏目体系+30天日更计划+热点预植入）",
        "description": "专为知识付费创作者打造。输入个人定位和擅长领域，AI生成：内容栏目体系（3-5个固定栏目）、30天日更日历（含每日选题方向+标题建议+内容形式）、12个月热点事件预植入表（节假日/行业峰会/社会热点）、发布后效果追踪模板。输出Excel日历+热点预埋表，拿到就能用。适合内容创作者、知识付费讲师。",
        "category": "digital_asset",
        "tags": ["个人IP", "内容日历", "知识付费", "自媒体", "选题", "AI Agent", "工作流"],
        "capability_type": "data",
        "delivery_mode": "instant",
        "pricing_model": "fixed",
        "price_ut": "5900",
        "has_deliverable": True,
    },
]

url = f"{API_BASE}/api/v1/capabilities"
ok = fail = 0
with httpx.Client(timeout=30) as client:
    for item in retry:
        try:
            resp = client.post(url, json=item, headers=headers)
            if resp.status_code in (200, 201):
                data = resp.json()
                pid = data.get("data", {}).get("id", "?")
                print(f"  [OK] {item['title'][:50]}... | {item['price_ut']} UT | id={pid}")
                ok += 1
            else:
                print(f"  [FAIL] {item['title'][:50]}... | HTTP {resp.status_code} | {resp.text[:200]}")
                fail += 1
        except Exception as e:
            print(f"  [ERR] {item['title'][:50]}... | {e}")
            fail += 1

print(f"\n--- 补上架: {ok} OK, {fail} FAIL ---")
