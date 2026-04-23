from typing import Any, Dict, List, Optional
import time


class PriorDecisionIndex:
    """Fast lookup index for prior decisions by request_id and task_type."""

    def __init__(self):
        self._by_id: Dict[str, Dict[str, Any]] = {}
        self._by_task_type: Dict[str, List[str]] = {}
        self._recent: List[str] = []
        self._max_recent = 100

    def index(self, decision: Dict[str, Any]) -> None:
        rid = decision.get("request_id")
        if not rid:
            return
        self._by_id[rid] = decision
        task_type = decision.get("task_type", "unknown")
        self._by_task_type.setdefault(task_type, []).append(rid)
        self._recent.insert(0, rid)
        if len(self._recent) > self._max_recent:
            self._recent = self._recent[:self._max_recent]

    def get(self, request_id: str) -> Optional[Dict[str, Any]]:
        return self._by_id.get(request_id)

    def get_by_task_type(self, task_type: str, limit: int = 10) -> List[Dict[str, Any]]:
        ids = self._by_task_type.get(task_type, [])[-limit:]
        return [self._by_id[rid] for rid in reversed(ids) if rid in self._by_id]

    def recent(self, limit: int = 10) -> List[Dict[str, Any]]:
        return [self._by_id[rid] for rid in self._recent[:limit] if rid in self._by_id]
