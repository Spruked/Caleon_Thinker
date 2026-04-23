from typing import Any, Dict, List


class ReflectionVault:
    """Prior decisions available for recursive self-review and pattern correction."""

    def __init__(self, max_decisions: int = 200):
        self._prior_decisions: List[Dict[str, Any]] = []
        self._max_decisions = max_decisions

    def fetch_related(self, context: Any = None) -> List[Dict[str, Any]]:
        if context is None:
            return self._prior_decisions[:10]

        user_input = ""
        if hasattr(context, "user_input"):
            user_input = context.user_input
        elif isinstance(context, dict):
            user_input = context.get("user_input", "")

        if not user_input:
            return self._prior_decisions[:10]

        input_words = set(user_input.lower().split())
        scored = []
        for decision in self._prior_decisions:
            prev = decision.get("user_input", "").lower()
            overlap = len(input_words & set(prev.split()))
            if overlap > 0:
                scored.append((overlap, decision))

        scored.sort(key=lambda x: -x[0])
        return [d for _, d in scored[:10]] or self._prior_decisions[:5]

    def record(self, decision_packet: Any) -> None:
        if hasattr(decision_packet, "__dict__"):
            record = decision_packet.__dict__
        elif isinstance(decision_packet, dict):
            record = decision_packet
        else:
            record = {"raw": str(decision_packet)}

        self._prior_decisions.insert(0, record)
        if len(self._prior_decisions) > self._max_decisions:
            self._prior_decisions = self._prior_decisions[:self._max_decisions]
