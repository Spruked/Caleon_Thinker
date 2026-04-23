from typing import Dict, Any, List
from app.reasoners.base import BaseReasoner


class IntuitiveReasoner(BaseReasoner):
    name = "intuitive"

    def evaluate(self, context: Dict[str, Any]) -> Dict[str, Any]:
        user_input = context.get("user_input", "")
        intent = context.get("intent", "")
        prior_decisions = context.get("prior_decisions", [])
        egf_state = context.get("egf_state", {})
        candidates = egf_state.get("candidates", [])

        claims = []
        confidence = 0.5
        risks = []
        notes = []

        if prior_decisions:
            similar = self._find_similar(user_input, prior_decisions)
            if similar:
                claims.append(self._claim(
                    text=f"Prior decision pattern suggests: {similar.get('harmonized_output', {}).get('selected', {}).get('text', 'similar approach')}",
                    tags=["prior_pattern", "intuitive"],
                    metadata={"source_decision_id": similar.get("request_id")},
                ))
                confidence += 0.15

        if candidates:
            top = max(candidates, key=lambda c: c.get("evidence_mass", 0), default=None)
            if top:
                claims.append(self._claim(
                    text=f"Strongest evidenced claim: {top.get('text', '')}",
                    tags=["evidence_driven", "intuitive"],
                ))
                confidence = min(1.0, confidence + top.get("evidence_mass", 0) * 0.2)

        convergence = egf_state.get("convergence", {})
        if convergence.get("state") == "converged":
            notes.append("EGF converged — intuition reinforces top candidate")
            confidence = min(1.0, confidence + 0.1)
        elif convergence.get("state") == "diverged":
            risks.append("EGF diverged — intuition withheld")
            confidence = max(0.1, confidence - 0.2)

        return self._result(claims=claims, confidence=confidence, risks=risks, notes=notes)

    def _find_similar(self, user_input: str, prior_decisions: List[Dict[str, Any]]) -> Dict[str, Any]:
        input_words = set(user_input.lower().split())
        best = None
        best_overlap = 0
        for decision in prior_decisions:
            prev_input = decision.get("user_input", "")
            overlap = len(input_words & set(prev_input.lower().split()))
            if overlap > best_overlap:
                best_overlap = overlap
                best = decision
        return best if best_overlap >= 2 else None

    def evaluate_top(self, top_candidates: List[Dict[str, Any]], context: Dict[str, Any]) -> Dict[str, Any]:
        if not top_candidates:
            return {"intuition_pick": None, "confidence": 0.0}
        best = max(top_candidates, key=lambda c: c.get("softmax_score", 0))
        return {"intuition_pick": best, "confidence": best.get("softmax_score", 0)}
