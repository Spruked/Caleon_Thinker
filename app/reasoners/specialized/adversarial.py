from typing import Dict, Any, List
from app.reasoners.base import BaseReasoner


class AdversarialReasoner(BaseReasoner):
    """Stress-tests conclusions by simulating opposition, exploits, and worst-case inputs."""
    name = "adversarial"

    def evaluate(self, context: Dict[str, Any]) -> Dict[str, Any]:
        egf_state = context.get("egf_state", {})
        candidates = egf_state.get("candidates", [])
        user_input = context.get("user_input", "")
        task_type = context.get("task_type", "")

        claims = []
        risks = []
        notes = []
        confidence = 0.8

        attacks = self._generate_attacks(candidates, user_input, task_type)
        survivors = []
        for candidate, attack_results in zip(candidates, attacks):
            survived = all(ar["survived"] for ar in attack_results)
            if survived:
                survivors.append(candidate)
                claims.append(self._claim(
                    text=f"Adversarially robust: {candidate.get('text', '')[:60]}",
                    tags=["adversarial", "robust"],
                    metadata={"attacks_survived": len(attack_results)},
                ))
            else:
                failed = [ar["attack_type"] for ar in attack_results if not ar["survived"]]
                risks.append(f"Candidate failed: {', '.join(failed)} — {candidate.get('text', '')[:50]}")

        if not survivors:
            risks.append("No candidate survived adversarial stress — all are fragile")
            notes.append("Recommend higher uncertainty radius on all outputs")
            confidence = 0.3

        injection = self._check_prompt_injection(user_input)
        if injection:
            risks.append("Possible prompt injection or manipulation pattern detected")
            confidence = max(0.2, confidence - 0.3)
            notes.append("Input flagged for adversarial content — applying increased scrutiny")

        manipulation = self._check_social_manipulation(user_input, context)
        if manipulation:
            risks.append(f"Social manipulation signal: {manipulation}")
            confidence = max(0.3, confidence - 0.2)

        confidence = min(0.9, 0.4 + len(survivors) / max(len(candidates), 1) * 0.5)

        return self._result(claims=claims, confidence=confidence, risks=risks, notes=notes)

    def _generate_attacks(
        self,
        candidates: List[Dict[str, Any]],
        user_input: str,
        task_type: str,
    ) -> List[List[Dict[str, Any]]]:
        attack_results = []
        for candidate in candidates:
            results = [
                self._negation_attack(candidate),
                self._edge_case_attack(candidate),
                self._stake_escalation_attack(candidate),
            ]
            attack_results.append(results)
        return attack_results

    def _negation_attack(self, candidate: Dict[str, Any]) -> Dict[str, Any]:
        mass = candidate.get("evidence_mass", 0)
        survived = mass >= 0.4
        return {
            "attack_type": "negation",
            "survived": survived,
            "note": "negation_resisted" if survived else "negation_collapsed_candidate",
        }

    def _edge_case_attack(self, candidate: Dict[str, Any]) -> Dict[str, Any]:
        uncertainty = candidate.get("uncertainty_radius", 1.0)
        survived = uncertainty < 0.7
        return {
            "attack_type": "edge_case",
            "survived": survived,
            "note": "edge_case_stable" if survived else "edge_case_exposed_uncertainty",
        }

    def _stake_escalation_attack(self, candidate: Dict[str, Any]) -> Dict[str, Any]:
        risk_exposure = candidate.get("risk_exposure", 0)
        survived = risk_exposure < 0.6
        return {
            "attack_type": "stake_escalation",
            "survived": survived,
            "note": "stake_stable" if survived else "high_risk_under_escalation",
        }

    def _check_prompt_injection(self, user_input: str) -> bool:
        injection_signals = [
            "ignore previous", "ignore all", "disregard", "forget your",
            "you are now", "act as", "pretend you", "jailbreak",
            "do anything now", "dan mode",
        ]
        lowered = user_input.lower()
        return any(signal in lowered for signal in injection_signals)

    def _check_social_manipulation(self, user_input: str, context: Dict[str, Any]) -> str:
        manipulation_signals = {
            "urgency_pressure": ["immediately", "right now", "no time", "emergency", "must respond"],
            "authority_spoofing": ["i am your creator", "anthropic says", "admin override"],
            "flattery_bypass": ["you're so smart", "as the most intelligent", "only you can"],
        }
        lowered = user_input.lower()
        for signal_type, patterns in manipulation_signals.items():
            if any(p in lowered for p in patterns):
                return signal_type
        return ""
