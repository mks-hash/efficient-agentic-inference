# Benchmark contract: SWE-bench file localization v1

Archived fixture contract. The active separated-program contract is
[localization-v2](benchmark-localization-v2.md); the combined v1 CLI is retired.

Contract identifier: `localization-v1`. Status: design; SWE-bench pipeline not yet
implemented. The CPU runner consumes the canonical records described here.

## Input and separation

One task record has instance_id, repository, base_commit, issue text and candidates
(relative file path + allowed source text). Task records contain no gold patches,
gold locations, test patch, FAIL_TO_PASS/PASS_TO_PASS or solution metadata.
Candidate text must come from the base commit. No gold-driven candidate selection.
Canonical gold records live separately and are joined only by the evaluator.

Require unique instance IDs and candidate paths. Paths use POSIX repository-relative
syntax, no absolute paths or parent traversal. Prediction is an ordered, unique
list of existing candidate paths. Unknown paths, malformed or truncated output
is invalid, preserved and scored as failure without silent repair.

## Labels and eligible population

Derive changed old/new paths from the accepted implementation patch, never the
test_patch field. Keep all changed files plus implementation/test/non-code subsets.
Freeze extension and test-directory rules in a versioned label policy before
SWE-bench use; do not manually discard awkward tasks.

Existing/modified/deleted files map to base-commit paths. Renames map to old paths.
New files have no base-commit candidate: retain explicit new-file labels and report
unreachable labels/candidate recall ceiling, including these in all-file recall.
Pure rename, binary, empty and unsupported patches require explicit dispositions.
Empty-gold tasks remain in the population with undefined recall/MRR and no strict
success; report their count and reason separately. They cannot establish model
quality. Eligibility and exclusion reasons must be frozen before evaluation.

Gold patch changes are reference labels, not unique necessary changes for every
valid repair. State that limitation in every report. AST symbol labeling is deferred
to a separate extension with explicit new-symbol sentinels and range semantics.

## Metrics

At K∈{1,3,5,10}: Recall@K = unique top-K gold hits / number of gold paths.
Precision@K = hits / K, including missing prediction slots. MRR = reciprocal rank
of the first gold match, zero for no match. Strict Success@K means all nonempty
gold paths occur in top K. Deduplication is a validation rule, not a repair step.
Invalid predictions receive zero recall/precision/MRR for nonempty gold and fail
strict success. Aggregate recall/MRR over nonempty-gold tasks and publish both
that denominator and total attempts. Strict success rate uses all attempted tasks.

Report all-file and implementation-file metrics separately once real labels exist.
Report corpus-level lexical performance and post-retrieval candidate recall ceiling
separately; candidate misses must not disappear from gold denominators.

## Timing and economics

Define every timing boundary. CPU fixture wall_ms measures ranking, prediction
validation and raw serialization per task;
file I/O, gold join, evaluation and process startup are excluded. It is not end-to-end
agent latency. Model experiments must record preparation, generation, router and
fallback stages and total latency separately. Allocated GPU time is the reservation
boundary, not an inferred utilization counter. For a CPU-only run GPU-seconds is
known zero, but CPU cost is unknown unless measured with an explicit pricing model.

Total cost includes every attempt, failure, retry, fallback and shared overhead
allocation. Missing cost means aggregate cost and CPS are null, with a reason.
Zero successful tasks also makes CPS null. Training cost is separate, with explicit
amortized views. Tokens do not apply to lexical inference and remain null.

## Frozen evaluation

Train/dev exclude all final-set overlaps; Verified cannot be used for iterative
prompt, adapter or threshold tuning. Store pinned dataset revision, task-ID/split
hashes, base commits, retrieval/config and label-policy hashes. Run paired treatments
on identical IDs. Freeze thresholds/statistical rules before final execution.
