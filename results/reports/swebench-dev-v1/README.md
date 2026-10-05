# SWE-bench dev-v1 — lexical localization pilot

Date: 2026-10-06. Method: lexical-bm25-v1. Contract: localization-v2.
This is a 12-task development pilot from six repositories, not a final evaluation
or a model comparison. No LLM, training or GPU was used.

## Population and results

Selected: 12 of 225 pinned dev instances; prepared: 12;
failed preparation: 0; failed prediction: 0;
unknown/empty gold: 0/0. Two tasks per repository, selected before evaluation by
repo-round-robin-sha256-v1 with seed eai-dev-v1. No substitutions after preparation.

| Measure | Value |
| --- | ---: |
| Recall@1 | 0.250000 |
| Recall@3 | 0.375000 |
| Recall@5 | 0.541667 |
| Recall@10 | 0.708333 |
| Candidate recall ceiling | 1.000000 |
| Conditional Recall@5 | 0.541667 |
| MRR, retained top 10 | 0.444444 |
| Strict Success@5 | 6/12 |
| Ranking wall p50 | 74.642 ms |
| Ranking wall p95 | 152.157 ms |
| Observed ranking CPU time, all tasks | 944.039 ms |
| GPU-seconds | 0 |
| Monetary cost / cost per success | unknown / unknown |

Quality is macro-averaged over 12 nonempty-gold tasks. All gold paths in this
particular pilot are implementation Python files already in the candidate corpus;
all-file and implementation-only metrics coincide. Conditional recall has 12
eligible tasks. Add/rename/delete/binary/empty cases are covered by independent
software fixtures, not inferred as prevalent from this pilot.

BM25 ranks every eligible base-tree Python file using its path and full source;
k1=1.2, b=0.75, unique issue terms, lexicographic path tie-break, retained top 10.
No ranker parameters or candidate policy were tuned against these outcomes.
Timing includes ranking/validation/raw serialization, excludes acquisition,
export, candidate preparation, I/O, process startup and evaluation; timing task
count is 12. These times cannot establish total-system economic savings.

## Evidence

The clean code commit used was
[`0edd9e6`](https://github.com/mks-hash/efficient-agentic-inference/tree/0edd9e666bac8306f658efb1c1390b5f0f06464e).
Builder Python 3.12.14, pyarrow 23.0.1,
git version 2.56.0; isolated predictor Python 3.14.7.
CPU: Intel(R) Core(TM) i5-7600 CPU @ 3.50GHz.

Local audit PASS: identical snapshots/inputs/labels and 27 deterministic artifacts
across two fresh-directory builds; 17698
regular-file hashes checked across both builds; all 12 solution patches apply to
exported base trees. Forbidden-field mutation preserved inputs, candidates,
order and semantic predictions. Gold mutation preserved predictions and changed
metrics. Repeated evaluation was identical. All v2 record schemas validated.

Bubblewrap probe and prediction execute in the same namespace/mount view. The
host project, evaluation code/data and Git history/cache are absent; network
namespace is separate, IPv4 route count zero and external connection fails.
The prediction sources are the four explicitly checksummed inference modules.

All 500 Verified IDs are reserved; dev/final ID intersection and normalized
same-repository issue overlap are empty. No final labels or predictions were built.

Independent-host reproduction is pending the manual GitHub CPU workflow. CPU CI
passed on Python 3.11 and 3.14; CI fixture success is separate from research evidence.

## Reproduce and inspect

Follow [the pinned-source rebuild and isolated audit recipe](../../../docs/reproducibility.md).
The manual `SWE-bench CPU reproduction` workflow rebuilds from the source URLs
and compares snapshot, input, gold and semantic prediction hashes to this reference.

- [Source pins](../../../configs/swebench-sources-v1.json)
- [Frozen dev membership](../../../splits/dev-v1.json)
- [Machine summary](summary.json), [per-task metrics](metrics.jsonl)
- [Saved predictions](predictions.jsonl), [inference manifest](manifest.json)
- [Snapshot manifest](snapshot.json), [leakage audit](audit.json)
- [Artifact checksums](checksums.json), [OS isolation probe](isolation.json)

Saved predictions contain ranked/candidate paths and measurements, without issue
text, repository source, gold patches or gold file lists. Original datasets,
Git objects and exported trees remain local and are reproducible from pinned sources.

## Limits

Small dev sample, no confidence interval or population-wide quality claim.
Gold files represent one accepted patch, not every possible valid repair.
Exact overlap checks do not prove absence of near duplicates or pretraining
contamination. No temporal test, model comparison, downstream repair result,
priced economics or specialization evidence exists yet. Independent-host results
must be recorded separately from the local audit.
