from typing import Dict, Any


class CoherenceScorer:
    def score(self, candidate: Dict[str, Any], context: Dict[str, Any]) -> float:
        return candidate.get("coherence_score", 0.0)

    def apply_all(self, candidates: list, context: Dict[str, Any]) -> None:
        pass
