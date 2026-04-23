from typing import Dict, Any
from app.core.enums import TribunalFrame


class LockeEngine:
    """Rights frame: consent, authorization, property, and protection from undue intrusion."""
    frame_name = TribunalFrame.LOCKE

    CONSENT_REQUIRED_SIGNALS = ["personal data", "private", "identity", "credentials", "access", "password"]
    INTRUSION_SIGNALS = ["without permission", "unauthorized", "bypass", "override access", "steal"]

    def review(self, candidate: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        text = candidate.get("text", "").lower()
        user_input = context.get("user_input", "").lower()
        rights_constraint = candidate.get("rights_constraint", 0.0)
        flags = []
        confidence = 0.85

        for signal in self.INTRUSION_SIGNALS:
            if signal in text or signal in user_input:
                flags.append(f"unauthorized_access_signal:{signal}")
                confidence = max(0.05, confidence - 0.4)

        if rights_constraint > 0.5:
            flags.append(f"rights_constraint_high:{rights_constraint:.2f}")
            confidence = max(0.1, confidence - rights_constraint * 0.3)

        consent_needed = any(s in text or s in user_input for s in self.CONSENT_REQUIRED_SIGNALS)
        consent_present = context.get("metadata", {}).get("consent_verified", False)
        if consent_needed and not consent_present:
            flags.append("consent_required_but_unverified")
            confidence = max(0.15, confidence - 0.25)

        allow = len(flags) == 0
        reason = (
            "Rights and consent requirements satisfied" if allow
            else f"Rights concern: {'; '.join(flags)}"
        )

        return {
            "frame": self.frame_name,
            "allow": allow,
            "confidence": confidence,
            "reason": reason,
            "flags": flags,
        }
