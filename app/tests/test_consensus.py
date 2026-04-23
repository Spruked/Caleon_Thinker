import pytest
from app.resilience.byzantine_consensus import ByzantineConsensus
from app.resilience.quorum import Quorum
from app.resilience.ping_drift_protection import PingDriftProtection
from app.resilience.signed_verdicts import SignedVerdict


def test_byzantine_commit_with_quorum():
    bc = ByzantineConsensus(quorum_size=3)
    hash_val = "abc123"
    verdicts = [{"decision_hash": hash_val, "node": f"n{i}"} for i in range(4)]
    result = bc.commit(verdicts)
    assert result["committed"] is True
    assert result["decision_hash"] == hash_val


def test_byzantine_no_quorum():
    bc = ByzantineConsensus(quorum_size=5)
    verdicts = [{"decision_hash": "h1", "node": f"n{i}"} for i in range(3)]
    result = bc.commit(verdicts)
    assert result["committed"] is False


def test_quorum_majority():
    q = Quorum(required=3)
    verdicts = [{"decision_hash": "h1"}, {"decision_hash": "h1"}, {"decision_hash": "h1"},
                {"decision_hash": "h2"}]
    result = q.check(verdicts)
    assert result["reached"] is True
    assert result["decision_hash"] == "h1"


def test_ping_drift_healthy():
    pdp = PingDriftProtection(max_skew_ms=250)
    result = pdp.ping()
    assert result["healthy"] is True
    assert "drift_ms" in result


def test_signed_verdict_round_trip():
    sv = SignedVerdict()
    verdict = {"decision_hash": "hash123", "allow": True, "confidence": 0.9}
    signed = sv.sign(verdict, "node_1")
    assert "decision_hash" in signed
    assert "node_id" in signed
