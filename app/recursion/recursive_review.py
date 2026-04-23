from typing import Any, Dict
from app.recursion.self_check import SelfCheck
from app.recursion.drift_recheck import DriftRecheck
from app.recursion.outcome_reflection import OutcomeReflection


class RecursiveReview:
    def __init__(self, max_iterations: int = 3):
        self.self_check = SelfCheck()
        self.drift_recheck = DriftRecheck()
        self.outcome_reflection = OutcomeReflection()
        self.max_iterations = max_iterations

    def recheck(self, harmonized: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        result = harmonized

        for i in range(self.max_iterations):
            check = self.self_check.run(result, context)
            if check["pass"]:
                break
            result = self._apply_correction(result, check)

        drift = self.drift_recheck.check(result, context)
        if drift["drifted"]:
            result["flags"] = result.get("flags", []) + [f"drift_detected:{drift['reason']}"]

        result["recursion_reflection"] = self.outcome_reflection.reflect(result, context)
        return result

    def _apply_correction(self, harmonized: Dict[str, Any], check: Dict[str, Any]) -> Dict[str, Any]:
        corrections = check.get("corrections", [])
        for correction in corrections:
            if correction == "increase_humility":
                harmonized.setdefault("wisdom", {})["humility_note"] = "Correction applied — increased epistemic humility"
            elif correction == "flag_uncertainty":
                harmonized["flags"] = harmonized.get("flags", []) + ["recursion_uncertainty_flag"]
        return harmonized
