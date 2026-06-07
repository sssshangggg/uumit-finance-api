import httpx

url = "https://shirt-conjoined-rasping.ngrok-free.dev"

# Check hot-topics raw response
r = httpx.get(f"{url}/api/v1/tools/hot-topics?limit=3", timeout=10)
print(f"Hot topics: {r.status_code}")
print(f"Body: {r.text[:300]}")

# Also check locally
r = httpx.get("http://localhost:8800/api/v1/tools/hot-topics?limit=3", timeout=10)
print(f"\nHot topics local: {r.status_code}")
print(f"Body: {r.text[:300]}")
