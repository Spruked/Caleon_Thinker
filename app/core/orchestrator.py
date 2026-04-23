class CognitiveOrchestrator:
    def __init__(
        self,
        memory_router,
        egf,
        reasoner_registry,
        tribunal_engine,
        softmax_engine,
        primary_closure,
        wisdom_engine,
        harmonizer,
        articulation_engine,
        telemetry,
        recursion_engine,
    ):
        self.memory_router = memory_router
        self.egf = egf
        self.reasoner_registry = reasoner_registry
        self.tribunal_engine = tribunal_engine
        self.softmax_engine = softmax_engine
        self.primary_closure = primary_closure
        self.wisdom_engine = wisdom_engine
        self.harmonizer = harmonizer
        self.articulation_engine = articulation_engine
        self.telemetry = telemetry
        self.recursion_engine = recursion_engine

    def run(self, context):
        self.telemetry.start(context)

        context = self.memory_router.enrich(context)
        egf_state = self.egf.initialize(context)

        specialized_results = self.reasoner_registry.run_specialized(context, egf_state)
        egf_state = self.egf.absorb(specialized_results)

        tribunal_results = self.tribunal_engine.review_all(egf_state, context)
        scored_candidates = self.softmax_engine.score(egf_state, tribunal_results, context)

        closure = self.primary_closure.run(scored_candidates, context)
        wisdom_adjusted = self.wisdom_engine.apply(closure, context)

        harmonized = self.harmonizer.resolve(
            egf_state=egf_state,
            tribunal_results=tribunal_results,
            closure=closure,
            wisdom=wisdom_adjusted,
            context=context,
        )

        reviewed = self.recursion_engine.recheck(harmonized, context)
        response = self.articulation_engine.render(reviewed, context)

        self.memory_router.commit(context, reviewed, response)
        self.telemetry.finish(context, reviewed, response)

        return response
