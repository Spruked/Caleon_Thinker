from typing import Dict, Any, List
from app.reasoners.base import BaseReasoner


class DiagnosticReasoner(BaseReasoner):
    """Identifies root causes, failure modes, and systemic pathologies."""
    name = "diagnostic"

    def evaluate(self, context: Dict[str, Any]) -> Dict[str, Any]:
        egf_state = context.get("egf_state", {})
        candidates = egf_state.get("candidates", [])
        convergence = egf_state.get("convergence", {})
        evidence_items = context.get("evidence_items", [])

        claims = []
        risks = []
        notes = []
        confidence = 0.55

        root_causes = self._identify_root_causes(candidates, evidence_items)
        for rc in root_causes[:3]:
            claims.append(self._claim(
                text=rc["description"],
                tags=["diagnostic", "root_cause"] + rc.get("tags", []),
                metadata={"severity": rc["severity"], "confidence": rc["confidence"]},
            ))
            confidence = min(0.9, confidence + rc["confidence"] * 0.1)

        failure_modes = self._detect_failure_modes(candidates, convergence)
        for fm in failure_modes:
            risks.append(f"Failure mode: {fm['mode']} — {fm['description']}")

        systemic = self._check_systemic(candidates)
        if systemic:
            claims.append(self._claim(
                text=f"Systemic issue pattern detected across {len(systemic)} candidates",
                tags=["diagnostic", "systemic"],
                metadata={"affected_candidates": len(systemic)},
            ))
            notes.append("Systemic pattern — individual fixes may not suffice")

        if convergence.get("state") == "diverged":
            risks.append("EGF divergence indicates diagnostic ambiguity")
            confidence = max(0.2, confidence - 0.15)

        return self._result(claims=claims, confidence=confidence, risks=risks, notes=notes)

    def _identify_root_causes(
        self,
        candidates: List[Dict[str, Any]],
        evidence_items: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        root_causes = []
        for candidate in candidates:
            drag = candidate.get("contradiction_drag", 0)
            mass = candidate.get("evidence_mass", 0)
            uncertainty = candidate.get("uncertainty_radius", 1.0)

            if drag > 0.5 and mass < 0.4:
                root_causes.append({
                    "description": f"Root cause candidate: high contradiction with weak evidence — {candidate.get('text', '')[:60]}",
                    "severity": "high" if drag > 0.7 else "medium",
                    "confidence": drag * 0.6,
                    "tags": ["contradiction_driven"],
                })
            elif uncertainty > 0.7:
                root_causes.append({
                    "description": f"Uncertainty concentration at: {candidate.get('text', '')[:60]}",
                    "severity": "medium",
                    "confidence": (1 - uncertainty) * 0.5,
                    "tags": ["uncertainty_driven"],
                })

        return sorted(root_causes, key=lambda rc: rc["confidence"], reverse=True)

    def _detect_failure_modes(
        self,
        candidates: List[Dict[str, Any]],
        convergence: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        modes = []
        if convergence.get("state") == "uncertain":
            modes.append({"mode": "indeterminate", "description": "EGF cannot resolve — multiple equally-weighted candidates"})
        high_risk = [c for c in candidates if c.get("risk_exposure", 0) > 0.6]
        for c in high_risk:
            modes.append({"mode": "high_risk_exposure", "description": c.get("text", "")[:60]})
        return modes

    def _check_systemic(self, candidates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        common_tag_threshold = max(len(candidates) // 2, 1)
        tag_counts: Dict[str, int] = {}
        for c in candidates:
            for tag in c.get("tags", []):
                tag_counts[tag] = tag_counts.get(tag, 0) + 1
        systemic_tags = {t for t, count in tag_counts.items() if count >= common_tag_threshold}
        return [c for c in candidates if set(c.get("tags", [])) & systemic_tags]
