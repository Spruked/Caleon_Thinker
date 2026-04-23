from typing import Dict, Any, List
from app.reasoners.base import BaseReasoner


class CausalReasoner(BaseReasoner):
    """Maps cause-effect chains and identifies proximate vs. distal causes."""
    name = "causal"

    def evaluate(self, context: Dict[str, Any]) -> Dict[str, Any]:
        user_input = context.get("user_input", "")
        evidence_items = context.get("evidence_items", [])
        egf_state = context.get("egf_state", {})
        candidates = egf_state.get("candidates", [])

        claims = []
        risks = []
        notes = []

        causal_chains = self._extract_chains(candidates, evidence_items)
        for chain in causal_chains[:3]:
            claims.append(self._claim(
                text=chain["narrative"],
                tags=["causal", chain["type"]],
                metadata={"chain_length": chain["length"], "strength": chain["strength"]},
            ))

        confidence = 0.5
        if causal_chains:
            avg_strength = sum(c["strength"] for c in causal_chains) / len(causal_chains)
            confidence = min(0.9, 0.4 + avg_strength * 0.5)

        confounders = self._detect_confounders(candidates)
        for confounder in confounders:
            risks.append(f"Potential confounder: {confounder}")
            confidence = max(0.2, confidence - 0.05)

        circular = self._detect_circular(causal_chains)
        if circular:
            risks.append("Circular causation detected — chain integrity uncertain")
            notes.append("Requires external anchoring to break circular dependency")

        return self._result(claims=claims, confidence=confidence, risks=risks, notes=notes)

    def _extract_chains(
        self,
        candidates: List[Dict[str, Any]],
        evidence_items: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        chains = []
        for i, candidate in enumerate(candidates[:4]):
            text = candidate.get("text", "")
            mass = candidate.get("evidence_mass", 0.0)
            drag = candidate.get("contradiction_drag", 0.0)

            cause_tags = [t for t in candidate.get("tags", []) if "cause" in t or "trigger" in t]
            effect_tags = [t for t in candidate.get("tags", []) if "effect" in t or "result" in t]

            if mass > 0.3:
                chain_type = "proximate" if i == 0 else "distal"
                chains.append({
                    "narrative": f"{'Proximate' if chain_type == 'proximate' else 'Distal'} cause: {text[:80]}",
                    "type": chain_type,
                    "length": len(cause_tags) + len(effect_tags) + 1,
                    "strength": max(0.0, mass - drag * 0.5),
                })

        if not chains:
            chains.append({
                "narrative": "Causal structure unclear — insufficient evidence mass",
                "type": "unknown",
                "length": 0,
                "strength": 0.2,
            })

        return chains

    def _detect_confounders(self, candidates: List[Dict[str, Any]]) -> List[str]:
        confounders = []
        tag_counts: Dict[str, int] = {}
        for c in candidates:
            for tag in c.get("tags", []):
                tag_counts[tag] = tag_counts.get(tag, 0) + 1
        for tag, count in tag_counts.items():
            if count > 2:
                confounders.append(tag)
        return confounders

    def _detect_circular(self, chains: List[Dict[str, Any]]) -> bool:
        texts = [c["narrative"] for c in chains]
        return any(t in texts[i + 1:] for i, t in enumerate(texts))
