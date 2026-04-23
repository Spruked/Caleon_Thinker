from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class ClaimNode:
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

    @property
    def net_gravity(self) -> float:
        return (self.evidence_mass - self.contradiction_drag) * self.coherence_score

    @property
    def is_viable(self) -> bool:
        return self.net_gravity > 0 and self.uncertainty_radius < 0.9

    def absorb_evidence(self, mass: float) -> None:
        self.evidence_mass = min(1.0, self.evidence_mass + mass)

    def apply_drag(self, drag: float) -> None:
        self.contradiction_drag = min(1.0, self.contradiction_drag + drag)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "claim_id": self.claim_id,
            "text": self.text,
            "source": self.source,
            "evidence_mass": self.evidence_mass,
            "contradiction_drag": self.contradiction_drag,
            "coherence_score": self.coherence_score,
            "uncertainty_radius": self.uncertainty_radius,
            "rights_constraint": self.rights_constraint,
            "risk_exposure": self.risk_exposure,
            "net_gravity": self.net_gravity,
            "is_viable": self.is_viable,
            "tags": self.tags,
            "metadata": self.metadata,
        }
