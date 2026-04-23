import time
import pytest
from app.memory.cache import ResponseCache
from app.memory.cache_keys import build_cache_key
from app.memory.cache_invalidator import CacheInvalidator


def test_cache_set_and_get():
    cache = ResponseCache()
    cache.set("key1", {"text": "hello"}, ttl_seconds=60)
    result = cache.get("key1")
    assert result == {"text": "hello"}


def test_cache_miss():
    cache = ResponseCache()
    assert cache.get("nonexistent") is None


def test_cache_expiry():
    cache = ResponseCache()
    cache.set("expiring", "value", ttl_seconds=1)
    time.sleep(1.1)
    assert cache.get("expiring") is None


def test_cache_hit_rate():
    cache = ResponseCache()
    cache.set("k1", "v1")
    cache.get("k1")
    cache.get("k1")
    cache.get("missing")
    assert cache.hit_rate == pytest.approx(2 / 3)


def test_build_cache_key_stability():
    k1 = build_cache_key("input", "user1", "1.0", "default", "1.0", "factual")
    k2 = build_cache_key("input", "user1", "1.0", "default", "1.0", "factual")
    assert k1 == k2


def test_build_cache_key_differs_by_scope():
    k1 = build_cache_key("input", "user1", "1.0", "default", "1.0", "factual")
    k2 = build_cache_key("input", "user2", "1.0", "default", "1.0", "factual")
    assert k1 != k2


def test_invalidator_blocks_sensitive():
    inv = CacheInvalidator()
    candidate = {"tags": ["personal_data"]}
    ctx = {}
    assert not inv.should_cache(candidate, ctx, 0.9)


def test_invalidator_blocks_low_confidence():
    inv = CacheInvalidator()
    assert not inv.should_cache({}, {}, 0.2)


def test_invalidator_allows_clean():
    inv = CacheInvalidator()
    assert inv.should_cache({"tags": ["factual"]}, {}, 0.8)
