from typing import Any, Dict, List


class ArticulationVault:
    """Stores reusable phrasing fragments and articulation patterns."""

    def __init__(self):
        self._fragments: Dict[str, str] = {}
        self._load_defaults()

    def _load_defaults(self) -> None:
        self._fragments.update({
            "high_uncertainty_prefix": "Based on available evidence, though with some uncertainty: ",
            "firm_refusal_prefix": "This request falls outside permissible bounds: ",
            "qualified_prefix": "With appropriate qualification: ",
            "confident_prefix": "",
        })

    def get(self, key: str, default: str = "") -> str:
        return self._fragments.get(key, default)

    def add(self, key: str, fragment: str) -> None:
        self._fragments[key] = fragment
