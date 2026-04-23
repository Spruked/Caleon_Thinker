import time
from typing import Any, Optional


class ResponseCache:
    def __init__(self, default_ttl: int = 300):
        self._store: dict = {}
        self._default_ttl = default_ttl
        self._hits = 0
        self._misses = 0

    def get(self, key: str) -> Optional[Any]:
        item = self._store.get(key)
        if not item:
            self._misses += 1
            return None
        if item["expires_at"] < time.time():
            del self._store[key]
            self._misses += 1
            return None
        self._hits += 1
        return item["value"]

    def set(self, key: str, value: Any, ttl_seconds: int = None) -> None:
        ttl = ttl_seconds if ttl_seconds is not None else self._default_ttl
        self._store[key] = {
            "value": value,
            "expires_at": time.time() + ttl,
            "created_at": time.time(),
        }

    def delete(self, key: str) -> None:
        self._store.pop(key, None)

    def flush_expired(self) -> int:
        now = time.time()
        expired = [k for k, v in self._store.items() if v["expires_at"] < now]
        for k in expired:
            del self._store[k]
        return len(expired)

    @property
    def hit_rate(self) -> float:
        total = self._hits + self._misses
        return self._hits / total if total > 0 else 0.0

    def stats(self) -> dict:
        return {"hits": self._hits, "misses": self._misses, "hit_rate": self.hit_rate, "size": len(self._store)}
