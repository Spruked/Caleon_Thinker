import pytest
from app.egf.gravity_field import EpistemologicalGravityField
from app.egf.claim_node import ClaimNode
from app.egf.evidence_mass import EvidenceMassCalculator
from app.egf.contradiction_drag import ContradictionDragEngine
from app.egf.uncertainty_radius import UncertaintyRadius


def make_context(evidence=None, task_type="factual"):
    return {
        "user_input": "test input",
        "intent": "test",
        "task_type": task_type,
        "evidence_items": evidence or [],
    }


def test_egf_initialize_empty():
    egf = EpistemologicalGravityField()
    state = egf.initialize(make_context())
    assert "candidates" in state
    assert "convergence" in state


def test_claim_node_net_gravity():
    node = ClaimNode("c1", "test claim", "test_source", evidence_mass=0.8, contradiction_drag=0.2, coherence_score=0.9)
    assert node.net_gravity == pytest.approx((0.8 - 0.2) * 0.9)


def test_claim_node_viability():
    viable = ClaimNode("c1", "viable", "src", evidence_mass=0.8, coherence_score=0.8, uncertainty_radius=0.2)
    not_viable = ClaimNode("c2", "not viable", "src", evidence_mass=0.0, coherence_score=0.0, uncertainty_radius=1.0)
    assert viable.is_viable
    assert not not_viable.is_viable


def test_evidence_mass_calculator():
    calc = EvidenceMassCalculator()
    node = ClaimNode("c1", "test", "src")
    evidence = [{"weight": 0.8, "reliability": 0.9, "recency_factor": 1.0}]
    mass = calc.compute(evidence, node)
    assert mass == pytest.approx(0.72, abs=0.01)


def test_contradiction_drag():
    engine = ContradictionDragEngine()
    a = ClaimNode("c1", "claim a", "src", evidence_mass=0.8, tags=["topic"])
    b = ClaimNode("c2", "claim b", "src", evidence_mass=0.3, tags=["topic"])
    drag = engine.compute_pairwise(a, b)
    assert drag >= 0


def test_uncertainty_radius_decreases_with_evidence():
    ur = UncertaintyRadius()
    low = ClaimNode("c1", "low", "src", evidence_mass=0.9, coherence_score=0.8)
    high = ClaimNode("c2", "high", "src", evidence_mass=0.1)
    assert ur.compute(low) < ur.compute(high)


def test_egf_absorb_reasoner_results():
    egf = EpistemologicalGravityField()
    egf.initialize(make_context())
    results = [{"reasoner": "test", "claims": [{"text": "absorbed claim", "tags": ["test"]}]}]
    state = egf.absorb(results)
    assert state["total_claims"] >= 1
