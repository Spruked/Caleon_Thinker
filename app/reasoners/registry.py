from typing import Dict, List, Any, Type
from app.reasoners.base import BaseReasoner
from app.core.enums import TaskType


TASK_REASONER_MAP: Dict[str, List[str]] = {
    TaskType.FACTUAL: ["deductive", "inductive", "probabilistic", "statistical", "causal"],
    TaskType.ETHICAL: ["moral", "critical", "adversarial", "reflective", "causal", "analogical"],
    TaskType.STRATEGIC: ["strategic", "causal", "means_end", "predictive", "systems", "temporal"],
    TaskType.DIAGNOSTIC: ["diagnostic", "abductive", "causal", "anomaly", "pattern", "statistical"],
    TaskType.CREATIVE: ["analogical", "hypothetical", "abductive", "interpretive", "comparative"],
    TaskType.REFLECTIVE: ["reflective", "critical", "contextual", "moral", "interpretive"],
    TaskType.ADVERSARIAL: ["adversarial", "critical", "counterfactual", "causal", "probabilistic"],
    TaskType.UNKNOWN: ["abductive", "critical", "causal", "probabilistic"],
}


class ReasonerRegistry:
    def __init__(self):
        self._specialized: Dict[str, BaseReasoner] = {}

    def register(self, reasoner: BaseReasoner) -> None:
        self._specialized[reasoner.name] = reasoner

    def get(self, name: str) -> BaseReasoner:
        return self._specialized[name]

    def select_for_task(self, task_type: str) -> List[BaseReasoner]:
        names = TASK_REASONER_MAP.get(task_type, TASK_REASONER_MAP[TaskType.UNKNOWN])
        return [self._specialized[n] for n in names if n in self._specialized]

    def run_specialized(self, context: Dict[str, Any], egf_state: Dict[str, Any]) -> List[Dict[str, Any]]:
        task_type = context.get("task_type", TaskType.UNKNOWN)
        active = self.select_for_task(task_type)
        enriched_ctx = {**context, "egf_state": egf_state}
        results = []
        for reasoner in active:
            try:
                result = reasoner.evaluate(enriched_ctx)
                results.append(result)
            except Exception as exc:
                results.append({
                    "reasoner": reasoner.name,
                    "claims": [],
                    "confidence": 0.0,
                    "risks": [str(exc)],
                    "notes": ["reasoner_error"],
                })
        return results

    def all_names(self) -> List[str]:
        return list(self._specialized.keys())
