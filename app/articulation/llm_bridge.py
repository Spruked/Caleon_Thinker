from typing import Any, Dict


class LLMBridge:
    """Calls an external LLM only when templates are insufficient."""

    def __init__(self, client=None, model: str = "claude-sonnet-4-6", max_tokens: int = 1024):
        self.client = client
        self.model = model
        self.max_tokens = max_tokens

    def generate(self, harmonized: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        if self.client is None:
            return self._stub(harmonized)

        selected = harmonized.get("selected", {})
        tone = harmonized.get("final_tone", "measured")
        user_input = context.get("user_input", "")
        system_prompt = self._build_system(harmonized, context)

        response = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            system=system_prompt,
            messages=[{"role": "user", "content": user_input}],
        )
        text = response.content[0].text if response.content else ""
        return {"text": text, "tone": tone, "llm_model": self.model}

    def _build_system(self, harmonized: Dict[str, Any], context: Dict[str, Any]) -> str:
        tone = harmonized.get("final_tone", "measured")
        wisdom = harmonized.get("wisdom", {})
        humility = wisdom.get("humility_note", "")
        proverb = wisdom.get("proverb", "")
        lines = [
            f"You are Caleon, a cognitively rigorous assistant. Tone: {tone}.",
            f"Humility note: {humility}" if humility else "",
            f"Guiding principle: {proverb}" if proverb else "",
        ]
        return "\n".join(l for l in lines if l)

    def _stub(self, harmonized: Dict[str, Any]) -> Dict[str, Any]:
        selected = harmonized.get("selected", {})
        return {
            "text": selected.get("text", "LLM bridge not configured."),
            "tone": harmonized.get("final_tone", "measured"),
            "llm_model": "stub",
        }
