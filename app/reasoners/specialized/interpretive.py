from typing import Dict, Any
from app.reasoners.base import BaseReasoner


class InterpretiveReasoner(BaseReasoner):
    """Resolves ambiguity in language, intent, and framing."""
    name = "interpretive"

    def evaluate(self, context: Dict[str, Any]) -> Dict[str, Any]:
        user_input = context.get("user_input", "")
        intent = context.get("intent", "")

        claims = []
        risks = []

        ambiguity_signals = ["could mean", "unclear", "ambiguous", "it depends", "either", "or maybe"]
        is_ambiguous = any(s in user_input.lower() for s in ambiguity_signals)

        if is_ambiguous:
            claims.append(self._claim(
                text=f"Ambiguous input detected — interpretation anchored to intent: '{intent}'",
                tags=["interpretive", "ambiguity"],
                metadata={"intent": intent},
            ))
            risks.append("Interpretation may not match user expectation — confidence reduced")
            confidence = 0.5
        else:
            claims.append(self._claim(
                text=f"Input is unambiguous — direct interpretation applied",
                tags=["interpretive", "clear"],
            ))
            confidence = 0.75

        return self._result(claims=claims, confidence=confidence, risks=risks)
