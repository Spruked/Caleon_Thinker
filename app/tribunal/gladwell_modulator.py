from typing import Dict, Any
from app.core.enums import TribunalFrame


class GladwellModulator:
    """Tipping point modulator: amplifies thin-slice signals and social tipping dynamics."""
    frame_name = TribunalFrame.GLADWELL

    TIPPING_THRESHOLD = 0.6

    def review(self, candidate: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        evidence_mass = candidate.get("evidence_mass", 0.0)
        coherence = candidate.get("coherence_score", 0.0)
        flags = []

        thin_slice_score = self._thin_slice(candidate, context)
        tipping = thin_slice_score >= self.TIPPING_THRESHOLD

        if tipping:
            flags.append("tipping_point_signal")

        confidence = 0.5 + thin_slice_score * 0.4
        reason = (
            f"Tipping point signal detected (thin_slice={thin_slice_score:.2f})" if tipping
            else f"Below tipping threshold (thin_slice={thin_slice_score:.2f})"
        )

        return {
            "frame": self.frame_name,
            "allow": True,
            "confidence": confidence,
            "reason": reason,
            "flags": flags,
            "thin_slice_score": thin_slice_score,
            "tipping": tipping,
        }

    def _thin_slice(self, candidate: Dict[str, Any], context: Dict[str, Any]) -> float:
        mass = candidate.get("evidence_mass", 0)
        coherence = candidate.get("coherence_score", 0)
        prior_count = len(context.get("prior_decisions", []))
        recency_signal = max((
            item.get("recency_factor", 0)
            for item in context.get("evidence_items", [])
        ), default=0.5)
        return min(1.0, (mass * 0.4) + (coherence * 0.3) + (recency_signal * 0.2) + (min(prior_count, 5) * 0.02))
