import hashlib
import json
import time
from typing import Any, Dict


class SignedVerdict:
    def sign(self, verdict: Dict[str, Any], node_id: str) -> Dict[str, Any]:
        payload = json.dumps(verdict, sort_keys=True, default=str)
        decision_hash = hashlib.sha256(payload.encode()).hexdigest()
        return {
            **verdict,
            "decision_hash": decision_hash,
            "node_id": node_id,
            "signed_at": time.time(),
        }

    def verify(self, signed: Dict[str, Any]) -> bool:
        stored_hash = signed.pop("decision_hash", None)
        stored_node = signed.pop("node_id", None)
        stored_at = signed.pop("signed_at", None)
        payload = json.dumps(signed, sort_keys=True, default=str)
        recomputed = hashlib.sha256(payload.encode()).hexdigest()
        signed["decision_hash"] = stored_hash
        signed["node_id"] = stored_node
        signed["signed_at"] = stored_at
        return recomputed == stored_hash
