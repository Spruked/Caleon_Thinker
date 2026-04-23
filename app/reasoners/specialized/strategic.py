from typing import Dict, Any
from app.reasoners.base import BaseReasoner


class StrategicReasoner(BaseReasoner):
    """Evaluates options against long-term goals, tradeoffs, and resource constraints."""
    name = "strategic"

    def evaluate(self, context: Dict[str, Any]) -> Dict[str, Any]:
        candidates = context.get("egf_state", {}).get("candidates", [])
        metadata = context.get("metadata", {})
        goals = metadata.get("goals", [])
        constraints = metadata.get("constraints", [])

        claims = []
        risks = []
        notes = []

        viable = [c for c in candidates if c.get("is_viable", False)]
        if not viable:
            viable = candidates[:3]

        for c in viable[:3]:
            risk = c.get("risk_exposure", 0)
            mass = c.get("evidence_mass", 0)
            strategic_score = mass * 0.6 - risk * 0.4
            claims.append(self._claim(
                text=f"Strategic option (score={strategic_score:.2f}): {c.get('text', '')[:60]}",
                tags=["strategic"],
                metadata={"strategic_score": strategic_score, "risk": risk},
            ))

        if constraints:
            notes.append(f"Evaluated against {len(constraints)} constraint(s)")
        if not goals:
            risks.append("No explicit goals supplied — strategic evaluation is generic")

        return self._result(claims=claims, confidence=0.6 if viable else 0.3, risks=risks, notes=notes)
