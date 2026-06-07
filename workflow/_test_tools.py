import httpx, json

# Test 1: AI Detection
text = "In today's fast-paced digital world, it is important to note that artificial intelligence has become a cornerstone of modern technology. Furthermore, the realm of AI continues to expand rapidly. However, it is worth mentioning that ethical considerations remain crucial. In conclusion, the future of AI is both promising and challenging."
r = httpx.post("http://localhost:8800/api/v1/tools/detect-ai", json={"text": text}, timeout=10)
print("=== AI Detection ===")
d = r.json()
print(f"Score: {d['score']}, Verdict: {d['verdict']}")

# Test 2: Viral Verify
article = "# 68% 的暴增，和 3 万的暴跌，是同一条流水线\n\n你以为出口暴增是好事？其实背后是一场残酷的产业迁徙。\n\n一季度中国电驴对英出口暴增 68.2%。同一个月，国内二手油车跌掉 3 万。\n\n一条流水线出来的东西。在英国被疯抢。在中国掉漆。\n\n这不是消费选择。这是结构性抛弃。\n\n你赌油车回归？看看欧洲碳关税时间表。2027 年全面实施。你确定要赌这个？"
r = httpx.post("http://localhost:8800/api/v1/tools/viral-verify", json={"content": article}, timeout=10)
print("\n=== Viral Verify ===")
d = r.json()
print(f"Score: {d['total_score']}/60, Verdict: {d['verdict']}")
for dim in d['dimensions']:
    print(f"  {dim['name']}: {dim['score']}/10 - {dim['note']}")

# Test 3: Hot Topics
r = httpx.get("http://localhost:8800/api/v1/tools/hot-topics?limit=5", timeout=15)
print("\n=== Hot Topics ===")
d = r.json()
for t in d['topics'][:5]:
    print(f"  #{t['rank']} [{t['source']}] {t['title'][:50]}")
