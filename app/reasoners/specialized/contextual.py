from typing import Dict, Any
from app.reasoners.base import BaseReasoner


class ContextualReasoner(BaseReasoner):
    """Situates claims within their surrounding context, norms, and constraints."""
    name = "contextual"

    def evaluate(self, context: Dict[str, Any]) -> Dict[str, Any]:
        metadata = context.get("metadata", {})
        task_type = context.get("task_type", "unknown")
        user_scope = context.get("user_scope")
        candidates = context.get("egf_state", {}).get("candidates", [])

        claims = []
        risks = []

        claims.append(self._claim(
            text=f"Context established: task_type={task_type}, scope={user_scope or 'global'}",
            tags=["contextual", task_type],
        ))

        context_mismatch = [
            c for c in candidates
            if task_type not in c.get("tags", []) and task_type != "unknown"
        ]
        if context_mismatch:
            risks.append(f"{len(context_mismatch)} candidate(s) lack task_type tag '{task_type}'")

        return self._result(claims=claims, confidence=0.6, risks=risks)
