from typing import Dict, Any
from app.reasoners.base import BaseReasoner


class StatisticalReasoner(BaseReasoner):
    """Applies frequency, distribution, and variance analysis to evidence."""
    name = "statistical"

    def evaluate(self, context: Dict[str, Any]) -> Dict[str, Any]:
        evidence_items = context.get("evidence_items", [])
        candidates = context.get("egf_state", {}).get("candidates", [])

        claims = []
        risks = []

        n = len(evidence_items)
        if n < 5:
            risks.append(f"Small evidence sample (n={n}) — statistical conclusions unreliable")
            return self._result(claims=claims, confidence=0.3, risks=risks,
                                notes=["insufficient_sample_size"])

        weights = [item.get("weight", 1.0) for item in evidence_items]
        mean_weight = sum(weights) / n
        variance = sum((w - mean_weight) ** 2 for w in weights) / n

        claims.append(self._claim(
            text=f"Evidence weight distribution: mean={mean_weight:.2f}, variance={variance:.2f}",
            tags=["statistical", "distribution"],
            metadata={"n": n, "mean": mean_weight, "variance": variance},
        ))

        if variance > 0.3:
            risks.append("High evidence weight variance — distribution is uneven")

        return self._result(claims=claims, confidence=min(0.8, 0.4 + n * 0.02), risks=risks)
