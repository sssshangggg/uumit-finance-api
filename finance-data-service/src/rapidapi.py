"""
RapidAPI 中间件
验证来自 RapidAPI 代理的请求，提取用户信息用于计费和限流。
"""
import os
import hashlib
import hmac
import time
from collections import defaultdict
from typing import Optional

from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse


class RapidAPIMiddleware(BaseHTTPMiddleware):
    """验证 RapidAPI 代理请求，可选限流。

    RapidAPI 通过代理转发请求时，会注入以下 header：
    - X-RapidAPI-Proxy-Secret: 你设置的代理密钥
    - X-RapidAPI-User: 调用者的 RapidAPI 账户 ID
    - X-RapidAPI-Subscription: 订阅计划 (BASIC/PRO/ULTRA)
    - X-Forwarded-For: 真实客户端 IP
    """

    # 免费路径，不需要 RapidAPI 密钥
    PUBLIC_PATHS = {"/", "/docs", "/openapi.json", "/redoc"}

    def __init__(self, app, proxy_secret: str = "", rate_limit_per_min: int = 60):
        super().__init__(app)
        self.proxy_secret = proxy_secret
        self.rate_limit_per_min = rate_limit_per_min
        self._usage: dict[str, list[float]] = defaultdict(list)

    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        # 公开路径直接放行
        if path in self.PUBLIC_PATHS or path.startswith("/docs") or path.startswith("/openapi"):
            return await call_next(request)

        # 检查是否是 RapidAPI 请求
        is_rapidapi = "x-rapidapi-proxy-secret" in request.headers or "x-rapidapi-user" in request.headers

        if is_rapidapi and self.proxy_secret:
            proxy_secret = request.headers.get("x-rapidapi-proxy-secret", "")
            if not hmac.compare_digest(proxy_secret, self.proxy_secret):
                return JSONResponse(
                    status_code=403,
                    content={"error": "invalid_proxy_secret", "detail": "RapidAPI proxy secret mismatch"},
                )

            # 限流检查
            user = request.headers.get("x-rapidapi-user", "anonymous")
            if self.rate_limit_per_min > 0:
                now = time.time()
                window = now - 60
                self._usage[user] = [t for t in self._usage.get(user, []) if t > window]
                if len(self._usage[user]) >= self.rate_limit_per_min:
                    return JSONResponse(
                        status_code=429,
                        content={"error": "rate_limited", "detail": f"Max {self.rate_limit_per_min} req/min"},
                        headers={"X-RateLimit-Limit": str(self.rate_limit_per_min), "Retry-After": "60"},
                    )
                self._usage[user].append(now)

        # 非 RapidAPI 请求直接放行（UUMit 用自己的 API key 认证）
        response = await call_next(request)

        # 注入 RapidAPI 响应头
        if is_rapidapi:
            response.headers["X-Powered-By"] = "UUMit-Finance-RapidAPI"
            response.headers["X-RapidAPI-User"] = request.headers.get("x-rapidapi-user", "unknown")

        return response


def get_rapidapi_middleware() -> Optional[RapidAPIMiddleware]:
    """从环境变量创建 RapidAPI 中间件，未配置则返回 None。"""
    secret = os.getenv("RAPIDAPI_PROXY_SECRET", "")
    rate_limit = int(os.getenv("RAPIDAPI_RATE_LIMIT", "60"))
    if secret:
        return RapidAPIMiddleware(app=None, proxy_secret=secret, rate_limit_per_min=rate_limit)
    return None
