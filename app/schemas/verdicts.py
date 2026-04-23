from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class VerdictSchema:
    verdict_id: str
    frame: str
    allow: bool
    confidence: float = 0.0
    reason: str = ""
    flags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class FusedVerdictSchema:
    request_id: str
    verdicts: Dict[str, VerdictSchema] = field(default_factory=dict)
    permitted: bool = False
    consensus_confidence: float = 0.0
    dissenting_frames: List[str] = field(default_factory=list)
    flags: List[str] = field(default_factory=list)
