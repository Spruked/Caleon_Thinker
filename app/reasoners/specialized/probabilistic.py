from typing import Dict, Any
from app.reasoners.base import BaseReasoner


class ProbabilisticReasoner(BaseReasoner):
    """Estimates likelihoods and propagates uncertainty through probability distributions."""
    name = "probabilistic"

    def evaluate(self, context: Dict[str, Any]) -> Dict[str, Any]:
        candidates = context.get("egf_state", {}).get("candidates", [])
        claims = []
        risks = []

        for c in candidates[:3]:
            mass = c.get("evidence_mass", 0)
            drag = c.get("contradiction_drag", 0)
            prob = max(0.0, min(1.0, mass - drag * 0.5))
            claims.append(self._claim(
                text=f"P({c.get('text', '')[:50]}) ≈ {prob:.2f}",
                tags=["probabilistic"],
                metadata={"probability": prob},
            ))

        confidence = max((c.get("evidence_mass", 0) for c in candidates), default=0.3)
        if not candidates:
            risks.append("no_candidates_to_evaluate")

        return self._result(claims=claims, confidence=confidence, risks=risks)
