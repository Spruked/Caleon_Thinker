from typing import Dict, Any
from app.reasoners.base import BaseReasoner


class ReflectiveReasoner(BaseReasoner):
    """Examines the system's own reasoning process for bias, drift, or inconsistency."""
    name = "reflective"

    def evaluate(self, context: Dict[str, Any]) -> Dict[str, Any]:
        prior_decisions = context.get("prior_decisions", [])
        egf_state = context.get("egf_state", {})
        convergence = egf_state.get("convergence", {})

        claims = []
        risks = []
        notes = []

        if prior_decisions:
            recent = prior_decisions[-3:]
            consistency = self._check_consistency(recent)
            claims.append(self._claim(
                text=f"Reasoning consistency with recent decisions: {consistency:.0%}",
                tags=["reflective", "consistency"],
                metadata={"consistency_score": consistency},
            ))
            if consistency < 0.5:
                risks.append("Low consistency with prior decisions — possible drift")

        if convergence.get("state") == "converged":
            notes.append("Reflective check: convergence appears earned, not forced")
        elif convergence.get("state") == "uncertain":
            risks.append("Convergence is uncertain — reflective caution advised")

        return self._result(claims=claims, confidence=0.65, risks=risks, notes=notes)

    def _check_consistency(self, decisions: list) -> float:
        if len(decisions) < 2:
            return 1.0
        outcomes = [d.get("harmonized_output", {}).get("final_tone", "") for d in decisions]
        unique = len(set(outcomes))
        return 1.0 - (unique - 1) / max(len(outcomes), 1)
