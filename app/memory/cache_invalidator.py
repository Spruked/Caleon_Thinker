import time
from typing import List, Set


class CacheInvalidator:
    """Enforces cache invalidation rules — do not cache blindly."""

    SENSITIVE_TAGS = {"personal_data", "private", "credentials", "financial", "medical", "legal"}
    LOW_CONFIDENCE_THRESHOLD = 0.4

    def should_cache(
        self,
        candidate: dict,
        context: dict,
        confidence: float,
    ) -> bool:
        if not self._passes_sensitivity_check(candidate, context):
            return False
        if not self._passes_confidence_check(confidence):
            return False
        if not self._passes_context_stability_check(context):
            return False
        return True

    def _passes_sensitivity_check(self, candidate: dict, context: dict) -> bool:
        candidate_tags = set(candidate.get("tags", []))
        if candidate_tags & self.SENSITIVE_TAGS:
            user_scope = context.get("user_scope")
            if not user_scope:
                return False
        return True

    def _passes_confidence_check(self, confidence: float) -> bool:
        return confidence >= self.LOW_CONFIDENCE_THRESHOLD

    def _passes_context_stability_check(self, context: dict) -> bool:
        metadata = context.get("metadata", {})
        return not metadata.get("context_volatile", False)

    def invalidation_tags(self, candidate: dict, context: dict) -> List[str]:
        tags = []
        if set(candidate.get("tags", [])) & self.SENSITIVE_TAGS:
            tags.append("sensitive_personal_output")
        if context.get("metadata", {}).get("domain") in {"legal", "financial", "medical"}:
            tags.append("stale_professional_domain")
        return tags
