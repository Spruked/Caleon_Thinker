from typing import List, Dict, Any
from app.egf.claim_node import ClaimNode


class CoherenceTensor:
    def score(self, claim: ClaimNode, context: Dict[str, Any]) -> float:
        intent = context.get("intent", "")
        task_type = context.get("task_type", "")

        tag_relevance = 0.0
        for tag in claim.tags:
            if tag in intent or tag in task_type:
                tag_relevance += 0.15

        source_trust = self._source_trust(claim.source)
        base = (claim.evidence_mass * 0.5) + (source_trust * 0.3) + min(0.2, tag_relevance)
        drag_penalty = claim.contradiction_drag * 0.4
        return max(0.0, min(1.0, base - drag_penalty))

    def _source_trust(self, source: str) -> float:
        trusted = {"a_priori", "tribunal", "deduction", "induction"}
        if source in trusted:
            return 0.9
        if source.startswith("reasoner:"):
            return 0.7
        return 0.5

    def apply_all(self, claims: List[ClaimNode], context: Dict[str, Any]) -> None:
        for claim in claims:
            claim.coherence_score = self.score(claim, context)
