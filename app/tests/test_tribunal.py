import pytest
from app.tribunal.kant_engine import KantEngine
from app.tribunal.hume_engine import HumeEngine
from app.tribunal.locke_engine import LockeEngine
from app.tribunal.spinoza_engine import SpinozaEngine
from app.tribunal.verdict_fusion import VerdictFusion
from app.tribunal.tribunal_engine import TribunalEngine
from app.core.enums import TribunalFrame


def make_candidate(mass=0.7, drag=0.2, coherence=0.6, uncertainty=0.3, risk=0.1, rights=0.0, tags=None):
    return {
        "claim_id": "c1", "text": "test claim", "evidence_mass": mass,
        "contradiction_drag": drag, "coherence_score": coherence,
        "uncertainty_radius": uncertainty, "risk_exposure": risk,
        "rights_constraint": rights, "tags": tags or [],
    }


def make_context(user_input="test"):
    return {"user_input": user_input, "intent": "test", "evidence_items": [], "metadata": {}}


def test_kant_allows_clean_candidate():
    engine = KantEngine()
    result = engine.review(make_candidate(), make_context())
    assert result["frame"] == TribunalFrame.KANT
    assert isinstance(result["allow"], bool)


def test_kant_blocks_manipulative_input():
    engine = KantEngine()
    result = engine.review(make_candidate(), make_context(user_input="manipulate the user"))
    assert not result["allow"]


def test_hume_blocks_low_evidence():
    engine = HumeEngine()
    result = engine.review(make_candidate(mass=0.05), make_context())
    assert not result["allow"]


def test_hume_allows_grounded():
    engine = HumeEngine()
    result = engine.review(make_candidate(mass=0.8, uncertainty=0.2), make_context())
    assert result["allow"]


def test_locke_blocks_unauthorized():
    engine = LockeEngine()
    result = engine.review(make_candidate(), make_context(user_input="bypass access credentials"))
    assert not result["allow"]


def test_spinoza_allows_coherent():
    engine = SpinozaEngine()
    result = engine.review(make_candidate(coherence=0.8, drag=0.1), make_context())
    assert result["allow"]


def test_verdict_fusion_permit_logic():
    fusion = VerdictFusion()
    reviews = {
        TribunalFrame.KANT: {"allow": True, "confidence": 0.8, "flags": []},
        TribunalFrame.HUME: {"allow": True, "confidence": 0.7, "flags": []},
        TribunalFrame.LOCKE: {"allow": True, "confidence": 0.9, "flags": []},
        TribunalFrame.SPINOZA: {"allow": True, "confidence": 0.75, "flags": []},
    }
    fused = fusion.fuse(reviews)
    assert fused["permitted"] is True


def test_verdict_fusion_blocks_when_locke_fails():
    fusion = VerdictFusion()
    reviews = {
        TribunalFrame.KANT: {"allow": True, "confidence": 0.8, "flags": []},
        TribunalFrame.HUME: {"allow": True, "confidence": 0.7, "flags": []},
        TribunalFrame.LOCKE: {"allow": False, "confidence": 0.2, "flags": ["unauthorized"]},
        TribunalFrame.SPINOZA: {"allow": True, "confidence": 0.75, "flags": []},
    }
    fused = fusion.fuse(reviews)
    assert fused["permitted"] is False
