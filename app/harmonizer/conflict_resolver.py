from typing import Any, Dict, List


class ConflictResolver:
    def identify(
        self,
        closure: Dict[str, Any],
        tribunal_results: List[Dict[str, Any]],
        wisdom: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        conflicts = []

        intuition = closure.get("intuition", {})
        deduction = closure.get("deduction", {})
        induction = closure.get("induction", {})

        if intuition.get("confidence", 0) > 0.7 and deduction.get("confidence", 0) < 0.4:
            conflicts.append({
                "type": "intuition_deduction_gap",
                "description": "Intuition strongly favors but deduction does not confirm",
                "severity": "medium",
            })

        if wisdom.get("escalate"):
            conflicts.append({
                "type": "wisdom_hold",
                "description": "Wisdom engine flagged: restraint level is 'hold'",
                "severity": "high",
            })

        permitted = [r for r in tribunal_results if r.get("ethically_permitted")]
        if tribunal_results and not permitted:
            conflicts.append({
                "type": "tribunal_full_block",
                "description": "No candidates passed tribunal review",
                "severity": "critical",
            })

        return conflicts
