import httpx, json

url = "https://shirt-conjoined-rasping.ngrok-free.dev"

# Test without ngrok header to confirm the error
r = httpx.post(f"{url}/api/v1/tools/viral-verify",
               json={"content": "这是一段足够长的测试文本内容，用于验证爆款内容检测API是否能够正常工作。需要至少五十个字符。"},
               timeout=10)
print(f"Without header: {r.status_code} | body={r.text[:200]}")

# Test with ngrok header
r = httpx.post(f"{url}/api/v1/tools/viral-verify",
               json={"content": "这是一段足够长的测试文本内容，用于验证爆款内容检测API是否能够正常工作。需要至少五十个字符。"},
               headers={"ngrok-skip-browser-warning": "true"},
               timeout=10)
print(f"With header: {r.status_code} | body={r.text[:200]}")

# Test hot-topics GET
r = httpx.get(f"{url}/api/v1/tools/hot-topics?limit=3",
              headers={"ngrok-skip-browser-warning": "true"},
              timeout=10)
print(f"Hot topics: {r.status_code} | count={r.json().get('count','?')}")

# Test AI detect
r = httpx.post(f"{url}/api/v1/tools/detect-ai",
               json={"text": "In today's digital landscape, it is important to note that AI has become a cornerstone of modern technology. Furthermore, the realm of AI continues to expand rapidly."},
               headers={"ngrok-skip-browser-warning": "true"},
               timeout=10)
print(f"AI detect: {r.status_code} | score={r.json().get('score','?')}")
