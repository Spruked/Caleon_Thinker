from typing import Any, Dict, List
from app.harmonizer.signal_reconciler import SignalReconciler
from app.harmonizer.conflict_resolver import ConflictResolver
from app.harmonizer.articulation_alignment import ArticulationAlignment


class Harmonizer:
    def __init__(self):
        self.reconciler = SignalReconciler()
        self.resolver = ConflictResolver()
        self.alignment = ArticulationAlignment()

    def resolve(
        self,
        egf_state: Dict[str, Any],
        tribunal_results: List[Dict[str, Any]],
        closure: Dict[str, Any],
        wisdom: Dict[str, Any],
        context: Dict[str, Any],
    ) -> Dict[str, Any]:
        top_candidates = closure.get("top_candidates", [])
        best = top_candidates[0] if top_candidates else {}

        reconciled = self.reconciler.reconcile(closure, wisdom, egf_state)
        conflicts = self.resolver.identify(closure, tribunal_results, wisdom)
        articulation_hint = self.alignment.align(reconciled, wisdom, context)

        return {
            "selected": best,
            "closure": closure,
            "wisdom": wisdom,
            "reconciled": reconciled,
            "conflicts": conflicts,
            "articulation_hint": articulation_hint,
            "final_tone": wisdom.get("tone", "measured"),
            "final_urgency": wisdom.get("urgency", "normal"),
            "flags": self._collect_flags(best, tribunal_results),
        }

    def _collect_flags(self, best: Dict[str, Any], tribunal_results: List[Dict[str, Any]]) -> List[str]:
        flags = list(best.get("tribunal_flags", []))
        if best.get("uncertainty_penalty", 0) > 0.4:
            flags.append("high_uncertainty")
        if best.get("fragility_penalty", 0) > 0.4:
            flags.append("fragility_warning")
        return flags
