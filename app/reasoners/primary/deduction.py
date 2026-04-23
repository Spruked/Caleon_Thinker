from typing import Dict, Any, List
from app.reasoners.base import BaseReasoner


class DeductiveReasoner(BaseReasoner):
    name = "deductive"

    def evaluate(self, context: Dict[str, Any]) -> Dict[str, Any]:
        a_priori = context.get("retrieved_memories", {})
        if isinstance(a_priori, list):
            a_priori = {}
        rules = a_priori.get("rules", {})
        principles = a_priori.get("principles", {})
        egf_state = context.get("egf_state", {})
        candidates = egf_state.get("candidates", [])

        claims = []
        risks = []
        notes = []
        confidence = 0.6

        rule_violations = []
        for candidate in candidates:
            for rule_name, rule_fn in rules.items() if isinstance(rules, dict) else []:
                if callable(rule_fn) and not rule_fn(candidate):
                    rule_violations.append(rule_name)
                    risks.append(f"Rule violated: {rule_name}")

        if not rule_violations:
            claims.append(self._claim(
                text="No a priori rule violations detected — deductive path is clear",
                tags=["rule_check", "deductive"],
            ))
            confidence = 0.75
        else:
            confidence = max(0.2, confidence - len(rule_violations) * 0.1)
            notes.append(f"{len(rule_violations)} rule violation(s) detected")

        for p_name, p_value in (principles.items() if isinstance(principles, dict) else []):
            claims.append(self._claim(
                text=f"Principle '{p_name}' applies: {p_value}",
                tags=["principle", "deductive", p_name],
            ))

        viable = egf_state.get("viable_claims", 0)
        if viable == 1:
            notes.append("Single viable claim — deduction converges cleanly")
            confidence = min(1.0, confidence + 0.1)

        return self._result(claims=claims, confidence=confidence, risks=risks, notes=notes)

    def evaluate(self, context: Dict[str, Any]) -> Dict[str, Any]:
        return self._full_evaluate(context)

    def _full_evaluate(self, context: Dict[str, Any]) -> Dict[str, Any]:
        egf_state = context.get("egf_state", {})
        candidates = egf_state.get("candidates", [])
        claims = []
        risks = []
        notes = []
        confidence = 0.6

        for candidate in candidates:
            if candidate.get("coherence_score", 0) >= 0.7 and candidate.get("evidence_mass", 0) >= 0.6:
                claims.append(self._claim(
                    text=f"Deductively sound: {candidate.get('text', '')}",
                    tags=["deductive", "sound"],
                ))
                confidence = min(1.0, confidence + 0.05)
            elif candidate.get("contradiction_drag", 0) > 0.5:
                risks.append(f"Contradiction drag exceeds threshold on: {candidate.get('text', '')[:60]}")

        if not claims:
            notes.append("No deductively sound candidates — holding open")

        return self._result(claims=claims, confidence=confidence, risks=risks, notes=notes)

    def evaluate_top(self, top_candidates: List[Dict[str, Any]], context: Dict[str, Any]) -> Dict[str, Any]:
        sound = [c for c in top_candidates if c.get("coherence_score", 0) >= 0.6]
        if not sound:
            return {"deduction_pick": None, "confidence": 0.3, "note": "no_sound_candidates"}
        best = max(sound, key=lambda c: c.get("coherence_score", 0))
        return {"deduction_pick": best, "confidence": best.get("coherence_score", 0)}
