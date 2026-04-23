from typing import List
from app.egf.claim_node import ClaimNode


class UncertaintyRadius:
    def compute(self, claim: ClaimNode) -> float:
        if claim.evidence_mass == 0:
            return 1.0
        base = 1.0 - claim.evidence_mass
        drag_inflation = claim.contradiction_drag * 0.3
        coherence_reduction = claim.coherence_score * 0.2
        return max(0.0, min(1.0, base + drag_inflation - coherence_reduction))

    def apply_all(self, claims: List[ClaimNode]) -> None:
        for claim in claims:
            claim.uncertainty_radius = self.compute(claim)

    def filter_certain(self, claims: List[ClaimNode], threshold: float = 0.5) -> List[ClaimNode]:
        return [c for c in claims if c.uncertainty_radius <= threshold]
