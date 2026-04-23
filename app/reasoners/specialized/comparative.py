from typing import Dict, Any, List
from app.reasoners.base import BaseReasoner


class ComparativeReasoner(BaseReasoner):
    """Ranks options against each other on shared dimensions."""
    name = "comparative"

    def evaluate(self, context: Dict[str, Any]) -> Dict[str, Any]:
        candidates = context.get("egf_state", {}).get("candidates", [])
        claims = []
        risks = []

        if len(candidates) < 2:
            risks.append("Fewer than 2 candidates — comparative analysis requires alternatives")
            return self._result(claims=claims, confidence=0.3, risks=risks)

        sorted_by_mass = sorted(candidates, key=lambda c: c.get("evidence_mass", 0), reverse=True)
        top, second = sorted_by_mass[0], sorted_by_mass[1]
        delta = top.get("evidence_mass", 0) - second.get("evidence_mass", 0)

        claims.append(self._claim(
            text=f"Top candidate leads by evidence_mass Δ={delta:.2f}: {top.get('text', '')[:50]}",
            tags=["comparative", "ranking"],
            metadata={"delta": delta, "candidate_count": len(candidates)},
        ))

        if delta < 0.1:
            risks.append("Near-equal candidates — ranking is fragile under perturbation")

        return self._result(claims=claims, confidence=0.6 + delta * 0.2, risks=risks)
