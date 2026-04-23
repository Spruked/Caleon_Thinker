from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class DecisionPacket:
    request_id: str
    candidate_outputs: List[Dict[str, Any]] = field(default_factory=list)
    tribunal_verdicts: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    softmax_scores: Dict[str, float] = field(default_factory=dict)
    primary_closure: Dict[str, Any] = field(default_factory=dict)
    wisdom_adjustments: Dict[str, Any] = field(default_factory=dict)
    harmonized_output: Dict[str, Any] = field(default_factory=dict)
    telemetry: Dict[str, Any] = field(default_factory=dict)
    glyph_trace: List[Dict[str, Any]] = field(default_factory=list)
