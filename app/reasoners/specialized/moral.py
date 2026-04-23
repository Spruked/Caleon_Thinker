from typing import Dict, Any
from app.reasoners.base import BaseReasoner


class MoralReasoner(BaseReasoner):
    """Evaluates actions against harm, fairness, dignity, and duty."""
    name = "moral"

    HARM_SIGNALS = ["harm", "hurt", "damage", "injure", "exploit", "deceive", "manipulate"]
    FAIRNESS_SIGNALS = ["fair", "equal", "just", "equitable", "impartial", "balanced"]

    def evaluate(self, context: Dict[str, Any]) -> Dict[str, Any]:
        user_input = context.get("user_input", "").lower()
        candidates = context.get("egf_state", {}).get("candidates", [])

        claims = []
        risks = []

        harm_detected = any(s in user_input for s in self.HARM_SIGNALS)
        fairness_relevant = any(s in user_input for s in self.FAIRNESS_SIGNALS)

        if harm_detected:
            risks.append("Harm signal detected in input — moral review required")

        if fairness_relevant:
            claims.append(self._claim(
                text="Fairness dimension identified — equal treatment principle applies",
                tags=["moral", "fairness"],
            ))

        for c in candidates:
            if c.get("rights_constraint", 0) > 0.5:
                risks.append(f"Rights constraint violation risk on: {c.get('text', '')[:50]}")

        confidence = 0.6 if not harm_detected else 0.4
        return self._result(claims=claims, confidence=confidence, risks=risks)
