from typing import Dict, Any, List
from app.core.enums import TribunalFrame


class VerdictFusion:
    """Merges tribunal verdicts into a unified permission and confidence signal."""

    REQUIRED_FRAMES = {TribunalFrame.KANT, TribunalFrame.HUME, TribunalFrame.LOCKE, TribunalFrame.SPINOZA}

    def fuse(self, frame_reviews: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        all_flags = []
        confidence_sum = 0.0
        frame_count = 0
        dissenting = []

        for frame_name, review in frame_reviews.items():
            allow = review.get("allow", True)
            if not allow:
                dissenting.append(frame_name)
            all_flags.extend(review.get("flags", []))
            confidence_sum += review.get("confidence", 0.5)
            frame_count += 1

        consensus_confidence = confidence_sum / max(frame_count, 1)

        kant = frame_reviews.get(TribunalFrame.KANT, {}).get("allow", False)
        hume = frame_reviews.get(TribunalFrame.HUME, {}).get("allow", False)
        locke = frame_reviews.get(TribunalFrame.LOCKE, {}).get("allow", False)
        spinoza = frame_reviews.get(TribunalFrame.SPINOZA, {}).get("allow", False)
        permitted = locke and kant and (hume or spinoza)

        taleb = frame_reviews.get(TribunalFrame.TALEB, {})
        gladwell = frame_reviews.get(TribunalFrame.GLADWELL, {})

        return {
            "permitted": permitted,
            "consensus_confidence": consensus_confidence,
            "dissenting_frames": dissenting,
            "flags": list(set(all_flags)),
            "taleb_fragility": taleb.get("fragility_score", 0.0),
            "gladwell_tipping": gladwell.get("tipping", False),
        }
