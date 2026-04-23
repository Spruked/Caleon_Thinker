from typing import Any, Dict, List
from app.reasoners.primary.intuition import IntuitiveReasoner
from app.reasoners.primary.deduction import DeductiveReasoner
from app.reasoners.primary.induction import InductiveReasoner


class PrimaryClosure:
    """Three primary reasoners stabilize the 24 specialized outputs into a closure."""

    def __init__(
        self,
        intuition: IntuitiveReasoner,
        deduction: DeductiveReasoner,
        induction: InductiveReasoner,
    ):
        self.intuition = intuition
        self.deduction = deduction
        self.induction = induction

    def run(self, candidates: List[Dict[str, Any]], context: Dict[str, Any]) -> Dict[str, Any]:
        top = candidates[:5]

        return {
            "intuition": self.intuition.evaluate_top(top, context),
            "deduction": self.deduction.evaluate_top(top, context),
            "induction": self.induction.evaluate_top(top, context),
            "top_candidates": top,
        }
