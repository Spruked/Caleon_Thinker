"""
ChaCha20-Poly1305 wrapper for governance artifact protection.
Requires: pip install cryptography
"""
import os
from typing import Tuple


try:
    from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
    _CRYPTO_AVAILABLE = True
except ImportError:
    _CRYPTO_AVAILABLE = False


class ChaChaWrapper:
    def __init__(self, key: bytes = None):
        if key is None:
            key = os.urandom(32)
        self.key = key
        self._cipher = ChaCha20Poly1305(key) if _CRYPTO_AVAILABLE else None

    def encrypt(self, plaintext: bytes, aad: bytes = b"") -> Tuple[bytes, bytes]:
        if not _CRYPTO_AVAILABLE:
            raise ImportError("cryptography package required: pip install cryptography")
        nonce = os.urandom(12)
        ciphertext = self._cipher.encrypt(nonce, plaintext, aad or None)
        return nonce, ciphertext

    def decrypt(self, nonce: bytes, ciphertext: bytes, aad: bytes = b"") -> bytes:
        if not _CRYPTO_AVAILABLE:
            raise ImportError("cryptography package required: pip install cryptography")
        return self._cipher.decrypt(nonce, ciphertext, aad or None)

    @property
    def available(self) -> bool:
        return _CRYPTO_AVAILABLE
