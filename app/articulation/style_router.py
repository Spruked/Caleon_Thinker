from typing import Any, Dict


STYLE_PROFILES = {
    "direct_refusal_with_reason": {"prefix": "firm_refusal_prefix", "verbose": False},
    "qualified_exploration": {"prefix": "qualified_prefix", "verbose": True},
    "concise_direct": {"prefix": "confident_prefix", "verbose": False},
    "balanced_measured": {"prefix": "qualified_prefix", "verbose": True},
}


class StyleRouter:
    def route(self, style: str, tone: str) -> Dict[str, Any]:
        profile = STYLE_PROFILES.get(style, STYLE_PROFILES["balanced_measured"])
        return {**profile, "tone": tone, "style": style}
