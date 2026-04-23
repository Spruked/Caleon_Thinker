from typing import Dict, Any
from app.core.enums import TribunalFrame


class HumeEngine:
    """Empiricist frame: is this grounded in evidence? Is it a fact or a value leap?"""
    frame_name = TribunalFrame.HUME

    def review(self, candidate: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        evidence_mass = candidate.get("evidence_mass", 0.0)
        uncertainty = candidate.get("uncertainty_radius", 1.0)
        flags = []
        confidence = 0.75

        if evidence_mass < 0.2:
            flags.append("insufficient_empirical_grounding")
            confidence -= 0.3

        if uncertainty > 0.7:
            flags.append("high_uncertainty_under_empirical_review")
            confidence -= 0.2

        is_fact_value_leap = self._detect_is_ought(candidate, context)
        if is_fact_value_leap:
            flags.append("is_ought_violation")
            confidence -= 0.15

        allow = evidence_mass >= 0.25 and uncertainty <= 0.75
        reason = (
            "Empirically grounded" if allow
            else f"Insufficient evidence (mass={evidence_mass:.2f}, uncertainty={uncertainty:.2f})"
        )

        return {
            "frame": self.frame_name,
            "allow": allow,
            "confidence": max(0.1, confidence),
            "reason": reason,
            "flags": flags,
        }

    def _detect_is_ought(self, candidate: Dict[str, Any], context: Dict[str, Any]) -> bool:
        text = candidate.get("text", "").lower()
        ought_signals = ["should", "must", "ought to", "is required to", "we need to"]
        fact_signals = ["because", "data shows", "evidence indicates", "studies confirm"]
        has_ought = any(s in text for s in ought_signals)
        has_grounding = any(s in text for s in fact_signals)
        return has_ought and not has_grounding
