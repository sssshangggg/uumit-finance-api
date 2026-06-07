import json, os, httpx
from dotenv import load_dotenv
load_dotenv()

UUMIT_API_KEY = os.getenv("UUMIT_API_KEY", "tmHkMAh5LN1ygSdx05tYVz4qt_grFGuTIn6e3AEBjAtwxwdBQvGHsPjKgMamW9NP")
UUMIT_USER_ID = os.getenv("UUMIT_USER_ID", "71e2c0fd-f489-476b-b79b-005de54b6ed7")
API_BASE = "https://api.uumit.com"

KNOWLEDGE_ITEMS = [
    {
        "title": "A股量化选股实战框架（附5个可运行策略）",
        "description": "面向Python投资者的完整A股量化选股方法论。从数据获取、因子构建（动量/波动率/估值/量价四因子）、多因子评分到策略回测，每章配可运行代码。附赠5个策略脚本：双均线动量、低波动选股、多因子打分、财报超预期、行业轮动ETF。7天学习计划，学完可独立搭建半自动选股系统。",
        "category": "digital_asset",
        "tags": ["量化投资", "A股", "Python", "选股策略", "因子投资", "回测", "金融"],
        "capability_type": "data",
        "delivery_mode": "instant",
        "pricing_model": "fixed",
        "price_ut": "20",
        "has_deliverable": True,
    },
    {
        "title": "上市公司财报速读指南（三张表拆解法+估值模型）",
        "description": "5分钟判断一家公司靠不靠谱的实战财报阅读方法论。三张核心报表（利润表/资产负债表/现金流量表）每张只需看3个数字，附带16个行业的健康阈值速查表。包含：银行/地产/科技行业的特殊指标、财务报表常见猫腻识别、附赠Python自动提取脚本。适合无会计基础的投资者和产品经理。7天从零到独立分析。",
        "category": "digital_asset",
        "tags": ["财报分析", "财务分析", "投资", "基本面", "资产负债表", "利润表", "金融"],
        "capability_type": "data",
        "delivery_mode": "instant",
        "pricing_model": "fixed",
        "price_ut": "13",
        "has_deliverable": True,
    },
    {
        "title": "中国宏观经济分析手册（GDP/CPI/M2联动解读）",
        "description": "7大核心宏观指标的完整解读框架：GDP三驾马车/CPI-PPI剪刀差/M1-M2剪刀差/PMI枯荣线/LPR利率传导/社融结构分析。每个指标附带查询接口代码和解读模板。包含美林时钟中国版判断方法、不同经济周期的资产配置策略、每日宏观速览Python脚本。学完可独立输出专业级宏观分析报告。",
        "category": "digital_asset",
        "tags": ["宏观经济", "GDP", "CPI", "货币政策", "经济周期", "资产配置", "金融"],
        "capability_type": "data",
        "delivery_mode": "instant",
        "pricing_model": "fixed",
        "price_ut": "15",
        "has_deliverable": True,
    },
]

def register_knowledge(items):
    url = f"{API_BASE}/api/v1/capabilities"
    headers = {
        "X-Api-Key": UUMIT_API_KEY,
        "X-Platform-User-Id": UUMIT_USER_ID,
        "Content-Type": "application/json",
    }
    
    ok = fail = 0
    with httpx.Client(timeout=30) as client:
        for item in items:
            try:
                resp = client.post(url, json=item, headers=headers)
                if resp.status_code in (200, 201):
                    data = resp.json()
                    print(f"  [OK] {item['title'][:40]}... | {item['price_ut']} UT | id={data.get('data', {}).get('id', '?')}")
                    ok += 1
                else:
                    print(f"  [FAIL] {item['title'][:40]}... | HTTP {resp.status_code} | {resp.text[:200]}")
                    fail += 1
            except Exception as e:
                print(f"  [ERR] {item['title'][:40]}... | {e}")
                fail += 1
    
    print(f"\n--- {ok} OK, {fail} FAIL ---")

if __name__ == "__main__":
    register_knowledge(KNOWLEDGE_ITEMS)
