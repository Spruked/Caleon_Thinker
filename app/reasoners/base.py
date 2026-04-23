from abc import ABC, abstractmethod
from typing import Dict, Any, List


class BaseReasoner(ABC):
    name: str

    @abstractmethod
    def evaluate(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Returns:
        {
            "reasoner": self.name,
            "claims": [...],
            "confidence": 0.0,
            "risks": [...],
            "notes": [...],
        }
        """
        raise NotImplementedError

    def _result(
        self,
        claims: List[Dict[str, Any]] = None,
        confidence: float = 0.0,
        risks: List[str] = None,
        notes: List[str] = None,
    ) -> Dict[str, Any]:
        return {
            "reasoner": self.name,
            "claims": claims or [],
            "confidence": confidence,
            "risks": risks or [],
            "notes": notes or [],
        }

    def _claim(
        self,
        text: str,
        tags: List[str] = None,
        metadata: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        return {
            "text": text,
            "tags": tags or [],
            "metadata": metadata or {},
        }
