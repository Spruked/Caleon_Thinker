from typing import Any, Dict, List


class SelfCheck:
    def run(self, harmonized: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        corrections = []
        flags = harmonized.get("flags", [])
        selected = harmonized.get("selected", {})
        reconciled = harmonized.get("reconciled", {})

        if "high_uncertainty" in flags and not harmonized.get("wisdom", {}).get("humility_note"):
            corrections.append("increase_humility")

        confidence = reconciled.get("reconciled_confidence", 0.5)
        if confidence < 0.3 and "recursion_uncertainty_flag" not in flags:
            corrections.append("flag_uncertainty")

        if harmonized.get("conflicts"):
            critical = [c for c in harmonized["conflicts"] if c.get("severity") == "critical"]
            if critical:
                corrections.append("critical_conflict_present")

        return {"pass": len(corrections) == 0, "corrections": corrections}
