import hashlib
import json
from typing import Any, Dict


class ManifestHash:
    def compute(self, manifest: Dict[str, Any]) -> str:
        serialized = json.dumps(manifest, sort_keys=True, default=str).encode()
        return hashlib.sha256(serialized).hexdigest()

    def verify(self, manifest: Dict[str, Any], expected_hash: str) -> bool:
        return self.compute(manifest) == expected_hash
