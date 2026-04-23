from typing import Dict, Any
from app.reasoners.base import BaseReasoner


class SpatialReasoner(BaseReasoner):
    """Evaluates spatial relationships, scope boundaries, and domain localization."""
    name = "spatial"

    def evaluate(self, context: Dict[str, Any]) -> Dict[str, Any]:
        metadata = context.get("metadata", {})
        scope = metadata.get("scope", "global")
        candidates = context.get("egf_state", {}).get("candidates", [])

        claims = []
        risks = []

        claims.append(self._claim(
            text=f"Evaluation scoped to domain: {scope}",
            tags=["spatial", "scope"],
        ))

        out_of_scope = [
            c for c in candidates
            if scope != "global" and scope not in c.get("tags", [])
        ]
        if out_of_scope:
            risks.append(f"{len(out_of_scope)} candidate(s) may be out of scope for domain '{scope}'")

        return self._result(claims=claims, confidence=0.5, risks=risks)
