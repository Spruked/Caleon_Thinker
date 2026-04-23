from typing import Any, Dict, List
from app.resilience.quorum import Quorum


class ByzantineConsensus:
    """Only use when distributed or multi-node."""

    def __init__(self, quorum_size: int = 4):
        self.quorum_size = quorum_size
        self.quorum = Quorum(required=quorum_size)

    def commit(self, signed_verdicts: List[Dict[str, Any]]) -> Dict[str, Any]:
        grouped: Dict[str, List[Dict[str, Any]]] = {}
        for verdict in signed_verdicts:
            key = verdict.get("decision_hash")
            grouped.setdefault(key, []).append(verdict)

        if not grouped:
            return {"committed": False, "decision_hash": None, "votes": 0, "verdicts": []}

        winner = max(grouped.items(), key=lambda item: len(item[1]), default=(None, []))
        decision_hash, votes = winner

        return {
            "committed": len(votes) >= self.quorum_size,
            "decision_hash": decision_hash,
            "votes": len(votes),
            "verdicts": votes,
            "byzantine_fault_tolerance": (len(signed_verdicts) - 1) // 3,
        }
