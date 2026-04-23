from typing import Any, Dict
from app.wisdom.restraint import RestraintGuide
from app.wisdom.timing import TimingGuide
from app.wisdom.humility import HumilityGuide
from app.wisdom.tone_guidance import ToneGuide
from app.wisdom.proverb_principles import ProverbPrinciples


class WisdomEngine:
    def __init__(self):
        self.restraint = RestraintGuide()
        self.timing = TimingGuide()
        self.humility = HumilityGuide()
        self.tone = ToneGuide()
        self.proverbs = ProverbPrinciples()

    def apply(self, closure: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        top = (closure.get("top_candidates") or [{}])[0]
        flags = top.get("tribunal_flags", [])
        uncertainty = top.get("uncertainty_radius", 0.5)
        confidence = top.get("softmax_score", 0.5)

        tone = self.tone.select(flags, uncertainty, context)
        urgency = self.timing.assess(confidence, context)
        restraint_level = self.restraint.assess(flags, confidence)
        humility_note = self.humility.note(uncertainty, confidence)
        proverb = self.proverbs.select(context)

        return {
            "tone": tone,
            "urgency": urgency,
            "restraint_level": restraint_level,
            "humility_note": humility_note,
            "proverb": proverb,
            "escalate": restraint_level == "hold",
        }
