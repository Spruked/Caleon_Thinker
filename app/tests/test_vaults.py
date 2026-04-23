import pytest
from app.memory.a_priori_vault import APrioriVault
from app.memory.a_posteriori_vault import APosterioriVault
from app.memory.reflection_vault import ReflectionVault


def test_a_priori_loads_defaults():
    vault = APrioriVault()
    vault.load_defaults()
    priors = vault.get_priors()
    assert "principles" in priors
    assert "non_maleficence" in priors["principles"]
    assert "rules" in priors


def test_a_posteriori_update_and_retrieve():
    vault = APosterioriVault()
    vault.update(
        {"request_id": "r1", "task_type": "factual", "user_input": "hello world", "tags": []},
        {"selected": {"text": "hello response"}},
    )
    result = vault.retrieve()
    assert len(result["cases"]) == 1
    assert result["cases"][0]["request_id"] == "r1"


def test_a_posteriori_max_cases():
    vault = APosterioriVault(max_cases=3)
    for i in range(5):
        vault.update({"request_id": f"r{i}", "task_type": "factual", "user_input": f"input {i}", "tags": []}, {})
    assert len(vault._cases) == 3


def test_reflection_vault_record_and_fetch():
    vault = ReflectionVault()
    vault.record({"request_id": "r1", "user_input": "hello world test", "harmonized_output": {}})
    related = vault.fetch_related({"user_input": "hello world"})
    assert len(related) >= 1


def test_reflection_vault_max_decisions():
    vault = ReflectionVault(max_decisions=5)
    for i in range(10):
        vault.record({"request_id": f"r{i}", "user_input": f"input {i}"})
    assert len(vault._prior_decisions) == 5
