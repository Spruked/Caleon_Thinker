from typing import Dict, Any, List
from app.core.enums import TribunalFrame


class KantEngine:
    """Deontological frame: duty, universal law, and non-instrumentalization of persons."""
    frame_name = TribunalFrame.KANT

    PROHIBITED_PATTERNS = [
        "deceive", "manipulate", "coerce", "exploit", "harm deliberately",
        "use person as means", "violate dignity",
    ]

    def review(self, candidate: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        text = candidate.get("text", "").lower()
        user_input = context.get("user_input", "").lower()
        flags = []
        reason_parts = []
        confidence = 0.8

        for pattern in self.PROHIBITED_PATTERNS:
            if pattern in text or pattern in user_input:
                flags.append(f"deontological_violation:{pattern}")
                confidence = max(0.1, confidence - 0.3)

        universalizable = self._universalizability_test(candidate, context)
        if not universalizable["passes"]:
            flags.append("fails_universalizability")
            reason_parts.append(universalizable["reason"])
            confidence = max(0.15, confidence - 0.25)

        allow = len(flags) == 0
        reason = "Duty-consistent and universalizable" if allow else "; ".join(reason_parts) or "Kantian constraint violated"

        return {
            "frame": self.frame_name,
            "allow": allow,
            "confidence": confidence,
            "reason": reason,
            "flags": flags,
        }

    def _universalizability_test(self, candidate: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        text = candidate.get("text", "").lower()
        risk = candidate.get("risk_exposure", 0)

        if risk > 0.7:
            return {"passes": False, "reason": "High risk — not universalizable at scale"}
        if "only for me" in text or "exception" in text:
            return {"passes": False, "reason": "Special-case framing violates universal law"}
        return {"passes": True, "reason": ""}
