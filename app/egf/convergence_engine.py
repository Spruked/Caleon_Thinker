from typing import List, Dict, Any
from app.egf.claim_node import ClaimNode
from app.core.enums import ConvergenceState


class ConvergenceEngine:
    def __init__(self, convergence_threshold: float = 0.7, min_viable: int = 1):
        self.convergence_threshold = convergence_threshold
        self.min_viable = min_viable

    def evaluate(self, claims: List[ClaimNode]) -> Dict[str, Any]:
        if not claims:
            return {"state": ConvergenceState.DIVERGED, "viable_count": 0, "top_claim": None}

        viable = [c for c in claims if c.is_viable]
        viable.sort(key=lambda c: c.net_gravity, reverse=True)

        if not viable:
            return {"state": ConvergenceState.UNCERTAIN, "viable_count": 0, "top_claim": None}

        top = viable[0]

        if top.net_gravity >= self.convergence_threshold and top.uncertainty_radius < 0.3:
            state = ConvergenceState.CONVERGED
        elif len(viable) <= 2:
            state = ConvergenceState.NARROWING
        else:
            state = ConvergenceState.OPEN

        return {
            "state": state,
            "viable_count": len(viable),
            "top_claim": top.to_dict(),
            "viable_claims": [c.to_dict() for c in viable],
            "all_claims": [c.to_dict() for c in claims],
        }
