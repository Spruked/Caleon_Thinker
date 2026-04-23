from typing import Dict, Any, List
from app.reasoners.base import BaseReasoner


class InductiveReasoner(BaseReasoner):
    name = "inductive"

    def evaluate(self, context: Dict[str, Any]) -> Dict[str, Any]:
        a_posteriori = context.get("retrieved_memories", {})
        if isinstance(a_posteriori, list):
            a_posteriori = {}
        cases = a_posteriori.get("cases", [])
        patterns = a_posteriori.get("patterns", [])
        egf_state = context.get("egf_state", {})
        candidates = egf_state.get("candidates", [])

        claims = []
        risks = []
        notes = []
        confidence = 0.5

        if patterns:
            for pattern in patterns[:3]:
                claims.append(self._claim(
                    text=f"Observed pattern supports: {pattern}",
                    tags=["pattern", "inductive"],
                ))
            confidence = min(1.0, confidence + len(patterns) * 0.05)

        if cases:
            supporting = self._matching_cases(cases, candidates)
            if supporting:
                claims.append(self._claim(
                    text=f"Inductive support from {len(supporting)} prior case(s)",
                    tags=["cases", "inductive"],
                    metadata={"case_ids": [c.get("record_id") for c in supporting]},
                ))
                confidence = min(1.0, confidence + min(0.2, len(supporting) * 0.04))
            else:
                notes.append("No matching prior cases — induction deferred")
                risks.append("low_inductive_support")

        if len(cases) < 3:
            notes.append("Thin case history — inductive confidence limited")
            confidence = max(0.2, confidence - 0.1)

        return self._result(claims=claims, confidence=confidence, risks=risks, notes=notes)

    def _matching_cases(self, cases: List[Dict[str, Any]], candidates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        candidate_tags = set()
        for c in candidates:
            candidate_tags.update(c.get("tags", []))
        return [
            case for case in cases
            if set(case.get("tags", [])) & candidate_tags
        ]

    def evaluate_top(self, top_candidates: List[Dict[str, Any]], context: Dict[str, Any]) -> Dict[str, Any]:
        cases = context.get("retrieved_memories", {})
        if isinstance(cases, list):
            cases = {}
        case_count = len(cases.get("cases", []))
        confidence = min(0.9, 0.4 + case_count * 0.05)
        best = top_candidates[0] if top_candidates else None
        return {"induction_pick": best, "confidence": confidence}
