from typing import Dict, Any, List
from app.reasoners.base import BaseReasoner


class AnomalyReasoner(BaseReasoner):
    """Identifies outliers, statistical anomalies, and structurally deviant claims."""
    name = "anomaly"

    def evaluate(self, context: Dict[str, Any]) -> Dict[str, Any]:
        candidates = context.get("egf_state", {}).get("candidates", [])
        claims = []
        risks = []

        if not candidates:
            return self._result(claims=claims, confidence=0.3, risks=["no_candidates"])

        masses = [c.get("evidence_mass", 0) for c in candidates]
        mean = sum(masses) / len(masses)
        std = (sum((m - mean) ** 2 for m in masses) / len(masses)) ** 0.5

        anomalies = [
            c for c, m in zip(candidates, masses)
            if abs(m - mean) > 2 * std
        ]
        for anomaly in anomalies:
            claims.append(self._claim(
                text=f"Anomalous candidate (evidence_mass deviation > 2σ): {anomaly.get('text', '')[:60]}",
                tags=["anomaly", "outlier"],
                metadata={"mass": anomaly.get("evidence_mass"), "mean": mean, "std": std},
            ))
            risks.append(f"Outlier may distort convergence: {anomaly.get('text', '')[:40]}")

        return self._result(claims=claims, confidence=0.7 if not anomalies else 0.5, risks=risks)
