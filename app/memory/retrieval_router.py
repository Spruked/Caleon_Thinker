from typing import Any, Dict, List
from app.memory.a_priori_vault import APrioriVault
from app.memory.a_posteriori_vault import APosterioriVault
from app.memory.reflection_vault import ReflectionVault
from app.memory.cache import ResponseCache
from app.memory.cache_keys import build_cache_key, build_retrieval_key
from app.memory.cache_invalidator import CacheInvalidator
from app.memory.prior_decision_index import PriorDecisionIndex


class RetrievalRouter:
    """Routes memory retrieval across all vaults; enriches context; handles commit."""

    def __init__(
        self,
        a_priori: APrioriVault,
        a_posteriori: APosterioriVault,
        reflection: ReflectionVault,
        cache: ResponseCache,
        decision_index: PriorDecisionIndex,
    ):
        self.a_priori = a_priori
        self.a_posteriori = a_posteriori
        self.reflection = reflection
        self.cache = cache
        self.decision_index = decision_index
        self.invalidator = CacheInvalidator()

    def enrich(self, context: Any) -> Any:
        if isinstance(context, dict):
            ctx = context
        else:
            ctx = context.__dict__

        retrieval_key = build_retrieval_key(
            ctx.get("user_input", ""),
            ctx.get("task_type", "unknown"),
            ctx.get("vault_revision", "1.0"),
        )
        cached_retrieval = self.cache.get(retrieval_key)
        if cached_retrieval:
            ctx["retrieved_memories"] = cached_retrieval
            ctx["cache_hit"] = True
            return context

        priors = self.a_priori.get_priors(ctx)
        learned = self.a_posteriori.retrieve(ctx)
        related = self.reflection.fetch_related(ctx)
        prior_decisions = self.decision_index.recent(10)

        bundle = {**priors, **learned, "reflection": related}
        self.cache.set(retrieval_key, bundle, ttl_seconds=120)

        ctx["retrieved_memories"] = bundle
        ctx["prior_decisions"] = prior_decisions
        ctx["cache_hit"] = False
        return context

    def commit(self, context: Any, reviewed: Dict[str, Any], response: Any) -> None:
        ctx = context if isinstance(context, dict) else context.__dict__
        decision_record = {
            "request_id": ctx.get("request_id"),
            "user_input": ctx.get("user_input", "")[:200],
            "task_type": ctx.get("task_type", "unknown"),
            "harmonized_output": reviewed,
        }
        self.reflection.record(decision_record)
        self.decision_index.index(decision_record)
        self.a_posteriori.update(decision_record, reviewed)

        cache_key = build_cache_key(
            ctx.get("user_input", ""),
            ctx.get("user_scope", "global"),
            ctx.get("policy_version", "1.0"),
            ctx.get("articulation_profile", "default"),
            ctx.get("vault_revision", "1.0"),
            ctx.get("task_type", "unknown"),
        )
        selected = reviewed.get("selected", {})
        confidence = reviewed.get("closure", {}).get("intuition", {}).get("confidence", 0)
        if self.invalidator.should_cache(selected, ctx, confidence):
            self.cache.set(cache_key, response)
