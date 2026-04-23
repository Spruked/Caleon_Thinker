from typing import Dict, Any, List
from app.reasoners.base import BaseReasoner


class PatternReasoner(BaseReasoner):
    """Detects recurring structures across evidence, candidates, and prior decisions."""
    name = "pattern"

    def evaluate(self, context: Dict[str, Any]) -> Dict[str, Any]:
        candidates = context.get("egf_state", {}).get("candidates", [])
        prior = context.get("prior_decisions", [])

        claims = []
        risks = []

        tag_freq: Dict[str, int] = {}
        for c in candidates:
            for tag in c.get("tags", []):
                tag_freq[tag] = tag_freq.get(tag, 0) + 1

        dominant = [(t, n) for t, n in tag_freq.items() if n >= 2]
        for tag, count in sorted(dominant, key=lambda x: -x[1])[:3]:
            claims.append(self._claim(
                text=f"Recurring pattern tag '{tag}' appears in {count} candidates",
                tags=["pattern", tag],
                metadata={"frequency": count},
            ))

        if not dominant:
            risks.append("No recurring patterns detected — candidates are structurally diverse")

        return self._result(claims=claims, confidence=0.55 if dominant else 0.3, risks=risks)
