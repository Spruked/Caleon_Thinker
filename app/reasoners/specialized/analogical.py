from typing import Dict, Any, List
from app.reasoners.base import BaseReasoner


class AnalogicalReasoner(BaseReasoner):
    """Maps structural similarities between domains to transfer conclusions."""
    name = "analogical"

    def evaluate(self, context: Dict[str, Any]) -> Dict[str, Any]:
        user_input = context.get("user_input", "")
        prior_decisions = context.get("prior_decisions", [])
        retrieved = context.get("retrieved_memories", {})
        cases = retrieved.get("cases", []) if isinstance(retrieved, dict) else []
        egf_state = context.get("egf_state", {})
        candidates = egf_state.get("candidates", [])

        claims = []
        risks = []
        notes = []

        analogies = self._find_analogies(user_input, cases, prior_decisions, candidates)
        for analogy in analogies[:3]:
            claims.append(self._claim(
                text=analogy["mapping"],
                tags=["analogical", "transfer"] + analogy.get("tags", []),
                metadata={
                    "similarity_score": analogy["similarity"],
                    "source_domain": analogy["source"],
                },
            ))

        confidence = max((a["similarity"] for a in analogies), default=0.3)
        if not analogies:
            notes.append("No structural analogies found — analogical path deferred")
            confidence = 0.25

        false_analogies = self._check_false_mappings(analogies, candidates)
        for fa in false_analogies:
            risks.append(f"Structural mismatch risk: {fa}")

        return self._result(claims=claims, confidence=confidence, risks=risks, notes=notes)

    def _find_analogies(
        self,
        user_input: str,
        cases: List[Dict[str, Any]],
        prior_decisions: List[Dict[str, Any]],
        candidates: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        analogies = []
        input_words = set(user_input.lower().split())

        for case in cases[:10]:
            case_words = set(str(case.get("content", "")).lower().split())
            overlap = len(input_words & case_words)
            if overlap >= 2:
                similarity = overlap / max(len(input_words), 1)
                analogies.append({
                    "mapping": f"Analogous to prior case: {str(case.get('content', ''))[:60]}",
                    "similarity": min(0.9, similarity),
                    "source": "case_memory",
                    "tags": case.get("tags", []),
                })

        for decision in prior_decisions[:5]:
            prev_input = decision.get("user_input", "")
            prev_words = set(prev_input.lower().split())
            overlap = len(input_words & prev_words)
            if overlap >= 3:
                similarity = overlap / max(len(input_words), 1)
                analogies.append({
                    "mapping": f"Structurally similar to: {prev_input[:60]}",
                    "similarity": min(0.85, similarity),
                    "source": "prior_decision",
                    "tags": ["decision_transfer"],
                })

        return sorted(analogies, key=lambda a: a["similarity"], reverse=True)

    def _check_false_mappings(
        self,
        analogies: List[Dict[str, Any]],
        candidates: List[Dict[str, Any]],
    ) -> List[str]:
        false_maps = []
        for analogy in analogies:
            if analogy["similarity"] < 0.4:
                false_maps.append(f"Weak similarity ({analogy['similarity']:.2f}): {analogy['mapping'][:40]}")
        return false_maps
