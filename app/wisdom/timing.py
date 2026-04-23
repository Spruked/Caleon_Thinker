from typing import Any, Dict


class TimingGuide:
    def assess(self, confidence: float, context: Dict[str, Any]) -> str:
        metadata = context.get("metadata", {})
        if metadata.get("time_sensitive"):
            return "immediate"
        if confidence >= 0.75:
            return "normal"
        if confidence >= 0.5:
            return "considered"
        return "deferred"
