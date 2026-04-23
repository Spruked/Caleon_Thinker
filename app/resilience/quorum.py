from typing import Any, Dict, List


class Quorum:
    def __init__(self, required: int = 3):
        self.required = required

    def check(self, signed_verdicts: List[Dict[str, Any]]) -> Dict[str, Any]:
        grouped: Dict[str, List[Dict[str, Any]]] = {}
        for verdict in signed_verdicts:
            key = verdict.get("decision_hash", "")
            grouped.setdefault(key, []).append(verdict)

        if not grouped:
            return {"reached": False, "votes": 0, "decision_hash": None}

        winner_hash, winner_votes = max(grouped.items(), key=lambda x: len(x[1]))
        return {
            "reached": len(winner_votes) >= self.required,
            "votes": len(winner_votes),
            "decision_hash": winner_hash,
            "required": self.required,
            "all_hashes": list(grouped.keys()),
        }
