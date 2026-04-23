from typing import Dict, Any


class UncertaintyPenaltyScorer:
    def score(self, candidate: Dict[str, Any]) -> float:
        radius = candidate.get("uncertainty_radius", 1.0)
        drag = candidate.get("contradiction_drag", 0.0)
        return min(1.0, radius * 0.7 + drag * 0.3)

    def apply_all(self, candidates: list) -> None:
        for c in candidates:
            c["uncertainty_penalty"] = self.score(c)
