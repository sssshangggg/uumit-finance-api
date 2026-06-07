import httpx, json

url = "https://shirt-conjoined-rasping.ngrok-free.dev"

# Test 1: POST with JSON body (how our endpoint expects it)
r = httpx.post(f"{url}/api/v1/tools/viral-verify", 
               json={"content": "测试文章内容，需要至少50个字符才能进行有效的爆款验证分析。"}, 
               timeout=10)
print(f"POST json body: {r.status_code}")

# Test 2: POST with form data (maybe UUMit sends form)
r = httpx.post(f"{url}/api/v1/tools/viral-verify",
               data={"content": "test"*20},
               timeout=10)
print(f"POST form data: {r.status_code} | {r.text[:100]}")

# Test 3: GET with query params (maybe UUMit sends GET)
r = httpx.get(f"{url}/api/v1/tools/viral-verify?content=testtest", timeout=10)
print(f"GET query: {r.status_code} | {r.text[:100]}")

# Test 4: POST with query params  
r = httpx.post(f"{url}/api/v1/tools/viral-verify?content=testtest", timeout=10)
print(f"POST query no body: {r.status_code} | {r.text[:100]}")

# Test 5: ngrok skip browser warning header
r = httpx.post(f"{url}/api/v1/tools/viral-verify",
               json={"content": "test"*20},
               headers={"ngrok-skip-browser-warning": "true"},
               timeout=10)
print(f"POST with ngrok header: {r.status_code}")
