from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ContextPacket:
    request_id: str
    user_input: str
    intent: str
    task_type: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    retrieved_memories: List[Dict[str, Any]] = field(default_factory=list)
    prior_decisions: List[Dict[str, Any]] = field(default_factory=list)
    evidence_items: List[Dict[str, Any]] = field(default_factory=list)
    active_reasoners: List[str] = field(default_factory=list)
    cache_hit: bool = False
    llm_allowed: bool = True
    policy_version: str = "1.0"
    user_scope: Optional[str] = None
    articulation_profile: str = "default"
    vault_revision: str = "1.0"
