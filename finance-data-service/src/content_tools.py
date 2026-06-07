"""AI 内容工具引擎 — 零外部依赖，纯规则引擎 + 网页抓取"""

import re, math
from collections import Counter
from typing import Optional
import httpx

# ============ 工具 1: AI 文本检测 ============

AI_PATTERNS = [
    r"\bit is (important|worth|essential|crucial) to (note|mention|understand|recognize|consider)\b",
    r"\bin (conclusion|summary|essence|short)\b",
    r"\bfurthermore\b", r"\bmoreover\b", r"\bnevertheless\b", r"\bconsequently\b",
    r"\bhowever\b", r"\btherefore\b", r"\bthus\b", r"\bhence\b",
    r"\b(delve|dive)\s+(into|deep)\b",
    r"\bin today.s (digital|fast-paced|ever-changing|interconnected) (world|landscape|era|age)\b",
    r"\b(unlock|unleash|harness)\s+(the|your|its)\s+(power|potential|full)\b",
    r"\ba\s+(testament|beacon|cornerstone|pillar)\s+(to|of)\b",
    r"\bnot only.*but also\b",
    r"\bin the realm of\b",
    r"\bit is worth noting that\b",
    r"\bfrom this (perspective|standpoint|vantage point)\b",
]

AI_TRANSITIONS = [
    "furthermore", "moreover", "consequently", "nevertheless", "nonetheless",
    "accordingly", "additionally", "specifically", "particularly", "ultimately",
    "in conclusion", "to summarize", "in summary", "as a result", "therefore",
    "thus", "hence", "accordingly", "meanwhile", "subsequently",
]

AI_FILLER = [
    "it is important to note", "it is worth mentioning", "it should be noted",
    "one could argue", "it can be said", "needless to say",
    "as previously mentioned", "as stated earlier",
]


def detect_ai_text(text: str) -> dict:
    """基于启发式规则检测 AI 生成文本的可能性。返回 0-100 分数和详细指标。"""
    if not text or len(text) < 50:
        return {"score": 0, "verdict": "text_too_short", "details": {}}

    # 1. 句子长度方差（AI 文本句子长度更均匀）
    sentences = re.split(r"[。！？.!?\n]+", text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 5]
    if len(sentences) < 3:
        return {"score": 0, "verdict": "too_few_sentences", "details": {}}

    sent_lens = [len(s) for s in sentences]
    avg_len = sum(sent_lens) / len(sent_lens)
    var_len = sum((l - avg_len) ** 2 for l in sent_lens) / len(sent_lens)
    cv = math.sqrt(var_len) / avg_len if avg_len > 0 else 0  # 变异系数

    # 2. AI 模式匹配
    text_lower = text.lower()
    pattern_count = 0
    matched_patterns = []
    for pat in AI_PATTERNS:
        matches = re.findall(pat, text_lower)
        if matches:
            pattern_count += len(matches)
            matched_patterns.append(pat)

    # 3. 过渡词密度
    transition_count = sum(text_lower.count(t) for t in AI_TRANSITIONS)
    word_count = len(text.split())
    transition_density = transition_count / max(word_count, 1) * 100

    # 4. AI 填充词
    filler_count = sum(text_lower.count(f) for f in AI_FILLER)

    # 5. 段落结构（AI 倾向均匀段落长度）
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    if len(paragraphs) >= 2:
        para_lens = [len(p) for p in paragraphs]
        para_avg = sum(para_lens) / len(para_lens)
        para_var = sum((l - para_avg) ** 2 for l in para_lens) / len(para_lens)
        para_cv = math.sqrt(para_var) / para_avg if para_avg > 0 else 0
    else:
        para_cv = 0

    # ---- 评分 ----
    score = 0.0

    # CV < 0.3 说明句子长度太均匀（AI 特征）
    if cv < 0.3:
        score += 25
    elif cv < 0.5:
        score += 15
    elif cv < 0.7:
        score += 5

    # 模式匹配得分
    score += min(pattern_count * 5, 25)

    # 过渡词密度 > 3% 是 AI 特征
    if transition_density > 4:
        score += 20
    elif transition_density > 2.5:
        score += 10

    # 填充词
    score += min(filler_count * 5, 15)

    # 段落 CV
    if len(paragraphs) >= 2 and para_cv < 0.5:
        score += 15

    score = min(score, 100)

    # 判定
    if score >= 70:
        verdict = "likely_ai"
    elif score >= 40:
        verdict = "possibly_ai"
    elif score >= 20:
        verdict = "possibly_human"
    else:
        verdict = "likely_human"

    return {
        "score": round(score, 1),
        "verdict": verdict,
        "details": {
            "sentence_count": len(sentences),
            "sentence_cv": round(cv, 3),
            "pattern_matches": len(matched_patterns),
            "transition_density_pct": round(transition_density, 2),
            "filler_count": filler_count,
            "paragraph_cv": round(para_cv, 3) if len(paragraphs) >= 2 else None,
        },
        "interpretation": {
            "likely_ai": "文本高度疑似 AI 生成，句子结构均匀、过渡词密度高、存在典型 AI 句式",
            "possibly_ai": "文本存在部分 AI 特征，建议人工复核",
            "possibly_human": "文本AI 特征不明显，更接近人类写作风格",
            "likely_human": "文本句子结构自然多变，AI 特征极少，很可能是人类写作",
        }.get(verdict, ""),
    }

# ============ 工具 2: 爆款验证 ============

def verify_viral(content: str) -> dict:
    """六维度爆款要素评分。纯规则引擎，无 AI 依赖。"""
    lines = [l for l in content.strip().split("\n") if l.strip()]
    title = lines[0] if lines else ""

    def _score_curiosity() -> tuple:
        s = 5
        if re.search(r"\d", title): s += 1
        if any(w in title for w in ["vs", "崩", "爆", "跌", "涨", "死", "疯", "狂"]): s += 1
        if "?" in title or "？" in title: s += 1
        early = "\n".join(lines[:5])
        if any(w in early for w in ["你以为", "其实", "不是", "真正", "背后", "本质"]): s += 1
        return min(s, 10), title[:50]

    def _score_emotion() -> tuple:
        s = 5
        for w in ["焦虑", "恐惧", "崩溃", "绝望", "刺痛", "残忍", "暴赚", "疯抢", "清醒", "愤怒"]:
            if w in content: s += 0.5
        return min(int(s), 10), f"检测到 {sum(1 for w in ['焦虑','恐惧','崩溃','绝望','刺痛'] if w in content)} 个高唤醒词"

    def _score_value() -> tuple:
        s = 5
        if re.search(r"\d+(\.\d+)?\s*(元|万|亿|%|英镑|美元|倍)", content): s += 2
        if "|" in content: s += 1
        if re.search(r"\d+\s*倍", content): s += 1
        return min(s, 10), "数据锚点" if s >= 7 else "缺少数据"

    def _score_relevance() -> tuple:
        s = 5
        if any(w in content for w in ["今日", "本周", "最新", "刚刚", "一季度"]): s += 2
        if "TopHub" in content or "热榜" in content: s += 2
        return min(s, 10), "时效性强" if s >= 7 else "时效性弱"

    def _score_pacing() -> tuple:
        short = sum(1 for l in lines if len(l) < 20)
        ratio = short / max(len(lines), 1)
        s = 5
        if ratio > 0.6: s += 2
        if ratio > 0.8: s += 3
        return min(s, 10), f"短句占比 {ratio:.0%}"

    def _score_novelty() -> tuple:
        s = 5
        for w in ["其实", "本质上", "背后", "镜像", "隐喻", "参差", "结构性"]:
            if w in content: s += 0.5
        if "结构性" in content: s += 1
        return min(int(s), 10), "有反直觉视角" if s >= 7 else "观点较常规"

    dims = [
        ("好奇心缺口", *_score_curiosity()),
        ("情绪共鸣", *_score_emotion()),
        ("价值/实用性", *_score_value()),
        ("关联/时效性", *_score_relevance()),
        ("叙事/节奏", *_score_pacing()),
        ("反直觉/新颖性", *_score_novelty()),
    ]

    scores = {d[0]: d[1] for d in dims}
    total = sum(scores.values())

    return {
        "total_score": total,
        "max_score": 60,
        "verdict": "爆款潜力高" if total >= 42 else "爆款潜力中" if total >= 30 else "爆款潜力低",
        "dimensions": [{"name": d[0], "score": d[1], "note": d[2]} for d in dims],
        "quick_tips": _generate_tips(scores),
    }


def _generate_tips(scores: dict) -> list[str]:
    tips = []
    if scores.get("好奇心缺口", 0) < 7:
        tips.append("标题可加数字或对比词增强好奇心")
    if scores.get("情绪共鸣", 0) < 7:
        tips.append("加入具象的人物故事或亲身经历触发共鸣")
    if scores.get("价值/实用性", 0) < 7:
        tips.append("增加具体数据、数字或对比增加实用价值")
    if scores.get("叙事/节奏", 0) < 7:
        tips.append("拆分长段落，增加短句和留白")
    if scores.get("反直觉/新颖性", 0) < 7:
        tips.append("找一个反常识的角度切入，挑战读者预设")
    return tips


# ============ 工具 3: 热点选题 ============

TOPHUB_URL = "https://tophub.today/hot"
UA = "Mozilla/5.0 (compatible; UUMit/1.0)"

def fetch_hot_topics(limit: int = 20) -> list[dict]:
    """从 TopHub 抓取实时热榜，返回结构化话题列表。"""
    r = httpx.get(TOPHUB_URL, headers={"User-Agent": UA}, timeout=15)
    r.raise_for_status()
    text = r.text

    items = []
    li_pat = re.compile(r'<li class="child-item">(.*?)</li>', re.DOTALL)
    for li in li_pat.finditer(text):
        block = li.group(1)
        rank_m = re.search(r'<span[^>]*>\s*(\d+)\s*</span>', block)
        title_m = re.search(r'<p class="medium-txt">\s*<a[^>]*>(.*?)</a>', block, re.DOTALL)
        link_m = re.search(r'<p class="medium-txt">\s*<a href="([^"]*)"', block)
        small_m = re.search(r'<p class="small-txt">\s*(.*?)\s*</p>', block, re.DOTALL)

        if title_m:
            title = re.sub(r"<[^>]*>", "", title_m.group(1)).strip()
            source, hot = "", ""
            if small_m:
                parts = [p.strip() for p in re.split(r"[\u00b7\u2027]", small_m.group(1))]
                source = parts[0] if parts else ""
                hot = parts[1].strip() if len(parts) > 1 else ""
            items.append({
                "rank": int(rank_m.group(1)) if rank_m else 0,
                "title": title,
                "link": link_m.group(1) if link_m else "",
                "source": source.strip(),
                "hot": hot.strip(),
            })

        if len(items) >= limit:
            break

    return items

