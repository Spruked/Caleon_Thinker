import pytest
from app.scoring.softmax_engine import SoftmaxEngine


def make_candidates(count=3):
    return [
        {
            "claim_id": f"c{i}",
            "text": f"candidate {i}",
            "evidence_mass": 0.3 + i * 0.2,
            "coherence_score": 0.5 + i * 0.1,
            "contradiction_drag": 0.1,
            "uncertainty_radius": 0.3,
            "uncertainty_penalty": 0.15,
            "fragility_penalty": 0.05,
            "ethically_permitted": True,
            "tribunal_flags": [],
        }
        for i in range(count)
    ]


def test_softmax_scores_sum_to_one():
    engine = SoftmaxEngine()
    candidates = make_candidates(4)
    scored = engine.score({"candidates": candidates}, candidates, {})
    total = sum(c["softmax_score"] for c in scored)
    assert total == pytest.approx(1.0, abs=0.001)


def test_softmax_sorted_descending():
    engine = SoftmaxEngine()
    candidates = make_candidates(4)
    scored = engine.score({"candidates": candidates}, candidates, {})
    scores = [c["softmax_score"] for c in scored]
    assert scores == sorted(scores, reverse=True)


def test_softmax_ethical_penalty_reduces_score():
    engine = SoftmaxEngine()
    permitted = {"text": "allowed", "evidence_mass": 0.7, "coherence_score": 0.7,
                 "uncertainty_penalty": 0.1, "fragility_penalty": 0.0, "ethically_permitted": True}
    blocked = {"text": "blocked", "evidence_mass": 0.7, "coherence_score": 0.7,
               "uncertainty_penalty": 0.1, "fragility_penalty": 0.0, "ethically_permitted": False}
    scored = engine.score({"candidates": [permitted, blocked]}, [permitted, blocked], {})
    permitted_score = next(c["softmax_score"] for c in scored if c["text"] == "allowed")
    blocked_score = next(c["softmax_score"] for c in scored if c["text"] == "blocked")
    assert permitted_score > blocked_score


def test_softmax_empty_candidates():
    engine = SoftmaxEngine()
    scored = engine.score({"candidates": []}, [], {})
    assert scored == []
