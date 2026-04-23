import os
from typing import Optional


class KeyProvider:
    def __init__(self):
        self._keys = {}

    def get(self, key_name: str) -> Optional[bytes]:
        if key_name in self._keys:
            return self._keys[key_name]
        env_val = os.getenv(f"CALEON_KEY_{key_name.upper()}")
        if env_val:
            return env_val.encode()
        return None

    def set(self, key_name: str, key_bytes: bytes) -> None:
        self._keys[key_name] = key_bytes

    def generate(self, key_name: str, length: int = 32) -> bytes:
        key = os.urandom(length)
        self._keys[key_name] = key
        return key
