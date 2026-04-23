from typing import List, Dict, Any, Optional
from app.egf.claim_node import ClaimNode
import uuid


class HypothesisPool:
    def __init__(self):
        self._pool: List[ClaimNode] = []

    def add(self, text: str, source: str, tags: List[str] = None, metadata: Dict[str, Any] = None) -> ClaimNode:
        node = ClaimNode(
            claim_id=str(uuid.uuid4()),
            text=text,
            source=source,
            tags=tags or [],
            metadata=metadata or {},
        )
        self._pool.append(node)
        return node

    def add_node(self, node: ClaimNode) -> None:
        self._pool.append(node)

    def get(self, claim_id: str) -> Optional[ClaimNode]:
        return next((c for c in self._pool if c.claim_id == claim_id), None)

    def all(self) -> List[ClaimNode]:
        return list(self._pool)

    def viable(self) -> List[ClaimNode]:
        return [c for c in self._pool if c.is_viable]

    def clear(self) -> None:
        self._pool.clear()

    def inject_from_reasoner(self, reasoner_output: Dict[str, Any]) -> None:
        for claim_dict in reasoner_output.get("claims", []):
            self.add(
                text=claim_dict.get("text", ""),
                source=f"reasoner:{reasoner_output.get('reasoner', 'unknown')}",
                tags=claim_dict.get("tags", []),
                metadata=claim_dict.get("metadata", {}),
            )
