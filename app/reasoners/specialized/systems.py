from typing import Dict, Any
from app.reasoners.base import BaseReasoner


class SystemsReasoner(BaseReasoner):
    """Evaluates feedback loops, emergent properties, and interdependencies."""
    name = "systems"

    def evaluate(self, context: Dict[str, Any]) -> Dict[str, Any]:
        candidates = context.get("egf_state", {}).get("candidates", [])
        metadata = context.get("metadata", {})
        system_map = metadata.get("system_map", {})

        claims = []
        risks = []

        interdependent = []
        for c in candidates:
            deps = c.get("metadata", {}).get("dependencies", [])
            if deps:
                interdependent.append((c, deps))

        if interdependent:
            claims.append(self._claim(
                text=f"{len(interdependent)} candidate(s) have system dependencies",
                tags=["systems", "interdependency"],
                metadata={"count": len(interdependent)},
            ))
            risks.append("Interdependent candidates — isolated evaluation may miss systemic effects")
        else:
            claims.append(self._claim(
                text="No system dependencies detected — candidates are locally isolated",
                tags=["systems", "isolated"],
            ))

        return self._result(claims=claims, confidence=0.55, risks=risks)
