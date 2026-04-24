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
        divergence_rkg=None,
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
        self.divergence_rkg = divergence_rkg

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

        # Post-verdict semantic divergence check
        if self.divergence_rkg is not None:
            verdict_text = harmonized.get("selected", {}).get("text", "")
            if verdict_text:
                ctx_dict = context if isinstance(context, dict) else context.__dict__
                evidence = [e.get("content", e.get("text", "")) for e in ctx_dict.get("evidence_items", [])]
                rkg_result = self.divergence_rkg.evaluate_verdict(
                    verdict_text=verdict_text,
                    supporting_evidence=[e for e in evidence if e],
                    harmonized=harmonized,
                    context=context if not isinstance(context, dict) else None,
                )
                if rkg_result.get("action") not in ("submit", "submit_justified"):
                    harmonized.setdefault("flags", []).append(
                        f"divergence:{rkg_result.get('action')}:score={rkg_result.get('score', 0):.2f}"
                    )
                harmonized["divergence_rkg"] = rkg_result

        reviewed = self.recursion_engine.recheck(harmonized, context)
        response = self.articulation_engine.render(reviewed, context)

        self.memory_router.commit(context, reviewed, response)
        self.telemetry.finish(context, reviewed, response)

        return response
