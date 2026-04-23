import os


class FeatureFlags:
    LLM_ARTICULATION_ENABLED: bool = os.getenv("FF_LLM_ARTICULATION", "true").lower() == "true"
    BYZANTINE_CONSENSUS_ENABLED: bool = os.getenv("FF_BYZANTINE", "false").lower() == "true"
    GLYPH_TRACE_ENABLED: bool = os.getenv("FF_GLYPH_TRACE", "true").lower() == "true"
    RECURSION_ENABLED: bool = os.getenv("FF_RECURSION", "true").lower() == "true"
    ADVERSARIAL_REASONER_ENABLED: bool = os.getenv("FF_ADVERSARIAL", "true").lower() == "true"
    PING_DRIFT_ENABLED: bool = os.getenv("FF_PING_DRIFT", "true").lower() == "true"
    WISDOM_ENGINE_ENABLED: bool = os.getenv("FF_WISDOM", "true").lower() == "true"


feature_flags = FeatureFlags()
