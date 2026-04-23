from typing import Any, Dict


class ArticulationAlignment:
    def align(
        self,
        reconciled: Dict[str, Any],
        wisdom: Dict[str, Any],
        context: Dict[str, Any],
    ) -> Dict[str, Any]:
        tone = wisdom.get("tone", "measured")
        urgency = wisdom.get("urgency", "normal")
        confidence = reconciled.get("reconciled_confidence", 0.5)
        humility = wisdom.get("humility_note", "")
        restraint = wisdom.get("restraint_level", "proceed")

        use_templates = confidence >= 0.6 and restraint == "proceed"
        use_llm = not use_templates and context.get("llm_allowed", True)

        return {
            "tone": tone,
            "urgency": urgency,
            "use_templates": use_templates,
            "use_llm": use_llm,
            "include_humility_note": bool(humility),
            "humility_note": humility,
            "style": self._derive_style(tone, urgency, context.get("task_type", "default")),
        }

    def _derive_style(self, tone: str, urgency: str, task_type: str) -> str:
        if tone == "firm":
            return "direct_refusal_with_reason"
        if tone == "exploratory":
            return "qualified_exploration"
        if urgency == "immediate":
            return "concise_direct"
        return "balanced_measured"
