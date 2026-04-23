from typing import Any, Dict
from app.articulation.articulation_vault import ArticulationVault
from app.articulation.style_router import StyleRouter
from app.articulation.response_templates import ResponseTemplates
from app.articulation.output_guard import OutputGuard
from app.memory.cache import ResponseCache
from app.memory.cache_keys import build_cache_key


class ArticulationEngine:
    def __init__(
        self,
        vault: ArticulationVault,
        style_router: StyleRouter,
        templates: ResponseTemplates,
        cache: ResponseCache,
        llm_bridge=None,
        output_guard: OutputGuard = None,
    ):
        self.vault = vault
        self.style_router = style_router
        self.templates = templates
        self.cache = cache
        self.llm_bridge = llm_bridge
        self.output_guard = output_guard or OutputGuard()

    def render(self, harmonized: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        ctx = context if isinstance(context, dict) else context.__dict__

        cache_key = build_cache_key(
            ctx.get("user_input", ""),
            ctx.get("user_scope", "global"),
            ctx.get("policy_version", "1.0"),
            ctx.get("articulation_profile", "default"),
            ctx.get("vault_revision", "1.0"),
            ctx.get("task_type", "unknown"),
        )
        cached = self.cache.get(cache_key)
        if cached:
            return {**cached, "articulation_mode": "cache_hit", "cache_hit": True}

        hint = harmonized.get("articulation_hint", {})
        style = hint.get("style", "balanced_measured")
        tone = hint.get("tone", "measured")
        use_templates = hint.get("use_templates", True)

        if use_templates:
            response = self.templates.render(harmonized, style, ctx)
            mode = "template"
        elif self.llm_bridge and ctx.get("llm_allowed", True):
            response = self.llm_bridge.generate(harmonized, ctx)
            mode = "llm"
        else:
            response = self._fallback_render(harmonized)
            mode = "fallback"

        if hint.get("include_humility_note") and hint.get("humility_note"):
            response["humility_addendum"] = hint["humility_note"]

        response["articulation_mode"] = mode
        response = self.output_guard.check(response, ctx)
        return response

    def _fallback_render(self, harmonized: Dict[str, Any]) -> Dict[str, Any]:
        selected = harmonized.get("selected", {})
        return {
            "text": selected.get("text", "No response generated"),
            "tone": harmonized.get("final_tone", "measured"),
            "flags": harmonized.get("flags", []),
        }
