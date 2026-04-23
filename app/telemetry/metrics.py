import time
from typing import Any, Dict, List


class MetricsCollector:
    def __init__(self):
        self._counters: Dict[str, int] = {}
        self._timers: Dict[str, List[float]] = {}
        self._gauges: Dict[str, float] = {}

    def increment(self, key: str, amount: int = 1) -> None:
        self._counters[key] = self._counters.get(key, 0) + amount

    def record_duration(self, key: str, duration_ms: float) -> None:
        self._timers.setdefault(key, []).append(duration_ms)

    def set_gauge(self, key: str, value: float) -> None:
        self._gauges[key] = value

    def avg_duration(self, key: str) -> float:
        values = self._timers.get(key, [])
        return sum(values) / len(values) if values else 0.0

    def snapshot(self) -> Dict[str, Any]:
        return {
            "counters": dict(self._counters),
            "avg_durations": {k: self.avg_duration(k) for k in self._timers},
            "gauges": dict(self._gauges),
        }
