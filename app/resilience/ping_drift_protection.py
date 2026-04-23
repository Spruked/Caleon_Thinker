import time
from typing import Dict


class PingDriftProtection:
    def __init__(self, max_skew_ms: float = 250.0):
        self.max_skew_ms = max_skew_ms
        self.last_ping: float = None
        self._drift_history = []

    def ping(self) -> Dict[str, float]:
        now = time.time() * 1000.0
        drift = 0.0 if self.last_ping is None else now - self.last_ping
        self.last_ping = now
        self._drift_history.append(drift)
        if len(self._drift_history) > 100:
            self._drift_history = self._drift_history[-100:]
        return {
            "drift_ms": drift,
            "healthy": drift <= self.max_skew_ms if drift else True,
            "avg_drift_ms": sum(self._drift_history) / len(self._drift_history),
        }

    def is_healthy(self) -> bool:
        if not self._drift_history:
            return True
        return self._drift_history[-1] <= self.max_skew_ms
