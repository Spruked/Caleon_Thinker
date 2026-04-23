from typing import Any, Dict


class ResponseTemplates:
    def render(self, harmonized: Dict[str, Any], style: str, context: Dict[str, Any]) -> Dict[str, Any]:
        selected = harmonized.get("selected", {})
        text = selected.get("text", "")
        tone = harmonized.get("final_tone", "measured")
        flags = harmonized.get("flags", [])
        conflicts = harmonized.get("conflicts", [])

        if style == "direct_refusal_with_reason":
            rendered = self._refusal(selected, flags)
        elif style == "qualified_exploration":
            rendered = self._qualified(text, tone, conflicts)
        elif style == "concise_direct":
            rendered = self._concise(text)
        else:
            rendered = self._balanced(text, tone, flags)

        return {"text": rendered, "tone": tone, "flags": flags, "style": style}

    def _refusal(self, selected: Dict[str, Any], flags: list) -> str:
        reason = "; ".join(flags) if flags else "ethical constraints"
        return f"This cannot be completed: {reason}."

    def _qualified(self, text: str, tone: str, conflicts: list) -> str:
        prefix = "With the following considerations in mind: " if conflicts else ""
        return f"{prefix}{text}"

    def _concise(self, text: str) -> str:
        return text[:300] if text else "No output available."

    def _balanced(self, text: str, tone: str, flags: list) -> str:
        flag_note = f" [Note: {'; '.join(flags[:2])}]" if flags else ""
        return f"{text}{flag_note}"
