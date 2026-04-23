from typing import Any, Dict


class DriftRecheck:
    def check(self, harmonized: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        prior_decisions = context.get("prior_decisions", []) if isinstance(context, dict) else []
        if not prior_decisions:
            return {"drifted": False, "reason": ""}

        current_tone = harmonized.get("final_tone", "measured")
        last_tones = [d.get("harmonized_output", {}).get("final_tone", "measured") for d in prior_decisions[:5]]

        if last_tones and all(t != current_tone for t in last_tones):
            return {"drifted": True, "reason": f"tone_shift:{current_tone}_from_{last_tones[0]}"}

        return {"drifted": False, "reason": ""}
