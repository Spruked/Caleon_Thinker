# Caleon Thinker

Caleon Thinker is a unified ethical cognition engine designed to provide structured reasoning, calibrated judgment, memory continuity, explainability, and resilient decision flow.

It is intended to serve as the cognitive core for products such as Orb, True_Mark assistants, GOAT interfaces, and future Caleon systems.

---

## Core Purpose

Thinker exists to move beyond shallow prompt-response systems by combining:

- Multi-mode reasoning
- Ethical governance
- Memory architecture
- Recursive self-review
- Confidence calibration
- Harmonized output selection
- Cache-aware articulation
- Telemetry and traceability
- Fault tolerance concepts

---

## Architecture Summary

### Epistemological Gravity Field (EGF)

The central reasoning substrate where claims, evidence, constraints, and hypotheses compete and converge toward justified conclusions.

### Reasoning System

**3 Primary Closers**
- Intuition
- Deduction
- Induction

**24 Specialized Reasoners**

Including: Abductive, Causal, Analogical, Critical, Diagnostic, Adversarial, Probabilistic, Statistical, Strategic, Temporal, Spatial, Moral, Reflective, Heuristic, Pattern, Means-End, Hypothetical, Comparative, Anomaly, Systems, Contextual, Predictive, Interpretive, Counterfactual

### Tribunal Governance

Named framing engines with hardened logic:

| Frame | Principle |
|-------|-----------|
| KANT | Duty / universal constraints |
| HUME | Evidence sufficiency |
| LOCKE | Rights / authorization |
| SPINOZA | Coherence / causality |

**Permit logic:** `LOCKE AND KANT AND (HUME OR SPINOZA)`

### Advisory Modulators

- **Gladwell** → hidden factors / outliers / tipping dynamics
- **Taleb** → antifragility / tail risk

### Memory System

- A Priori Vault — immutable rules, schemas, principles
- A Posteriori Vault — learned cases, patterns, preferences
- Reflection Vault — prior decisions for recursive review
- Cache Layer — strict invalidation policy; never cache blindly

### Output Stack

- Softmax scoring (truthfulness, accuracy, coherence, uncertainty penalty, fragility penalty)
- Wisdom guidance (tone, restraint, timing, humility)
- Harmonizer (signal reconciliation, conflict resolution)
- Articulation engine (cache → template → LLM, in that order)
- Output guard (final safety filter)

### Observability

- Glyph Trace — meaning-level trace across all cognitive stages
- Telemetry — system health and performance signals
- Metrics — counters, durations, gauges
- Health monitoring

### Resilience

- Ping drift protection
- Redundancy manager
- Byzantine consensus
- Signed verdict support

---

## Project Structure

```text
caleon/
└── app/
    ├── core/          — ContextPacket, DecisionPacket, Orchestrator, enums, exceptions
    ├── egf/           — Gravity field, claim nodes, evidence mass, convergence
    ├── reasoners/     — 3 primary closers + 24 specialized reasoners + registry
    ├── tribunal/      — Kant, Hume, Locke, Spinoza, Gladwell, Taleb, verdict fusion
    ├── memory/        — A priori, a posteriori, reflection vaults + cache
    ├── scoring/       — Softmax, truthfulness, accuracy, uncertainty, fragility
    ├── wisdom/        — Tone, restraint, timing, humility, proverb principles
    ├── harmonizer/    — Signal reconciler, conflict resolver, articulation alignment
    ├── articulation/  — Engine, templates, LLM bridge, output guard
    ├── telemetry/     — Glyph trace, telemetry, metrics, event bus, health monitor
    ├── recursion/     — Recursive review, self-check, drift recheck, outcome reflection
    ├── resilience/    — Ping drift, redundancy, Byzantine consensus, quorum, signed verdicts
    ├── security/      — ChaCha20-Poly1305 wrapper, HMAC verifier, manifest hash, governance capsule
    ├── schemas/       — Claims, evidence, verdicts, memory, telemetry
    ├── config/        — Settings, constants, feature flags
    └── tests/         — 47 tests across all subsystems
```

---

## Quickstart

```bash
# Clone and set up
git clone https://github.com/Spruked/Caleon_Thinker.git
cd Caleon_Thinker
python -m venv .venv
.venv/Scripts/pip install pytest

# Run a single thought
.venv/Scripts/python app/main.py "Is it ethical to deceive someone for their own benefit?"

# Run all tests
.venv/Scripts/python -m pytest app/tests/ -v
```

---

## Status

**v0.1.0** — canonical skeleton complete. All 9 build phases delivered. 47/47 tests passing.

> Caleon is a unified ethical cognition system built around an Epistemological Gravity Field, embedding 24 specialized reasoning forms that converge through intuition, deduction, and induction, governed by philosophically framed evaluators, stabilized by harmonization, structured vault memory, recursive reflection, cache-aware articulation, and drift-resistant telemetry.
