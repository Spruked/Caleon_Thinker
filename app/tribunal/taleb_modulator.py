from typing import Dict, Any
from app.core.enums import TribunalFrame


class TalebModulator:
    """Antifragility modulator: penalizes fragility, rewards robustness under stress."""
    frame_name = TribunalFrame.TALEB

    def review(self, candidate: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        fragility_penalty = candidate.get("fragility_penalty", 0.0)
        uncertainty = candidate.get("uncertainty_radius", 1.0)
        risk_exposure = candidate.get("risk_exposure", 0.0)
        flags = []

        fragility_score = self._compute_fragility(fragility_penalty, uncertainty, risk_exposure)
        is_fragile = fragility_score > 0.5
        is_antifragile = fragility_score < 0.2

        if is_fragile:
            flags.append(f"fragile_candidate:{fragility_score:.2f}")
        if is_antifragile:
            flags.append("antifragile")

        confidence = max(0.1, 0.9 - fragility_score * 0.6)
        reason = (
            f"Antifragile — gains under volatility" if is_antifragile
            else f"Fragility score={fragility_score:.2f}" if is_fragile
            else f"Acceptable fragility level ({fragility_score:.2f})"
        )

        return {
            "frame": self.frame_name,
            "allow": True,
            "confidence": confidence,
            "reason": reason,
            "flags": flags,
            "fragility_score": fragility_score,
            "is_antifragile": is_antifragile,
        }

    def _compute_fragility(self, penalty: float, uncertainty: float, risk: float) -> float:
        return min(1.0, (penalty * 0.4) + (uncertainty * 0.3) + (risk * 0.3))
