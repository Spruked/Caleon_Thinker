from typing import List, Dict, Any
from app.egf.claim_node import ClaimNode


class ContradictionDragEngine:
    def __init__(self, drag_threshold: float = 0.3):
        self.drag_threshold = drag_threshold

    def compute_pairwise(self, claim_a: ClaimNode, claim_b: ClaimNode) -> float:
        if claim_a.claim_id == claim_b.claim_id:
            return 0.0
        tag_overlap = set(claim_a.tags) & set(claim_b.tags)
        if not tag_overlap:
            return 0.0
        conflict_score = abs(claim_a.evidence_mass - claim_b.evidence_mass)
        return conflict_score * (len(tag_overlap) / max(len(claim_a.tags), 1))

    def apply_all(self, claims: List[ClaimNode]) -> None:
        for i, claim_a in enumerate(claims):
            drag = 0.0
            for j, claim_b in enumerate(claims):
                if i != j:
                    drag += self.compute_pairwise(claim_a, claim_b)
            claim_a.apply_drag(min(1.0, drag))

    def dominant_claims(self, claims: List[ClaimNode]) -> List[ClaimNode]:
        return [c for c in claims if c.contradiction_drag < self.drag_threshold]
