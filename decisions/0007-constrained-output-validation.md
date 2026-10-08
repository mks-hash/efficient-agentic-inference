# ADR 0007: Output constraints on fresh same-repository validation

Date: 2026-10-07. Status: accepted for preparation; paid execution NOT_AUTHORIZED.

## Decision and motivation

Compare each already selected model with itself, with and without a generation-time
JSON/candidate constraint, on the reserved 20 validation-v1 issues. The exposed
dev-v2 comparison motivates this intervention; its validity-conditioned diagnostic
is post hoc and selected, and does not prove superior 14B ranking capability.
Do not change models, prompts, evidence, sampling, gold policy or the grader.

The versioned intervention is `candidate-json-array-v1`: an array of zero to ten
strings drawn from the path-sorted inference candidates. The schema is derived
solely from the canonical packet. It adds no gold, ranking hints or prompt tokens.
The pinned backend converts the request's JSON schema to a sampling grammar.
Its `uniqueItems` support is absent; duplicates remain failures in the unchanged
strict parser. Empty candidates permit only an empty array. No output extraction,
path correction, deduplication, retry or fallback is allowed.

## Comparability

Localization contract v2, artifact schemas 2.0.0 and accounting v1 remain unchanged.
This is a new execution intervention and campaign contract v1, not a reinterpretation
of frozen dev-v2 predictions. Compare four fresh arms on identical validation
packets; historical numbers provide context only. Same-repository unseen issues
do not establish repository-disjoint, temporal or pretraining-contamination controls.

Freeze protocol/config/prompt/split hashes before reconstructing validation data;
freeze exact code/build/model/input/hardware identities before its first generation.
Gold may be produced by the separate snapshot coordinator but must remain invisible
to inference. Do not inspect validation labels/quality until all four arms are
collected. Never replace a failed task or adjust the intervention after exposure.

Primary inference concerns the small model's within-model quality change. The
14B within-model change and model-by-constraint interaction are secondary,
exploratory diagnostics; no multiple confirmatory winner selection is permitted.
See the [preregistered protocol](../docs/experiments/reliability-validation-v1.md).

## Consequences

CPU fixtures and a short isolated synthetic 4B probe validate implementation only.
14B constrained generation, GPU gates and validation quality remain NOT_RUN until
an independently authorized run. Training is not justified by preparation or a
validity improvement alone. Actual invoice attribution and complete cost per
success remain separate evidence gates.
