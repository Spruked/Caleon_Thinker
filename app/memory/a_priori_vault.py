from typing import Any, Callable, Dict


class APrioriVault:
    """Immutable foundational rules, schemas, and principles loaded at startup."""

    def __init__(self):
        self._rules: Dict[str, Callable] = {}
        self._schemas: Dict[str, Any] = {}
        self._principles: Dict[str, str] = {}

    def load_defaults(self) -> None:
        self._principles.update({
            "non_maleficence": "Do not produce outputs that cause harm",
            "honesty": "Do not assert falsehoods knowingly",
            "autonomy": "Respect the user's right to make informed decisions",
            "proportionality": "Response weight should match task weight",
            "epistemic_humility": "Acknowledge uncertainty rather than assert false confidence",
        })
        self._rules.update({
            "no_high_risk_without_tribunal": lambda c: not (c.get("risk_exposure", 0) > 0.8 and not c.get("ethically_permitted", False)),
            "no_zero_confidence_output": lambda c: c.get("softmax_score", 0) > 0.01,
        })

    def add_rule(self, name: str, rule: Callable) -> None:
        self._rules[name] = rule

    def add_principle(self, name: str, description: str) -> None:
        self._principles[name] = description

    def add_schema(self, name: str, schema: Any) -> None:
        self._schemas[name] = schema

    def get_priors(self, context: Any = None) -> Dict[str, Any]:
        return {
            "rules": self._rules,
            "schemas": self._schemas,
            "principles": self._principles,
        }
