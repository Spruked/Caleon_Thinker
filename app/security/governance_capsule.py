import json
import time
from typing import Any, Dict
from app.security.manifest_hash import ManifestHash
from app.security.signature_verify import SignatureVerifier


class GovernanceCapsule:
    """Wraps a decision or policy with integrity hash and signature."""

    def __init__(self, secret: bytes = b"caleon-default-secret-change-me"):
        self.hasher = ManifestHash()
        self.signer = SignatureVerifier(secret)

    def seal(self, payload: Dict[str, Any], metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        capsule = {
            "payload": payload,
            "metadata": metadata or {},
            "sealed_at": time.time(),
        }
        manifest_hash = self.hasher.compute(capsule)
        signature = self.signer.sign(capsule)
        return {
            **capsule,
            "manifest_hash": manifest_hash,
            "signature": signature,
        }

    def verify_seal(self, capsule: Dict[str, Any]) -> bool:
        stored_hash = capsule.get("manifest_hash")
        stored_sig = capsule.get("signature")
        inner = {k: v for k, v in capsule.items() if k not in ("manifest_hash", "signature")}
        hash_ok = self.hasher.verify(inner, stored_hash)
        sig_ok = self.signer.verify(inner, stored_sig)
        return hash_ok and sig_ok
