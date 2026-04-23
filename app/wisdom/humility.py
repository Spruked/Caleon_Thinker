class HumilityGuide:
    def note(self, uncertainty: float, confidence: float) -> str:
        if uncertainty > 0.7:
            return "High uncertainty — response should acknowledge limits of current evidence"
        if uncertainty > 0.4 or confidence < 0.5:
            return "Moderate uncertainty — qualify assertions appropriately"
        return ""
