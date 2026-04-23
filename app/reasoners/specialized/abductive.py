from typing import Dict, Any, List
from app.reasoners.base import BaseReasoner


class AbductiveReasoner(BaseReasoner):
    """Infers the best explanation for incomplete observations."""
    name = "abductive"

    def evaluate(self, context: Dict[str, Any]) -> Dict[str, Any]:
        user_input = context.get("user_input", "")
        evidence_items = context.get("evidence_items", [])
        egf_state = context.get("egf_state", {})
        candidates = egf_state.get("candidates", [])

        claims = []
        risks = []
        notes = []

        explanations = self._generate_explanations(user_input, evidence_items, candidates)
        ranked = self._rank_by_parsimony(explanations)

        for exp in ranked[:3]:
            claims.append(self._claim(
                text=exp["hypothesis"],
                tags=["abductive", "explanation"] + exp.get("tags", []),
                metadata={"parsimony_score": exp["parsimony"], "coverage": exp["coverage"]},
            ))

        confidence = ranked[0]["parsimony"] if ranked else 0.3
        if len(evidence_items) < 2:
            risks.append("thin_evidence_base")
            confidence = max(0.2, confidence - 0.15)
            notes.append("Abductive inference limited by evidence volume")

        unexplained = self._unexplained_observations(evidence_items, ranked)
        if unexplained:
            risks.append(f"{len(unexplained)} unexplained observation(s) remain")

        return self._result(claims=claims, confidence=confidence, risks=risks, notes=notes)

    def _generate_explanations(
        self,
        user_input: str,
        evidence_items: List[Dict[str, Any]],
        candidates: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        explanations = []

        if candidates:
            for candidate in candidates[:5]:
                text = candidate.get("text", "")
                evidence_mass = candidate.get("evidence_mass", 0.0)
                tags = candidate.get("tags", [])
                covered = sum(
                    1 for item in evidence_items
                    if any(t in item.get("tags", []) for t in tags)
                )
                coverage = covered / max(len(evidence_items), 1)
                explanations.append({
                    "hypothesis": f"Best explanation: {text}",
                    "parsimony": evidence_mass * 0.6 + coverage * 0.4,
                    "coverage": coverage,
                    "tags": tags,
                })

        if not explanations:
            explanations.append({
                "hypothesis": f"No structured evidence — inference from input: {user_input[:80]}",
                "parsimony": 0.3,
                "coverage": 0.0,
                "tags": ["speculative"],
            })

        return explanations

    def _rank_by_parsimony(self, explanations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return sorted(explanations, key=lambda e: e["parsimony"], reverse=True)

    def _unexplained_observations(
        self,
        evidence_items: List[Dict[str, Any]],
        ranked: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        explained_tags = set()
        for exp in ranked:
            explained_tags.update(exp.get("tags", []))
        return [
            item for item in evidence_items
            if not set(item.get("tags", [])) & explained_tags
        ]
