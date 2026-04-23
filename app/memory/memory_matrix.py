from app.memory.a_priori_vault import APrioriVault
from app.memory.a_posteriori_vault import APosterioriVault
from app.memory.reflection_vault import ReflectionVault
from app.memory.cache import ResponseCache
from app.memory.prior_decision_index import PriorDecisionIndex
from app.memory.retrieval_router import RetrievalRouter


class MemoryMatrix:
    """Single assembly point for all memory subsystems."""

    def __init__(self):
        self.a_priori = APrioriVault()
        self.a_posteriori = APosterioriVault()
        self.reflection = ReflectionVault()
        self.cache = ResponseCache()
        self.decision_index = PriorDecisionIndex()
        self.router = RetrievalRouter(
            a_priori=self.a_priori,
            a_posteriori=self.a_posteriori,
            reflection=self.reflection,
            cache=self.cache,
            decision_index=self.decision_index,
        )

    def initialize(self) -> None:
        self.a_priori.load_defaults()

    def get_router(self) -> RetrievalRouter:
        return self.router
