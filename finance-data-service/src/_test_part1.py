import re as _re
from datetime import date, timedelta
import json as _json
import httpx

# ============ 工具 4: 违禁词检测 ============

AD_LAW_BANNED = [
    "国家级", "世界级", "最高级", "最佳", "最大", "第一", "唯一", "首个", "首选",
    "最好", "最先进", "最便宜", "最低价", "最受欢迎", "最有效", "最天然",
    "顶级", "极品", "终极", "极致", "绝无仅有", "空前绝后", "独一无二", "万能",
    "第一品牌", "金牌", "王牌", "领袖品牌", "王者", "冠军", "全网第一",
    "销量第一", "排名第一", "市场占有率第一", "100%", "百分百", "彻底", "完全",
    "根治", "根除", "永不", "永久", "祖传", "特效", "神效", "奇效",
    "最新科学", "最新技术", "最先进工艺", "填补国内空白", "国际品质",
]

PLATFORM_BANNED = [
    "加微信", "加V", "加薇", "加v信", "加我微信", "扫码加", "私信我",
    "微信号", "vx", "VX", "QQ号", "手机号", "联系电话", "联系方式",
    "免费领取", "免费送", "免费拿", "白送", "不要钱",
    "点击购买", "立即下单", "马上下单", "限时抢购", "秒杀", "疯抢",
    "赚钱", "日入", "月入", "年入", "躺赚", "暴富", "发财",
    "包过", "保过", "必过", "稳赚", "保收益", "零风险",
    "最便宜", "最低", "全网最低", "历史最低", "亏本", "亏本卖",
    "假一赔十", "假一罚十", "假一赔百",
    "点击链接", "复制链接", "打开淘宝", "打开拼多多",
    "刷单", "刷量", "刷粉", "刷赞", "刷评论", "水军",
]

INDUSTRY_BANNED = {
    "医疗": ["治愈", "根除", "无副作用", "纯天然", "无添加", "不复发", "一个疗程见效", "三天见效"],
    "金融": ["保本", "保息", "无风险", "稳赚不赔", "年化收益", "承诺收益", "刚性兑付", "零风险"],
    "教育": ["包过", "保过", "包录取", "签约保分", "命题组", "内部资料", "真题答案"],
    "食品": ["治疗", "预防疾病", "增强免疫力", "排毒", "减肥", "瘦身"],
}

BANNED_REGEX_PATTERNS = [
    (r"加\s*[vV薇]\s*[信]?", "疑似引流行为"),
    (r"[vV]\s*[xX信]", "疑似引流行为"),
    (r"微\s*信\s*[号号]", "疑似引流行为"),
    (r"[1-9]\d{4,10}", "疑似联系方式"),
    (r"最\s*[好大优强棒赞牛]", "疑似极限用语"),
    (r"[1-9]0{1,2}\s*%", "疑似绝对化承诺"),
    (r"[日年月]入?\s*[1-9]\d{2,4}", "疑似收益承诺"),
    (r"扫\s*码|二维\s*码", "疑似引流行为"),
]

def check_banned_words(text):
    if not text or len(text) < 2:
        return {"has_violation": False, "total_flags": 0, "flags": [], "summary": "文本过短"}
    flags = []
    text_lower = text.lower()
    for word in AD_LAW_BANNED:
        if word in text:
            idx = text.index(word)
            flags.append({"word": word, "position": idx, "category": "广告法违禁词", "category_en": "ad_law", "severity": "high", "suggestion": f"建议将\u201c{word}\u201d替换为客观描述"})
    for word in PLATFORM_BANNED:
        if word.lower() in text_lower:
            idx = text_lower.index(word.lower())
            sev = "high" if any(kw in word for kw in ["微信", "加", "扫码", "免费", "赚钱"]) else "medium"
            flags.append({"word": word, "position": idx, "category": "平台违禁词", "category_en": "platform", "severity": sev, "suggestion": f"建议删除或替换\u201c{word}\u201d"})
    for industry, words in INDUSTRY_BANNED.items():
        for word in words:
            if word in text:
                idx = text.index(word)
                flags.append({"word": word, "position": idx, "category": f"{industry}行业敏感词", "category_en": "industry", "severity": "high", "suggestion": f"涉及{industry}行业，建议删除或提供资质"})
    for pattern, desc in BANNED_REGEX_PATTERNS:
        for match in _re.finditer(pattern, text):
            matched = match.group()
            if not any(f.get("word") == matched for f in flags):
                flags.append({"word": matched, "position": match.start(), "category": desc, "category_en": "regex_pattern", "severity": "high", "suggestion": f"检测到{desc}，建议修改"})
    flags.sort(key=lambda x: x["position"])
    return {
        "has_violation": len(flags) > 0,
        "total_flags": len(flags),
        "flags_by_category": {
            "广告法": len([f for f in flags if f["category_en"] == "ad_law"]),
            "平台规则": len([f for f in flags if f["category_en"] == "platform"]),
            "行业敏感": len([f for f in flags if f["category_en"] == "industry"]),
            "变体检测": len([f for f in flags if f["category_en"] == "regex_pattern"]),
        },
        "flags": flags,
        "summary": f"共检测到 {len(flags)} 个违禁/敏感词" if flags else "未检测到违禁词",
    }

print("PART1_OK")