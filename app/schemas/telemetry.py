from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import time


@dataclass
class TelemetryEvent:
    event_id: str
    event_type: str
    request_id: str
    timestamp: float = field(default_factory=time.time)
    duration_ms: Optional[float] = None
    payload: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)


@dataclass
class HealthSnapshot:
    timestamp: float = field(default_factory=time.time)
    egf_active: bool = True
    cache_hit_rate: float = 0.0
    avg_latency_ms: float = 0.0
    drift_ms: float = 0.0
    active_reasoners: int = 0
    tribunal_pass_rate: float = 0.0
    errors: List[str] = field(default_factory=list)
