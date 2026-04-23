from typing import Dict, Any


class TruthfulnessScorer:
    def score(self, candidate: Dict[str, Any], context: Dict[str, Any]) -> float:
        mass = candidate.get("evidence_mass", 0.0)
        drag = candidate.get("contradiction_drag", 0.0)
        uncertainty = candidate.get("uncertainty_radius", 1.0)
        raw = mass * 0.6 - drag * 0.3 - uncertainty * 0.1
        return max(0.0, min(1.0, raw))

    def apply_all(self, candidates: list, context: Dict[str, Any]) -> None:
        for c in candidates:
            c["truthfulness"] = self.score(c, context)
