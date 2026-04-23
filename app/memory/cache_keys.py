import hashlib
import json
from typing import Any


def _stable_hash(obj: Any) -> str:
    serialized = json.dumps(obj, sort_keys=True, default=str)
    return hashlib.sha256(serialized.encode()).hexdigest()[:16]


def build_cache_key(
    user_input: str,
    user_scope: str,
    policy_version: str,
    articulation_profile: str,
    vault_revision: str,
    task_type: str,
) -> str:
    """Canonical cache key per spec: input hash + scope + policy + articulation + vault + task."""
    input_hash = _stable_hash(user_input)
    return "|".join([
        input_hash,
        user_scope or "global",
        policy_version,
        articulation_profile,
        vault_revision,
        task_type,
    ])


def build_retrieval_key(user_input: str, task_type: str, vault_revision: str) -> str:
    input_hash = _stable_hash(user_input)
    return f"retrieval|{input_hash}|{task_type}|{vault_revision}"


def build_reasoning_fragment_key(reasoner_name: str, task_type: str, input_hash: str) -> str:
    return f"fragment|{reasoner_name}|{task_type}|{input_hash}"
