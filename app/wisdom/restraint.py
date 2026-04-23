from typing import List


class RestraintGuide:
    HIGH_RESTRAINT_FLAGS = {"deontological_violation", "consent_required_but_unverified", "unauthorized_access_signal"}

    def assess(self, flags: List[str], confidence: float) -> str:
        for flag in flags:
            for hrf in self.HIGH_RESTRAINT_FLAGS:
                if hrf in flag:
                    return "hold"
        if confidence < 0.3:
            return "defer"
        if confidence < 0.5:
            return "caution"
        return "proceed"
