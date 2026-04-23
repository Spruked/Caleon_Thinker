from typing import Any, Dict, List


class ToneGuide:
    def select(self, flags: List[str], uncertainty: float, context: Dict[str, Any]) -> str:
        task_type = context.get("task_type", "")
        if any("violation" in f for f in flags):
            return "firm"
        if uncertainty > 0.6:
            return "exploratory"
        if task_type == "ethical":
            return "measured"
        if task_type == "strategic":
            return "analytical"
        if task_type == "diagnostic":
            return "precise"
        return "measured"
