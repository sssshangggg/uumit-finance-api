"""
缓存层 —— 对 Tushare 查询结果做内存缓存，避免重复请求。
"""
import hashlib
import json
import time
from threading import Lock
from typing import Any, Optional


class QueryCache:
    """简单的 TTL 内存缓存，适合单进程部署。"""

    def __init__(self, ttl_seconds: int = 300):
        self._ttl = ttl_seconds
        self._store: dict[str, tuple[float, Any]] = {}
        self._lock = Lock()

    def _make_key(self, func_name: str, kwargs: dict) -> str:
        raw = json.dumps({"f": func_name, "a": kwargs}, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(raw.encode()).hexdigest()

    def get(self, func_name: str, kwargs: dict) -> Optional[Any]:
        key = self._make_key(func_name, kwargs)
        with self._lock:
            entry = self._store.get(key)
            if entry is None:
                return None
            ts, val = entry
            if time.time() - ts > self._ttl:
                del self._store[key]
                return None
            return val

    def set(self, func_name: str, kwargs: dict, value: Any) -> None:
        key = self._make_key(func_name, kwargs)
        with self._lock:
            self._store[key] = (time.time(), value)

    def clear(self) -> None:
        with self._lock:
            self._store.clear()


# 全局单例
cache = QueryCache()
