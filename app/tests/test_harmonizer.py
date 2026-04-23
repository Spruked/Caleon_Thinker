import pytest
from app.harmonizer.harmonizer import Harmonizer


def make_harmonizer_inputs():
    egf_state = {
        "candidates": [],
        "convergence": {"state": "narrowing"},
    }
    tribunal_results = [
        {
            "claim_id": "c1", "text": "top candidate",
            "evidence_mass": 0.8, "softmax_score": 0.6,
            "ethically_permitted": True, "tribunal_flags": [],
            "uncertainty_penalty": 0.1, "fragility_penalty": 0.05,
        }
    ]
    closure = {
        "intuition": {"confidence": 0.7, "intuition_pick": tribunal_results[0]},
        "deduction": {"confidence": 0.65},
        "induction": {"confidence": 0.6},
        "top_candidates": tribunal_results,
    }
    wisdom = {
        "tone": "measured", "urgency": "normal",
        "restraint_level": "proceed", "humility_note": "",
        "proverb": "Trust but verify.", "escalate": False,
    }
    context = {"user_input": "test", "task_type": "factual", "llm_allowed": True}
    return egf_state, tribunal_results, closure, wisdom, context


def test_harmonizer_returns_selected():
    h = Harmonizer()
    egf_state, tribunal_results, closure, wisdom, context = make_harmonizer_inputs()
    result = h.resolve(egf_state, tribunal_results, closure, wisdom, context)
    assert "selected" in result
    assert result["selected"]["text"] == "top candidate"


def test_harmonizer_collects_flags():
    h = Harmonizer()
    egf_state, tribunal_results, closure, wisdom, context = make_harmonizer_inputs()
    tribunal_results[0]["uncertainty_penalty"] = 0.9
    result = h.resolve(egf_state, tribunal_results, closure, wisdom, context)
    assert "high_uncertainty" in result["flags"]


def test_harmonizer_final_tone():
    h = Harmonizer()
    egf_state, tribunal_results, closure, wisdom, context = make_harmonizer_inputs()
    wisdom["tone"] = "firm"
    result = h.resolve(egf_state, tribunal_results, closure, wisdom, context)
    assert result["final_tone"] == "firm"
