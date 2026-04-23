from typing import Any, Dict


class SignalReconciler:
    def reconcile(
        self,
        closure: Dict[str, Any],
        wisdom: Dict[str, Any],
        egf_state: Dict[str, Any],
    ) -> Dict[str, Any]:
        intuition_conf = closure.get("intuition", {}).get("confidence", 0.5)
        deduction_conf = closure.get("deduction", {}).get("confidence", 0.5)
        induction_conf = closure.get("induction", {}).get("confidence", 0.5)

        primary_signal = (intuition_conf + deduction_conf + induction_conf) / 3.0
        wisdom_modifier = 1.0 if wisdom.get("restraint_level") == "proceed" else 0.8

        return {
            "primary_signal": primary_signal,
            "wisdom_modifier": wisdom_modifier,
            "reconciled_confidence": primary_signal * wisdom_modifier,
            "convergence_state": egf_state.get("convergence", {}).get("state", "unknown"),
        }
