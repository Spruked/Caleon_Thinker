from typing import Dict, Any


class FragilityPenaltyScorer:
    def score(self, candidate: Dict[str, Any]) -> float:
        risk = candidate.get("risk_exposure", 0.0)
        uncertainty = candidate.get("uncertainty_radius", 1.0)
        tribunal_flags = len(candidate.get("tribunal_flags", []))
        flag_penalty = min(0.3, tribunal_flags * 0.05)
        return min(1.0, risk * 0.5 + uncertainty * 0.3 + flag_penalty)

    def apply_all(self, candidates: list) -> None:
        for c in candidates:
            c["fragility_penalty"] = self.score(c)
