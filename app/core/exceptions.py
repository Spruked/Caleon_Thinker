class CaleonError(Exception):
    pass


class EGFError(CaleonError):
    pass


class ConvergenceError(EGFError):
    pass


class ReasonerError(CaleonError):
    pass


class ReasonerNotFoundError(ReasonerError):
    pass


class TribunalError(CaleonError):
    pass


class VaultError(CaleonError):
    pass


class CacheError(VaultError):
    pass


class ArticulationError(CaleonError):
    pass


class LLMBridgeError(ArticulationError):
    pass


class HarmonizerError(CaleonError):
    pass


class SecurityError(CaleonError):
    pass


class SignatureVerificationError(SecurityError):
    pass


class ManifestIntegrityError(SecurityError):
    pass


class ResilienceError(CaleonError):
    pass


class QuorumNotReachedError(ResilienceError):
    pass


class DriftExceededError(ResilienceError):
    pass


class RecursionLimitError(CaleonError):
    pass
