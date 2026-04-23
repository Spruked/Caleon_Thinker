from typing import Any, Callable, Dict, List, Optional


class RedundancyManager:
    def __init__(self, replicas: int = 3):
        self.replicas = replicas
        self._handlers: List[Callable] = []

    def register(self, handler: Callable) -> None:
        self._handlers.append(handler)

    def execute(self, payload: Any) -> Optional[Any]:
        results = []
        errors = []
        for handler in self._handlers[:self.replicas]:
            try:
                result = handler(payload)
                results.append(result)
            except Exception as e:
                errors.append(str(e))

        if not results:
            return None

        return self._majority_vote(results)

    def _majority_vote(self, results: List[Any]) -> Any:
        if len(results) == 1:
            return results[0]
        counts: Dict[str, int] = {}
        for r in results:
            key = str(r)
            counts[key] = counts.get(key, 0) + 1
        winner = max(counts, key=counts.__getitem__)
        return next(r for r in results if str(r) == winner)
