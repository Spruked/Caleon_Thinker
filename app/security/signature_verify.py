import hashlib
import hmac
from typing import Any, Dict
import json


class SignatureVerifier:
    def __init__(self, secret: bytes):
        self.secret = secret

    def sign(self, payload: Dict[str, Any]) -> str:
        serialized = json.dumps(payload, sort_keys=True, default=str).encode()
        return hmac.new(self.secret, serialized, hashlib.sha256).hexdigest()

    def verify(self, payload: Dict[str, Any], signature: str) -> bool:
        expected = self.sign(payload)
        return hmac.compare_digest(expected, signature)
