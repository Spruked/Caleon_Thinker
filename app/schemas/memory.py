from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import time


@dataclass
class MemoryRecord:
    record_id: str
    vault_type: str
    content: Dict[str, Any]
    created_at: float = field(default_factory=time.time)
    expires_at: Optional[float] = None
    tags: List[str] = field(default_factory=list)
    source_request_id: Optional[str] = None

    @property
    def is_expired(self) -> bool:
        if self.expires_at is None:
            return False
        return time.time() > self.expires_at


@dataclass
class RetrievalBundle:
    request_id: str
    a_priori: Dict[str, Any] = field(default_factory=dict)
    a_posteriori: Dict[str, Any] = field(default_factory=dict)
    reflection: List[Dict[str, Any]] = field(default_factory=list)
    cache_hit: bool = False
