import time
from typing import Any, Dict, List
from app.core.enums import GlyphStage


class GlyphTrace:
    """Meaning-level trace — records what the system understood at each cognitive stage."""

    def __init__(self):
        self.events: List[Dict[str, Any]] = []
        self._start_time = time.time()

    def record(self, stage: str, payload: Dict[str, Any]) -> None:
        self.events.append({
            "stage": stage,
            "payload": payload,
            "elapsed_ms": (time.time() - self._start_time) * 1000,
            "timestamp": time.time(),
        })

    def export(self) -> List[Dict[str, Any]]:
        return list(self.events)

    def summary(self) -> Dict[str, Any]:
        stages = [e["stage"] for e in self.events]
        return {
            "total_stages": len(stages),
            "stages_completed": stages,
            "total_elapsed_ms": (time.time() - self._start_time) * 1000,
        }

    def reset(self) -> None:
        self.events.clear()
        self._start_time = time.time()
