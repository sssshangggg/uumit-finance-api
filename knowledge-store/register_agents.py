# -*- coding: utf-8 -*-
"""UUMit AI Agent 工作流 — 10件商品批量上架
汇率: 100 UT = 1 RMB
"""
import json, os, httpx
from dotenv import load_dotenv
load_dotenv()

UUMIT_API_KEY = os.getenv("UUMIT_API_KEY", "tmHkMAh5LN1ygSdx05tYVz4qt_grFGuTIn6e3AEBjAtwxwdBQvGHsPjKgMamW9NP")
UUMIT_USER_ID = os.getenv("UUMIT_USER_ID", "71e2c0fd-f489-476b-b79b-005de54b6ed7")
API_BASE = "https://api.uumit.com"

# ============================================================
# 10个AI Agent工作流产品定义 (汇率: 100 UT = 1 RMB)
# ============================================================

PRODUCTS = [
    # === 第一批: 首发3件 (最稳+高客单价+易出案例) ===
    {
        "title": "虚拟商品蓝海选品Agent（多平台热榜交叉验证+竞争缺口评分）",
        "description": "帮你挖出电商平台上的冷门虚拟品蓝海。聚合小红书/抖音/1688三大平台热榜，提取高频关键词后交叉验证淘宝/拼多多销量与竞争度，输出带评分的选品推荐报告。解决'不知道卖什么'和'选的品已经红海'两大痛点。每份报告含10-20个候选品，按竞争缺口评分排序，附每个品的目标人群画像和定价建议。数据源均为公开平台，合规无风险。",
        "category": "digital_asset",
        "tags": ["选品", "虚拟电商", "蓝海", "数据分析", "电商", "1688", "小红书", "抖音", "AI Agent", "工作流"],
        "capability_type": "data",
        "delivery_mode": "instant",
        "pricing_model": "fixed",
        "price_ut": "6900",
        "has_deliverable": True,
    },
    {
        "title": "竞品动态监控Agent（定价/功能/招聘三线追踪+周报输出）",
        "description": "指定最多10个竞品，每周自动输出一份竞品周报。三线监控：定价变动（降价/涨价/套餐调整）、功能更新（新功能上线/旧功能下架）、招聘动态（扩招技术岗=有预算，裁员=收缩）。变动对比+异常预警（如竞品突然降价30%自动标红），附应对建议。适合SaaS创业者、产品经理、电商品牌方。纯数据报告，无合规风险。",
        "category": "digital_asset",
        "tags": ["竞品分析", "市场监控", "SaaS", "电商", "数据报告", "周报", "AI Agent", "工作流"],
        "capability_type": "data",
        "delivery_mode": "instant",
        "pricing_model": "fixed",
        "price_ut": "7900",
        "has_deliverable": True,
    },
    {
        "title": "小红书数据复盘+标题优化Agent（单篇笔记深度拆解+优化方案）",
        "description": "不做玄学生成，只做确定性优化。输入你的小红书笔记截图或数据导出，输出：标题关键词评分（含高频词/蓝海词/无效词分类）、封面CTR预估、互动率与同类笔记对比、3版优化标题供替换。聚焦'已经发的笔记怎么改'而非'怎么从零写爆款'，结果可验证、可对比，用户满意度高。单次分析1篇，含优化前后对比表。",
        "category": "digital_asset",
        "tags": ["小红书", "数据分析", "标题优化", "复盘", "内容运营", "AI Agent", "工作流"],
        "capability_type": "data",
        "delivery_mode": "instant",
        "pricing_model": "fixed",
        "price_ut": "2900",
        "has_deliverable": True,
    },
    # === 第二批: 已验证方向 ===
    {
        "title": "短视频脚本拆解+仿写Agent（爆款结构反向工程+3版仿写）",
        "description": "输入任意抖音/视频号爆款视频链接，AI自动拆解：hook类型（悬念/反常识/恐吓/共情）、节奏图谱（秒级情绪曲线）、转化话术点。基于拆解结果仿写3版不同风格脚本（口播/剧情/干货），每版含分镜建议和时长预估。不是简单洗稿，是结构级复刻+风格变体。适合短视频创作者、MCN编导。",
        "category": "digital_asset",
        "tags": ["短视频", "脚本", "拆解", "仿写", "抖音", "视频号", "内容创作", "AI Agent", "工作流"],
        "capability_type": "data",
        "delivery_mode": "instant",
        "pricing_model": "fixed",
        "price_ut": "3900",
        "has_deliverable": True,
    },
    {
        "title": "多平台内容格式适配Agent（一稿多平台排版+发布策略）",
        "description": "输入一篇长文/文案，自动输出适配6个平台的版本：小红书（结构化+emoji+话题标签）、抖音口播稿（口语化+节奏切分）、公众号长文（分段+金句提取）、知乎回答（深度拓展+引用格式）、微博（极简+热搜词植入）、朋友圈（短文案+配图建议）。附各平台最佳发布时间表和发布顺序策略。初期不做自动发布（避免API权限问题），专注内容格式转换。",
        "category": "digital_asset",
        "tags": ["多平台", "内容分发", "格式适配", "自媒体", "小红书", "抖音", "公众号", "AI Agent", "工作流"],
        "capability_type": "data",
        "delivery_mode": "instant",
        "pricing_model": "fixed",
        "price_ut": "3900",
        "has_deliverable": True,
    },
    {
        "title": "B2B销售线索发现Agent（招聘信息监控版）",
        "description": "聚焦单一高价值信号：招聘信息。持续监控目标行业/地区的技术岗招聘动态，识别'扩招=有预算'的强信号企业。每日输出线索简报：公司名、融资轮次、当前招聘岗位数、技术岗占比变化、推测预算区间、推荐触达话术。初期聚焦'招聘信息'单一源，落地难度低，信号可靠性高。适合SaaS销售、企服BD、猎头。",
        "category": "digital_asset",
        "tags": ["B2B", "销售线索", "招聘监控", "SaaS", "企业服务", "AI Agent", "工作流"],
        "capability_type": "data",
        "delivery_mode": "instant",
        "pricing_model": "fixed",
        "price_ut": "6900",
        "has_deliverable": True,
    },
    {
        "title": "店铺Review舆情分析Agent（多平台评论聚合+差评根因诊断）",
        "description": "聚合淘宝/京东/拼多多/Amazon的用户评论，自动完成：情感分类（正面/中性/负面占比）、高频词云提取、差评根因聚类（物流/质量/客服/描述不符/其他）、基于差评改进建议优先级排序、好评回复模板自动生成（含不同风格：专业/温暖/幽默）。适合电商卖家、品牌运营、产品经理。提供3份不同品类示例报告作为选购参考。",
        "category": "digital_asset",
        "tags": ["舆情分析", "评论分析", "电商", "差评诊断", "用户研究", "AI Agent", "工作流"],
        "capability_type": "data",
        "delivery_mode": "instant",
        "pricing_model": "fixed",
        "price_ut": "4900",
        "has_deliverable": True,
    },
    # === 第三批: 经调整的专项 ===
    {
        "title": "A股财报关键数据预警Agent（营收/利润/现金流三线监控+阈值预警）",
        "description": "聚焦财报披露期，监控指定股票池（最多10只）的营收、净利润、毛利率、经营现金流等5项核心指标。当任一指标环比/同比变化超过预设阈值（如营收增50%或降30%），自动推送预警通知。数据来源于公开财报（巨潮资讯/交易所公告），无合规风险。每季度更新监控池，支持自定义阈值。适合基本面投资者、价值投资者。",
        "category": "digital_asset",
        "tags": ["A股", "财报", "预警", "基本面", "投资", "财务分析", "AI Agent", "工作流"],
        "capability_type": "data",
        "delivery_mode": "instant",
        "pricing_model": "fixed",
        "price_ut": "3900",
        "has_deliverable": True,
    },
    {
        "title": "个人IP年度内容日历Agent（栏目体系+30天日更日历+热点预植入）",
        "description": "专为知识付费创作者打造。输入你的个人定位和擅长领域，AI生成：内容栏目体系（3-5个固定栏目）、30天日更日历（含每日选题方向+标题建议+内容形式）、12个月热点事件预植入表（节假日/行业峰会/社会热点）、发布后效果追踪模板。输出Excel日历+热点预埋表，拿到就能用。适合小红书博主、公众号作者、知识付费讲师。",
        "category": "digital_asset",
        "tags": ["个人IP", "内容日历", "知识付费", "自媒体", "选题", "AI Agent", "工作流"],
        "capability_type": "data",
        "delivery_mode": "instant",
        "pricing_model": "fixed",
        "price_ut": "5900",
        "has_deliverable": True,
    },
    {
        "title": "高赞AI工具需求清单（周更·小红书/Twitter/Product Hunt三源精选20条）",
        "description": "每周整理20条来自小红书、Twitter(X)、Product Hunt的AI工具真实需求。每条含：原文链接、平台点赞/转发数、需求描述（一句话概括用户痛点）、已有竞品缺口分析（市面上有没有人在做/做得怎么样）、难度评级（低/中/高）。用户拿到的是一份可直接选品或找外包的需求清单，交付最轻、价值最直观。适合非技术创业者、产品经理、独立开发者。",
        "category": "digital_asset",
        "tags": ["AI工具", "需求挖掘", "产品灵感", "选品", "Product Hunt", "小红书", "Twitter", "周更", "AI Agent"],
        "capability_type": "data",
        "delivery_mode": "instant",
        "pricing_model": "fixed",
        "price_ut": "1900",
        "has_deliverable": True,
    },
]

def register_products(products, dry_run=False):
    url = f"{API_BASE}/api/v1/capabilities"
    headers = {
        "X-Api-Key": UUMIT_API_KEY,
        "X-Platform-User-Id": UUMIT_USER_ID,
        "Content-Type": "application/json",
    }

    ok = fail = 0
    results = []
    with httpx.Client(timeout=30) as client:
        for item in products:
            price_rmb = int(item["price_ut"]) / 100
            if dry_run:
                print(f"  [DRY RUN] {item['title'][:50]}... | {item['price_ut']} UT (RMB{price_rmb:.2f}) | tags={len(item['tags'])}")
                ok += 1
                continue
            try:
                resp = client.post(url, json=item, headers=headers)
                if resp.status_code in (200, 201):
                    data = resp.json()
                    pid = data.get("data", {}).get("id", "?")
                    print(f"  [OK] {item['title'][:50]}... | {item['price_ut']} UT (RMB{price_rmb:.2f}) | id={pid}")
                    results.append({"title": item["title"], "id": pid, "price_ut": item["price_ut"], "status": "ok"})
                    ok += 1
                else:
                    print(f"  [FAIL] {item['title'][:50]}... | HTTP {resp.status_code} | {resp.text[:150]}")
                    results.append({"title": item["title"], "status": "fail", "code": resp.status_code, "body": resp.text[:150]})
                    fail += 1
            except Exception as e:
                print(f"  [ERR] {item['title'][:50]}... | {e}")
                results.append({"title": item["title"], "status": "error", "error": str(e)})
                fail += 1

    mode = "DRY RUN" if dry_run else "上架"
    print(f"\n--- {mode}: {ok} OK, {fail} FAIL (共{len(products)}件) ---")

    # Summary by batch
    total_ut = sum(int(p["price_ut"]) for p in products)
    total_rmb = total_ut / 100
    print(f"总UT价值: {total_ut:,} UT (RMB{total_rmb:.2f})")
    return results

if __name__ == "__main__":
    import sys
    dry_run = "--dry-run" in sys.argv or "-n" in sys.argv or "--dry" in sys.argv
    if dry_run:
        print("=== UUMit AI Agent工作流 DRY RUN ===\n")
    else:
        print("=== UUMit AI Agent工作流 正式上架 ===\n")
    register_products(PRODUCTS, dry_run=dry_run)
