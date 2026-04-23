from enum import Enum, auto


class TaskType(str, Enum):
    FACTUAL = "factual"
    ETHICAL = "ethical"
    STRATEGIC = "strategic"
    DIAGNOSTIC = "diagnostic"
    CREATIVE = "creative"
    REFLECTIVE = "reflective"
    ADVERSARIAL = "adversarial"
    UNKNOWN = "unknown"


class ReasonerTier(str, Enum):
    PRIMARY = "primary"
    SPECIALIZED = "specialized"


class VaultType(str, Enum):
    A_PRIORI = "a_priori"
    A_POSTERIORI = "a_posteriori"
    REFLECTION = "reflection"
    CACHE = "cache"


class TribunalFrame(str, Enum):
    KANT = "KANT"
    HUME = "HUME"
    LOCKE = "LOCKE"
    SPINOZA = "SPINOZA"
    GLADWELL = "GLADWELL"
    TALEB = "TALEB"


class ArticulationMode(str, Enum):
    TEMPLATE = "template"
    LLM = "llm"
    CACHE_HIT = "cache_hit"
    HYBRID = "hybrid"


class ConvergenceState(str, Enum):
    OPEN = "open"
    NARROWING = "narrowing"
    CONVERGED = "converged"
    DIVERGED = "diverged"
    UNCERTAIN = "uncertain"


class SeverityLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class GlyphStage(str, Enum):
    CONTEXT_LOADED = "context_loaded"
    A_PRIORI_APPLIED = "a_priori_applied"
    SPECIALIZED_REASONERS_SELECTED = "specialized_reasoners_selected"
    EGF_CONVERGENCE_UPDATE = "egf_convergence_update"
    TRIBUNAL_REVIEW_COMPLETE = "tribunal_review_complete"
    SOFTMAX_SCORED = "softmax_scored"
    PRIMARY_CLOSURE_COMPLETE = "primary_closure_complete"
    WISDOM_ADJUSTED = "wisdom_adjusted"
    HARMONIZER_RESOLVED = "harmonizer_resolved"
    ARTICULATION_CACHE_HIT = "articulation_cache_hit"
    REFLECTION_VAULT_UPDATED = "reflection_vault_updated"
