from typing import Dict, Any
from app.core.enums import TribunalFrame


class SpinozaEngine:
    """Coherence frame: does this follow from the nature of things? Is it causally consistent?"""
    frame_name = TribunalFrame.SPINOZA

    def review(self, candidate: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        coherence_score = candidate.get("coherence_score", 0.0)
        contradiction_drag = candidate.get("contradiction_drag", 0.0)
        flags = []
        confidence = 0.75

        if coherence_score < 0.3:
            flags.append(f"low_coherence:{coherence_score:.2f}")
            confidence -= 0.25

        if contradiction_drag > 0.5:
            flags.append(f"high_contradiction_drag:{contradiction_drag:.2f}")
            confidence -= 0.2

        causal_fit = self._evaluate_causal_fit(candidate, context)
        if not causal_fit:
            flags.append("poor_causal_fit")
            confidence -= 0.1

        allow = coherence_score >= 0.3 and contradiction_drag <= 0.6
        reason = (
            "Causally coherent and self-consistent" if allow
            else f"Coherence failure: score={coherence_score:.2f}, drag={contradiction_drag:.2f}"
        )

        return {
            "frame": self.frame_name,
            "allow": allow,
            "confidence": max(0.1, confidence),
            "reason": reason,
            "flags": flags,
        }

    def _evaluate_causal_fit(self, candidate: Dict[str, Any], context: Dict[str, Any]) -> bool:
        tags = set(candidate.get("tags", []))
        evidence_tags = set()
        for item in context.get("evidence_items", []):
            evidence_tags.update(item.get("tags", []))
        return bool(tags & evidence_tags) or not evidence_tags
