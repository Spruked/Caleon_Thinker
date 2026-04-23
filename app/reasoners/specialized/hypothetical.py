from typing import Dict, Any
from app.reasoners.base import BaseReasoner


class HypotheticalReasoner(BaseReasoner):
    """Explores what-if scenarios and evaluates conditional claims."""
    name = "hypothetical"

    def evaluate(self, context: Dict[str, Any]) -> Dict[str, Any]:
        candidates = context.get("egf_state", {}).get("candidates", [])
        user_input = context.get("user_input", "")

        claims = []
        risks = []

        if "if" in user_input.lower() or "what if" in user_input.lower():
            claims.append(self._claim(
                text="Hypothetical framing detected — conditional evaluation applied",
                tags=["hypothetical", "conditional"],
            ))

        for c in candidates[:3]:
            if c.get("uncertainty_radius", 1.0) > 0.5:
                claims.append(self._claim(
                    text=f"Hypothetical branch: if evidence improves — {c.get('text', '')[:60]}",
                    tags=["hypothetical", "branch"],
                    metadata={"base_uncertainty": c.get("uncertainty_radius")},
                ))

        if not claims:
            risks.append("No hypothetical scenarios generated — input is declarative")

        return self._result(claims=claims, confidence=0.5 if claims else 0.3, risks=risks)
