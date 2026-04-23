from typing import Dict, Any
from app.reasoners.base import BaseReasoner


class HeuristicReasoner(BaseReasoner):
    """Applies fast, rule-of-thumb reasoning for speed and practical clarity."""
    name = "heuristic"

    HEURISTICS = [
        ("high_certainty_fast_path", lambda c: c.get("evidence_mass", 0) > 0.8 and c.get("uncertainty_radius", 1) < 0.2),
        ("avoid_high_drag", lambda c: c.get("contradiction_drag", 0) < 0.3),
        ("prefer_low_risk", lambda c: c.get("risk_exposure", 0) < 0.4),
    ]

    def evaluate(self, context: Dict[str, Any]) -> Dict[str, Any]:
        candidates = context.get("egf_state", {}).get("candidates", [])
        claims = []
        risks = []

        for name, rule in self.HEURISTICS:
            passing = [c for c in candidates if rule(c)]
            if passing:
                claims.append(self._claim(
                    text=f"Heuristic '{name}' selects {len(passing)} candidate(s)",
                    tags=["heuristic", name],
                    metadata={"count": len(passing)},
                ))

        if not claims:
            risks.append("No heuristic shortcuts apply — full reasoning required")

        return self._result(claims=claims, confidence=0.6 if claims else 0.3, risks=risks)
