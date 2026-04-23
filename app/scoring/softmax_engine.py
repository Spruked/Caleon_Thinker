import math
from typing import Any, Dict, List


class SoftmaxEngine:
    def _softmax(self, logits: List[float]) -> List[float]:
        if not logits:
            return []
        max_logit = max(logits)
        exps = [math.exp(x - max_logit) for x in logits]
        total = sum(exps)
        return [x / total for x in exps]

    def score(
        self,
        egf_state: Dict[str, Any],
        tribunal_results: List[Dict[str, Any]],
        context: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        candidates = tribunal_results if tribunal_results else egf_state.get("candidates", [])
        logits = []

        for candidate in candidates:
            truthfulness = candidate.get("truthfulness", candidate.get("evidence_mass", 0.0))
            accuracy = candidate.get("accuracy", candidate.get("coherence_score", 0.0))
            coherence = candidate.get("coherence_score", 0.0)
            uncertainty_penalty = candidate.get("uncertainty_penalty", candidate.get("uncertainty_radius", 0.0) * 0.5)
            fragility_penalty = candidate.get("fragility_penalty", 0.0)
            ethical_bonus = 0.1 if candidate.get("ethically_permitted", False) else -1.0

            logit = (
                (1.8 * truthfulness)
                + (1.6 * accuracy)
                + (1.1 * coherence)
                + ethical_bonus
                - (1.2 * uncertainty_penalty)
                - (1.0 * fragility_penalty)
            )
            logits.append(logit)

        probs = self._softmax(logits)

        for candidate, prob in zip(candidates, probs):
            candidate["softmax_score"] = prob

        return sorted(candidates, key=lambda x: x.get("softmax_score", 0), reverse=True)
