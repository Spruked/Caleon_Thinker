from typing import Dict, Any


class AccuracyScorer:
    def score(self, candidate: Dict[str, Any], context: Dict[str, Any]) -> float:
        coherence = candidate.get("coherence_score", 0.0)
        tribunal_confidence = candidate.get("tribunal_confidence", 0.5)
        return min(1.0, coherence * 0.6 + tribunal_confidence * 0.4)

    def apply_all(self, candidates: list, context: Dict[str, Any]) -> None:
        for c in candidates:
            c["accuracy"] = self.score(c, context)
