from typing import Dict, Any, List
from app.tribunal.verdict_fusion import VerdictFusion


class TribunalEngine:
    def __init__(self, engines: list):
        self.engines = engines
        self.fusion = VerdictFusion()

    def review_all(self, egf_state: Dict[str, Any], context: Dict[str, Any]) -> List[Dict[str, Any]]:
        results = []
        for candidate in egf_state.get("candidates", []):
            frame_reviews = {}
            for engine in self.engines:
                frame_reviews[engine.frame_name] = engine.review(candidate, context)

            fused = self.fusion.fuse(frame_reviews)
            candidate["tribunal"] = frame_reviews
            candidate["ethically_permitted"] = fused["permitted"]
            candidate["tribunal_confidence"] = fused["consensus_confidence"]
            candidate["tribunal_flags"] = fused["flags"]
            results.append(candidate)

        return results

    def _permit(self, frame_reviews: Dict[str, Dict[str, Any]]) -> bool:
        from app.core.enums import TribunalFrame
        kant = frame_reviews.get(TribunalFrame.KANT, {}).get("allow", False)
        hume = frame_reviews.get(TribunalFrame.HUME, {}).get("allow", False)
        locke = frame_reviews.get(TribunalFrame.LOCKE, {}).get("allow", False)
        spinoza = frame_reviews.get(TribunalFrame.SPINOZA, {}).get("allow", False)
        return locke and kant and (hume or spinoza)
