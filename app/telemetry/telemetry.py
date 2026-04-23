import time
import uuid
from typing import Any, Dict
from app.telemetry.glyph_trace import GlyphTrace
from app.telemetry.metrics import MetricsCollector
from app.telemetry.event_bus import EventBus
from app.telemetry.health_monitor import HealthMonitor
from app.core.enums import GlyphStage


class TelemetrySystem:
    def __init__(self):
        self.glyph = GlyphTrace()
        self.metrics = MetricsCollector()
        self.bus = EventBus()
        self.health = HealthMonitor()
        self._request_start: Dict[str, float] = {}

    def start(self, context: Any) -> None:
        ctx = context if isinstance(context, dict) else context.__dict__
        rid = ctx.get("request_id", str(uuid.uuid4()))
        self._request_start[rid] = time.time()
        self.glyph.reset()
        self.glyph.record(GlyphStage.CONTEXT_LOADED, {"request_id": rid, "task_type": ctx.get("task_type")})
        self.metrics.increment("requests_started")
        self.bus.publish("request.started", {"request_id": rid})

    def finish(self, context: Any, reviewed: Dict[str, Any], response: Any) -> None:
        ctx = context if isinstance(context, dict) else context.__dict__
        rid = ctx.get("request_id", "")
        start = self._request_start.pop(rid, time.time())
        duration_ms = (time.time() - start) * 1000

        self.glyph.record(GlyphStage.REFLECTION_VAULT_UPDATED, {
            "request_id": rid,
            "duration_ms": duration_ms,
            "flags": reviewed.get("flags", []),
        })
        self.metrics.increment("requests_completed")
        self.metrics.record_duration("request_duration_ms", duration_ms)

        cache_hit = ctx.get("cache_hit", False)
        if cache_hit:
            self.metrics.increment("cache_hits")
        self.bus.publish("request.completed", {"request_id": rid, "duration_ms": duration_ms})

    def trace(self, stage: str, payload: Dict[str, Any]) -> None:
        self.glyph.record(stage, payload)
        self.bus.publish(f"stage.{stage}", payload)
