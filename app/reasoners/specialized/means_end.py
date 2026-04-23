from typing import Dict, Any
from app.reasoners.base import BaseReasoner


class MeansEndReasoner(BaseReasoner):
    """Maps available means to desired ends and evaluates instrumental pathways."""
    name = "means_end"

    def evaluate(self, context: Dict[str, Any]) -> Dict[str, Any]:
        metadata = context.get("metadata", {})
        goals = metadata.get("goals", [])
        available_means = metadata.get("available_means", [])
        candidates = context.get("egf_state", {}).get("candidates", [])

        claims = []
        risks = []

        if not goals:
            risks.append("No goals specified — means-end analysis is blind")
            return self._result(claims=claims, confidence=0.2, risks=risks)

        for goal in goals[:3]:
            matched = [c for c in candidates if goal.lower() in c.get("text", "").lower()]
            if matched:
                claims.append(self._claim(
                    text=f"Instrumental path to '{goal}': {matched[0].get('text', '')[:60]}",
                    tags=["means_end", "instrumental"],
                    metadata={"goal": goal},
                ))
            else:
                risks.append(f"No candidate supports goal: '{goal}'")

        return self._result(claims=claims, confidence=0.6 if claims else 0.3, risks=risks)
