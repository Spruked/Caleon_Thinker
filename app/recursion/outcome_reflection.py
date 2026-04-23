from typing import Any, Dict


class OutcomeReflection:
    def reflect(self, harmonized: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        selected = harmonized.get("selected", {})
        flags = harmonized.get("flags", [])
        conflicts = harmonized.get("conflicts", [])
        reconciled = harmonized.get("reconciled", {})

        quality = "high"
        if len(flags) > 2:
            quality = "medium"
        if len(flags) > 4 or conflicts:
            quality = "low"
        if any(c.get("severity") == "critical" for c in conflicts):
            quality = "critical_concern"

        return {
            "output_quality": quality,
            "flag_count": len(flags),
            "conflict_count": len(conflicts),
            "confidence": reconciled.get("reconciled_confidence", 0.0),
            "notes": [f"flags:{','.join(flags[:3])}"] if flags else [],
        }
