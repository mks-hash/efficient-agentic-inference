# ADR 0009: Unique ranking through a candidate score vector

Date: 2026-10-07. Status: accepted for preparation; paid execution NOT_AUTHORIZED.

## Decision

Compare the previous candidate-constrained path-array recipe with a new
`candidate-score-vector-v1` recipe on 30 fresh `validation-v2` issues. Reuse both
pinned model artifacts, backend, bounded repository evidence and strict evaluator.
The new recipe generates one integer from 0 through 100 per input candidate,
in the existing path-sorted candidate order. Scores are relevance estimates,
not calibrated probabilities. Zero means excluded. Map positive entries to
their corresponding paths, sort by descending score then lexicographic path,
and take at most ten. A complete all-zero vector maps to an empty ranking.

This mapping defines the new model output representation before evaluation.
It never repairs, deduplicates or rescues a malformed path-array answer. Invalid,
wrong-length, noninteger or out-of-range vectors fail. Repeated scores are valid
ties, not repeated path identities; every input candidate has a single position.
The old path parser still rejects duplicates. The evaluator remains unchanged.

The pinned converter does not support uniqueItems. A stateless enumeration of
all path permutations is impractical at twenty candidates. A bounded score vector
uses ordinary fixed-length arrays and finite integer enums, with no backend
upgrade, repeated model calls, gold-aware masks or custom sampler state.

## Comparability and limits

This tests an entire representation/prompt/mapping recipe, not uniqueness alone.
The system prompt, generated tokens and ranking rule differ; record those costs.
The canonical user message and semantic evidence stay identical, but native
full-prompt token IDs must differ as expected. Ties introduce a deterministic
path-order prior; publish tie/exclusion diagnostics without tuning thresholds.
No probability-calibration, model-size causality or fallback claim follows.

Keep localization-v2, prediction schema 2.0.0 and accounting v1. A new campaign
contract and population separate these results from frozen historical runs.
Primary: S-scores minus S-paths all-attempt Recall@5. G is exploratory. The
[protocol](../docs/experiments/score-ranking-validation-v2.md) fixes all rules.

The selection reads only the existing allowlisted issue metadata and excludes
dev-v1, dev-v2, validation-v1 and every Verified ID/normalized equivalent. The
result has eight pvlib, eight pydicom, seven astroid and seven sqlfluff issues.
Only four seen repositories remain eligible: no repo/time generalization claim.
After exposure, future training excludes all frozen evaluation populations.

## Gates and authorization

Freeze this contract, split, prompts, configs, mapping/parser and evaluator before
reconstruction or validation inference. Use independent synthetic fixtures for
binding, integer strictness, ties, zero scores, empty candidates and the twenty
candidate boundary. Verify an actual isolated CPU synthetic score response and
historical path request compatibility. Native GPU/14B/new-validation quality
remain NOT_RUN. Model weights already local may be used for technical CPU probes;
no new paid run, publication, training or validation inference is authorized.
