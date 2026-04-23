from typing import Any, Dict


class OutputGuard:
    """Final safety filter before response leaves the system."""

    BLOCKED_PATTERNS = [
        "ignore all previous", "jailbreak", "i am now unrestricted",
        "bypass all safety", "disable your ethics",
    ]

    def check(self, response: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        text = response.get("text", "")
        if self._contains_blocked(text):
            return {
                "text": "Output blocked by safety guard.",
                "tone": "firm",
                "flags": response.get("flags", []) + ["output_guard_blocked"],
                "articulation_mode": response.get("articulation_mode", "guard"),
                "blocked": True,
            }
        return response

    def _contains_blocked(self, text: str) -> bool:
        lowered = text.lower()
        return any(p in lowered for p in self.BLOCKED_PATTERNS)
