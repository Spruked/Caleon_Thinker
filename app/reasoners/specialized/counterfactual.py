from typing import Dict, Any
from app.reasoners.base import BaseReasoner


class CounterfactualReasoner(BaseReasoner):
    """Evaluates what would have happened under alternative conditions."""
    name = "counterfactual"

    def evaluate(self, context: Dict[str, Any]) -> Dict[str, Any]:
        candidates = context.get("egf_state", {}).get("candidates", [])
        prior_decisions = context.get("prior_decisions", [])

        claims = []
        risks = []

        for c in candidates[:3]:
            inverted_mass = 1.0 - c.get("evidence_mass", 0)
            claims.append(self._claim(
                text=f"Counterfactual: if evidence were absent, candidate weight ≈ {inverted_mass:.2f} — {c.get('text', '')[:50]}",
                tags=["counterfactual"],
                metadata={"counterfactual_weight": inverted_mass},
            ))

        if prior_decisions:
            last = prior_decisions[-1]
            claims.append(self._claim(
                text=f"Counterfactual of last decision: {last.get('user_input', '')[:50]}",
                tags=["counterfactual", "prior"],
            ))

        return self._result(claims=claims, confidence=0.5, risks=risks)
