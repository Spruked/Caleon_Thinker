from typing import Dict, Any, List
from app.egf.claim_node import ClaimNode


class EvidenceMassCalculator:
    def __init__(self, base_weight: float = 1.0, recency_decay: float = 0.95):
        self.base_weight = base_weight
        self.recency_decay = recency_decay

    def compute(self, evidence_items: List[Dict[str, Any]], claim: ClaimNode) -> float:
        total_mass = 0.0
        for item in evidence_items:
            if item.get("claim_id") != claim.claim_id and item.get("claim_id") is not None:
                continue
            weight = item.get("weight", self.base_weight)
            reliability = item.get("reliability", 1.0)
            recency = item.get("recency_factor", 1.0)
            total_mass += weight * reliability * recency
        return min(1.0, total_mass)

    def apply_all(self, claims: List[ClaimNode], evidence_items: List[Dict[str, Any]]) -> None:
        for claim in claims:
            mass = self.compute(evidence_items, claim)
            claim.absorb_evidence(mass)
