import httpx, os
from dotenv import load_dotenv
load_dotenv(r"C:\Users\MECHREVO\Documents\UUMit\finance-data-service\.env")

API_BASE = "https://api.uumit.com"
headers = {
    "X-Api-Key": os.getenv("UUMIT_API_KEY"),
    "X-Platform-User-Id": os.getenv("UUMIT_USER_ID"),
    "Content-Type": "application/json",
}

fixes = [
    ("a32a21b5-19f7-4ba5-b5ee-6bdff158a6d2", "全网热榜实时选题工具（多来源热搜聚合+财经筛选+选题建议）"),
    ("001a5479-66d4-4f73-89ea-2b6c9c1dd6fa", "内容账号冷启动30天SOP（日更计划+选题日历+涨粉实操）"),
    ("76a7d6e3-5dc0-4c4f-b8b4-d32bbd9d6ec8", "私域运营全流程SOP手册（获客+转化+复购+裂变四步闭环）"),
    ("b9d63bc3-909b-4086-8954-a89006b8932e", "内容排版美学模板包（10种风格+交互组件+品牌配色指南）"),
]

for pid, new_title in fixes:
    r = httpx.put(f"{API_BASE}/api/v1/capabilities/{pid}", json={"title": new_title}, headers=headers, timeout=10)
    status = "OK" if r.status_code == 200 else f"FAIL {r.status_code}"
    resp_title = r.json().get("data", {}).get("title", "")[:50]
    print(f"[{status}] {pid[:8]}... -> {resp_title}")