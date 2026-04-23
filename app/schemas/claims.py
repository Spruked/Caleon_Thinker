from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ClaimSchema:
    claim_id: str
    text: str
    source: str
    evidence_mass: float = 0.0
    contradiction_drag: float = 0.0
    coherence_score: float = 0.0
    uncertainty_radius: float = 1.0
    rights_constraint: float = 0.0
    risk_exposure: float = 0.0
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    parent_claim_id: Optional[str] = None
    truthfulness: float = 0.0
    accuracy: float = 0.0
    ethically_permitted: bool = False
    softmax_score: float = 0.0
    uncertainty_penalty: float = 0.0
    fragility_penalty: float = 0.0
