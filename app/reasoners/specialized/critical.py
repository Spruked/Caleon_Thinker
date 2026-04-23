from typing import Dict, Any, List
from app.reasoners.base import BaseReasoner


class CriticalReasoner(BaseReasoner):
    """Interrogates assumptions, identifies weak reasoning, and flags epistemic gaps."""
    name = "critical"

    def evaluate(self, context: Dict[str, Any]) -> Dict[str, Any]:
        egf_state = context.get("egf_state", {})
        candidates = egf_state.get("candidates", [])
        convergence = egf_state.get("convergence", {})

        claims = []
        risks = []
        notes = []
        confidence = 0.7

        weak = self._identify_weak_candidates(candidates)
        for w in weak:
            risks.append(f"Weak candidate: {w['reason']} — {w['text'][:60]}")
            confidence = max(0.2, confidence - 0.05)

        assumption_flags = self._surface_assumptions(candidates, context)
        for flag in assumption_flags:
            claims.append(self._claim(
                text=f"Assumption surfaced: {flag}",
                tags=["critical", "assumption"],
            ))

        gaps = self._identify_gaps(candidates, context)
        for gap in gaps:
            risks.append(f"Epistemic gap: {gap}")

        if convergence.get("state") == "converged" and len(weak) > 0:
            notes.append("Convergence may be premature — weak candidates remain")
            confidence = max(0.3, confidence - 0.1)

        if not candidates:
            risks.append("No candidates to critically evaluate")
            confidence = 0.2

        return self._result(claims=claims, confidence=confidence, risks=risks, notes=notes)

    def _identify_weak_candidates(self, candidates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        weak = []
        for c in candidates:
            reasons = []
            if c.get("evidence_mass", 0) < 0.2:
                reasons.append("low_evidence_mass")
            if c.get("contradiction_drag", 0) > 0.6:
                reasons.append("high_contradiction_drag")
            if c.get("uncertainty_radius", 1.0) > 0.8:
                reasons.append("high_uncertainty")
            if reasons:
                weak.append({
                    "text": c.get("text", ""),
                    "reason": ", ".join(reasons),
                })
        return weak

    def _surface_assumptions(
        self,
        candidates: List[Dict[str, Any]],
        context: Dict[str, Any],
    ) -> List[str]:
        assumptions = []
        intent = context.get("intent", "")

        if not context.get("evidence_items"):
            assumptions.append("No external evidence supplied — input is assumed credible")

        if len(candidates) == 1:
            assumptions.append("Single candidate — no competitive evaluation possible")

        if context.get("llm_allowed") and not context.get("cache_hit"):
            assumptions.append("LLM articulation assumed available and reliable")

        return assumptions

    def _identify_gaps(
        self,
        candidates: List[Dict[str, Any]],
        context: Dict[str, Any],
    ) -> List[str]:
        gaps = []
        if not context.get("retrieved_memories"):
            gaps.append("No memory retrieval — historical context absent")
        if not context.get("prior_decisions"):
            gaps.append("No prior decision history — pattern detection unavailable")
        all_tags = set()
        for c in candidates:
            all_tags.update(c.get("tags", []))
        if not all_tags:
            gaps.append("No semantic tags on candidates — coherence tensor blind")
        return gaps
