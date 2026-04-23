from typing import List, Dict, Any
from app.egf.hypothesis_pool import HypothesisPool
from app.egf.evidence_mass import EvidenceMassCalculator
from app.egf.contradiction_drag import ContradictionDragEngine
from app.egf.coherence_tensor import CoherenceTensor
from app.egf.uncertainty_radius import UncertaintyRadius
from app.egf.convergence_engine import ConvergenceEngine
from app.egf.claim_node import ClaimNode


class EpistemologicalGravityField:
    def __init__(self):
        self.pool = HypothesisPool()
        self.mass_calculator = EvidenceMassCalculator()
        self.drag_engine = ContradictionDragEngine()
        self.coherence_tensor = CoherenceTensor()
        self.uncertainty_engine = UncertaintyRadius()
        self.convergence_engine = ConvergenceEngine()

    def initialize(self, context: Dict[str, Any]) -> Dict[str, Any]:
        self.pool.clear()
        for item in context.get("evidence_items", []):
            self.pool.add(
                text=item.get("text", ""),
                source=item.get("source", "context"),
                tags=item.get("tags", []),
                metadata=item,
            )
        return self._compute_state(context)

    def absorb(self, reasoner_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        for result in reasoner_results:
            self.pool.inject_from_reasoner(result)
        return self._compute_state({})

    def _compute_state(self, context: Dict[str, Any]) -> Dict[str, Any]:
        claims = self.pool.all()
        self.mass_calculator.apply_all(claims, context.get("evidence_items", []))
        self.drag_engine.apply_all(claims)
        self.coherence_tensor.apply_all(claims, context)
        self.uncertainty_engine.apply_all(claims)
        convergence = self.convergence_engine.evaluate(claims)

        candidates = [
            {**c.to_dict(), "truthfulness": c.evidence_mass, "accuracy": c.coherence_score}
            for c in claims
        ]

        return {
            "candidates": candidates,
            "convergence": convergence,
            "total_claims": len(claims),
            "viable_claims": len(self.pool.viable()),
        }
