import time
from typing import Any, Dict, List
from app.schemas.telemetry import HealthSnapshot


class HealthMonitor:
    def __init__(self):
        self._errors: List[str] = []
        self._last_snapshot: HealthSnapshot = None

    def record_error(self, error: str) -> None:
        self._errors.append(error)
        if len(self._errors) > 100:
            self._errors = self._errors[-100:]

    def snapshot(
        self,
        cache_hit_rate: float = 0.0,
        avg_latency_ms: float = 0.0,
        drift_ms: float = 0.0,
        active_reasoners: int = 0,
        tribunal_pass_rate: float = 0.0,
    ) -> HealthSnapshot:
        snap = HealthSnapshot(
            cache_hit_rate=cache_hit_rate,
            avg_latency_ms=avg_latency_ms,
            drift_ms=drift_ms,
            active_reasoners=active_reasoners,
            tribunal_pass_rate=tribunal_pass_rate,
            errors=list(self._errors[-5:]),
        )
        self._last_snapshot = snap
        return snap

    def is_healthy(self) -> bool:
        if not self._last_snapshot:
            return True
        return (
            self._last_snapshot.avg_latency_ms < 5000
            and self._last_snapshot.drift_ms < 500
            and len(self._errors) < 10
        )
