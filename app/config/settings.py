import os


class Settings:
    APP_NAME: str = "Caleon Thinker"
    VERSION: str = "0.1.0"
    POLICY_VERSION: str = "1.0"
    VAULT_REVISION: str = "1.0"

    CACHE_DEFAULT_TTL: int = int(os.getenv("CALEON_CACHE_TTL", "300"))
    CACHE_MAX_SIZE: int = int(os.getenv("CALEON_CACHE_MAX_SIZE", "1000"))

    LLM_MODEL: str = os.getenv("CALEON_LLM_MODEL", "claude-sonnet-4-6")
    LLM_MAX_TOKENS: int = int(os.getenv("CALEON_LLM_MAX_TOKENS", "1024"))
    LLM_ENABLED: bool = os.getenv("CALEON_LLM_ENABLED", "true").lower() == "true"

    PING_DRIFT_MAX_MS: float = float(os.getenv("CALEON_PING_DRIFT_MS", "250"))
    BYZANTINE_QUORUM: int = int(os.getenv("CALEON_QUORUM", "4"))
    RECURSION_MAX_ITER: int = int(os.getenv("CALEON_RECURSION_MAX", "3"))

    ARTICULATION_PROFILE: str = os.getenv("CALEON_ARTICULATION_PROFILE", "default")
    DEFAULT_TASK_TYPE: str = os.getenv("CALEON_DEFAULT_TASK_TYPE", "unknown")

    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")


settings = Settings()
