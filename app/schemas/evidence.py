from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class EvidenceSchema:
    evidence_id: str
    claim_id: str
    source: str
    content: str
    weight: float = 1.0
    reliability: float = 1.0
    recency_factor: float = 1.0
    contradiction_target: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def effective_mass(self) -> float:
        return self.weight * self.reliability * self.recency_factor
