from typing import Any, Dict, Optional

PROVERBS = {
    "ethical": "Do not cut what you can untie.",
    "diagnostic": "When you hear hoofbeats, think horses before zebras.",
    "strategic": "The best time to plant a tree was twenty years ago.",
    "factual": "Trust but verify.",
    "adversarial": "Prepare for the storm before it arrives.",
    "reflective": "Know thyself.",
    "default": "Act only on what you can stand behind completely.",
}


class ProverbPrinciples:
    def select(self, context: Dict[str, Any]) -> Optional[str]:
        task_type = context.get("task_type", "default")
        return PROVERBS.get(task_type, PROVERBS["default"])
