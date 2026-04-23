from typing import Dict, Any
from app.reasoners.base import BaseReasoner


class PredictiveReasoner(BaseReasoner):
    """Projects likely outcomes based on current evidence trajectories."""
    name = "predictive"

    def evaluate(self, context: Dict[str, Any]) -> Dict[str, Any]:
        candidates = context.get("egf_state", {}).get("candidates", [])
        prior_decisions = context.get("prior_decisions", [])

        claims = []
        risks = []

        if not candidates:
            risks.append("no_candidates_for_projection")
            return self._result(claims=claims, confidence=0.2, risks=risks)

        top = max(candidates, key=lambda c: c.get("evidence_mass", 0))
        mass = top.get("evidence_mass", 0)
        projected_confidence = min(0.9, mass + 0.1 * len(prior_decisions))

        claims.append(self._claim(
            text=f"Projected outcome: {top.get('text', '')[:60]} (confidence≈{projected_confidence:.2f})",
            tags=["predictive", "projection"],
            metadata={"projected_confidence": projected_confidence},
        ))

        if mass < 0.4:
            risks.append("Low evidence mass — projection is speculative")

        return self._result(claims=claims, confidence=projected_confidence, risks=risks)
