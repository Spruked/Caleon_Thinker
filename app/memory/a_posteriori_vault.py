from typing import Any, Dict, List


class APosterioriVault:
    """Learned experience: cases, patterns, and user preferences accumulated at runtime."""

    def __init__(self, max_cases: int = 500):
        self._cases: List[Dict[str, Any]] = []
        self._patterns: List[str] = []
        self._learned_preferences: Dict[str, Any] = {}
        self._max_cases = max_cases

    def retrieve(self, context: Any = None) -> Dict[str, Any]:
        return {
            "cases": self._cases[:10],
            "patterns": self._patterns[:10],
            "preferences": self._learned_preferences,
        }

    def update(self, decision: Dict[str, Any], outcome: Dict[str, Any]) -> None:
        case = {
            "request_id": decision.get("request_id"),
            "task_type": decision.get("task_type"),
            "user_input": decision.get("user_input", "")[:100],
            "outcome_summary": outcome.get("selected", {}).get("text", "")[:100],
            "tags": decision.get("tags", []),
            "content": outcome,
        }
        self._cases.insert(0, case)
        if len(self._cases) > self._max_cases:
            self._cases = self._cases[:self._max_cases]

        self._extract_patterns(case)

    def _extract_patterns(self, case: Dict[str, Any]) -> None:
        task = case.get("task_type")
        if task and task not in self._patterns:
            self._patterns.append(f"task_type:{task}")
        if len(self._patterns) > 50:
            self._patterns = self._patterns[:50]

    def update_preference(self, key: str, value: Any) -> None:
        self._learned_preferences[key] = value
