from typing import Dict, Any
from app.reasoners.base import BaseReasoner


class TemporalReasoner(BaseReasoner):
    """Considers time dependencies, sequencing, and recency effects on evidence."""
    name = "temporal"

    def evaluate(self, context: Dict[str, Any]) -> Dict[str, Any]:
        evidence_items = context.get("evidence_items", [])
        candidates = context.get("egf_state", {}).get("candidates", [])

        claims = []
        risks = []

        recency_weighted = sorted(
            evidence_items,
            key=lambda e: e.get("recency_factor", 0.5),
            reverse=True,
        )

        if recency_weighted:
            top = recency_weighted[0]
            claims.append(self._claim(
                text=f"Most temporally current evidence: {top.get('content', top.get('text', ''))[:60]}",
                tags=["temporal", "recency"],
                metadata={"recency_factor": top.get("recency_factor", 1.0)},
            ))

        stale = [e for e in evidence_items if e.get("recency_factor", 1.0) < 0.4]
        if stale:
            risks.append(f"{len(stale)} stale evidence item(s) — temporal decay may invalidate conclusions")

        return self._result(claims=claims, confidence=0.55 if recency_weighted else 0.3, risks=risks)
