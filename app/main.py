"""
Caleon Thinker — Entry point and factory.
Assembles all subsystems and exposes a single run() call.
"""
import uuid
from typing import Any, Dict, Optional

from app.config.settings import settings
from app.core.context_packet import ContextPacket
from app.core.orchestrator import CognitiveOrchestrator
from app.egf.gravity_field import EpistemologicalGravityField
from app.memory.memory_matrix import MemoryMatrix
from app.reasoners.registry import ReasonerRegistry
from app.reasoners.primary.intuition import IntuitiveReasoner
from app.reasoners.primary.deduction import DeductiveReasoner
from app.reasoners.primary.induction import InductiveReasoner
from app.reasoners.primary.primary_closure import PrimaryClosure
from app.reasoners.specialized.abductive import AbductiveReasoner
from app.reasoners.specialized.analogical import AnalogicalReasoner
from app.reasoners.specialized.causal import CausalReasoner
from app.reasoners.specialized.critical import CriticalReasoner
from app.reasoners.specialized.counterfactual import CounterfactualReasoner
from app.reasoners.specialized.diagnostic import DiagnosticReasoner
from app.reasoners.specialized.probabilistic import ProbabilisticReasoner
from app.reasoners.specialized.statistical import StatisticalReasoner
from app.reasoners.specialized.strategic import StrategicReasoner
from app.reasoners.specialized.temporal import TemporalReasoner
from app.reasoners.specialized.spatial import SpatialReasoner
from app.reasoners.specialized.moral import MoralReasoner
from app.reasoners.specialized.reflective import ReflectiveReasoner
from app.reasoners.specialized.heuristic import HeuristicReasoner
from app.reasoners.specialized.pattern import PatternReasoner
from app.reasoners.specialized.means_end import MeansEndReasoner
from app.reasoners.specialized.hypothetical import HypotheticalReasoner
from app.reasoners.specialized.comparative import ComparativeReasoner
from app.reasoners.specialized.anomaly import AnomalyReasoner
from app.reasoners.specialized.systems import SystemsReasoner
from app.reasoners.specialized.contextual import ContextualReasoner
from app.reasoners.specialized.predictive import PredictiveReasoner
from app.reasoners.specialized.interpretive import InterpretiveReasoner
from app.reasoners.specialized.adversarial import AdversarialReasoner
from app.tribunal.tribunal_engine import TribunalEngine
from app.tribunal.kant_engine import KantEngine
from app.tribunal.hume_engine import HumeEngine
from app.tribunal.locke_engine import LockeEngine
from app.tribunal.spinoza_engine import SpinozaEngine
from app.tribunal.gladwell_modulator import GladwellModulator
from app.tribunal.taleb_modulator import TalebModulator
from app.scoring.softmax_engine import SoftmaxEngine
from app.scoring.truthfulness_score import TruthfulnessScorer
from app.scoring.accuracy_score import AccuracyScorer
from app.scoring.uncertainty_penalty import UncertaintyPenaltyScorer
from app.scoring.fragility_penalty import FragilityPenaltyScorer
from app.wisdom.wisdom_engine import WisdomEngine
from app.harmonizer.harmonizer import Harmonizer
from app.articulation.articulation_engine import ArticulationEngine
from app.articulation.articulation_vault import ArticulationVault
from app.articulation.style_router import StyleRouter
from app.articulation.response_templates import ResponseTemplates
from app.articulation.output_guard import OutputGuard
from app.articulation.llm_bridge import LLMBridge
from app.telemetry.telemetry import TelemetrySystem
from app.recursion.recursive_review import RecursiveReview


def build_orchestrator(llm_client=None) -> CognitiveOrchestrator:
    memory = MemoryMatrix()
    memory.initialize()

    registry = ReasonerRegistry()
    for r in [
        AbductiveReasoner(), AnalogicalReasoner(), CausalReasoner(),
        CriticalReasoner(), CounterfactualReasoner(), DiagnosticReasoner(),
        ProbabilisticReasoner(), StatisticalReasoner(), StrategicReasoner(),
        TemporalReasoner(), SpatialReasoner(), MoralReasoner(),
        ReflectiveReasoner(), HeuristicReasoner(), PatternReasoner(),
        MeansEndReasoner(), HypotheticalReasoner(), ComparativeReasoner(),
        AnomalyReasoner(), SystemsReasoner(), ContextualReasoner(),
        PredictiveReasoner(), InterpretiveReasoner(), AdversarialReasoner(),
    ]:
        registry.register(r)

    tribunal = TribunalEngine([
        KantEngine(), HumeEngine(), LockeEngine(), SpinozaEngine(),
        GladwellModulator(), TalebModulator(),
    ])

    softmax = SoftmaxEngine()
    truth_scorer = TruthfulnessScorer()
    acc_scorer = AccuracyScorer()
    unc_scorer = UncertaintyPenaltyScorer()
    frag_scorer = FragilityPenaltyScorer()

    class ScoredSoftmax:
        def score(self, egf_state, tribunal_results, context):
            for c in tribunal_results:
                truth_scorer.apply_all([c], context)
                acc_scorer.apply_all([c], context)
                unc_scorer.apply_all([c])
                frag_scorer.apply_all([c])
            return softmax.score(egf_state, tribunal_results, context)

    intuition = IntuitiveReasoner()
    deduction = DeductiveReasoner()
    induction = InductiveReasoner()
    closure = PrimaryClosure(intuition, deduction, induction)

    llm_bridge = LLMBridge(client=llm_client, model=settings.LLM_MODEL) if settings.LLM_ENABLED else None
    art_cache = memory.cache

    articulation = ArticulationEngine(
        vault=ArticulationVault(),
        style_router=StyleRouter(),
        templates=ResponseTemplates(),
        cache=art_cache,
        llm_bridge=llm_bridge,
        output_guard=OutputGuard(),
    )

    return CognitiveOrchestrator(
        memory_router=memory.get_router(),
        egf=EpistemologicalGravityField(),
        reasoner_registry=registry,
        tribunal_engine=tribunal,
        softmax_engine=ScoredSoftmax(),
        primary_closure=closure,
        wisdom_engine=WisdomEngine(),
        harmonizer=Harmonizer(),
        articulation_engine=articulation,
        telemetry=TelemetrySystem(),
        recursion_engine=RecursiveReview(max_iterations=settings.RECURSION_MAX_ITER),
    )


def run(
    user_input: str,
    intent: str = "",
    task_type: str = None,
    metadata: Dict[str, Any] = None,
    llm_client=None,
) -> Dict[str, Any]:
    orchestrator = build_orchestrator(llm_client=llm_client)
    context = ContextPacket(
        request_id=str(uuid.uuid4()),
        user_input=user_input,
        intent=intent or user_input[:80],
        task_type=task_type or settings.DEFAULT_TASK_TYPE,
        metadata=metadata or {},
        llm_allowed=settings.LLM_ENABLED,
        policy_version=settings.POLICY_VERSION,
        articulation_profile=settings.ARTICULATION_PROFILE,
        vault_revision=settings.VAULT_REVISION,
    )
    return orchestrator.run(context)


if __name__ == "__main__":
    import sys
    prompt = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Hello, Caleon."
    result = run(user_input=prompt)
    print(result.get("text", result))
