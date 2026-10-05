# SWE-bench file localization — contract v2

Identifier: `localization-v2`. Artifact schema: `2.0.0`. Decision:
[ADR 0002](../decisions/0002-snapshot-labels-and-leakage-boundary.md).
The old v1 combined fixture artifacts retain their original meaning; no automatic
conversion of old results into research measurements is permitted.

## Three separate artifact types

- Inference: an allowlisted instance plus preparation disposition, tree and ordered
  candidate checksums. No upstream patch, hints, tests or evaluation fields.
- Prediction: ranked candidate paths, raw output, disposition, measurements and
  candidate identity. No gold labels or correctness metrics.
- Evaluation: solution-patch changes and label disposition, stored separately.

`predict` imports no labeler/evaluator and accepts no gold argument. `evaluate`
verifies saved prediction checksums before joining labels. It cannot regenerate or
repair predictions. Both programs refuse to overwrite output directories.

## Snapshot and selection

[Pinned source configuration](../configs/swebench-sources-v1.json) stores dataset
revisions, exact source file URLs and SHA-256 hashes. [Split manifests](../splits/)
freeze selected IDs, base commits, repository identities, issue fingerprints,
selection algorithm, source population and overlap exclusions. The first dev pilot
selects 12 instances by fixed-seed SHA-256 ranking within repository and sorted-repo
round-robin. Selection reads only instance_id, repo, base_commit, problem_statement.

Reserve all 500 Verified IDs. Check dev/final ID intersection and exact normalized
same-repository issue duplicates. This does not prove absence of near duplicates or
model pretraining contamination. Final labels/predictions are not produced during
this pilot. Training/validation split policies require a later frozen extension.

Export exact Git blobs from base_commit; verify commit, tree and blob IDs. Manifests
contain sorted path, size, mode, kind and content SHA-256. Git archive attributes
must not rewrite or hide files. Export regular files only; record symlinks without
following them and Git submodules without expanding them. Never execute repo code.

Candidate policy `python-full-corpus-v1`: regular `.py`, valid UTF-8 without NUL,
at most 1 MiB/file, full text and path, ordered lexicographically. Include tests;
do not filter generated files using gold. Manifest every skip reason. Candidate
builder accepts only the inference projection and the verified exported tree.

## Gold policy

`patch` is the solution patch, distinct from `test_patch`. All-file metrics refer
to solution-patch files, not all original PR changes. Git parses destination paths;
strict diff metadata identifies old paths and change kinds. Rename/delete/modify
use old/base paths; add/copy use new paths. Preserve mode-only and binary changes,
multi-file patches and unreachable new files. Never use test_patch as target gold.

Category policy: paths under test/tests/testing or basenames beginning test_ are
test files; remaining `.py` are implementation; other paths are non-code. Generated
files have no special exclusion. This is a coarse frozen classification, not a
semantic guarantee. Empty and unsupported patches have explicit dispositions.
Synthetic cases specify expected labels independently, including add/delete/rename,
quoted paths, binary, tests and mode-only changes. The audit dry-runs solution
patch applicability against each exported base tree without modifying it.

## Quality and denominators

K∈{1,3,5,10}; primary K=5. Recall@K = gold hits in unique top-K / all gold paths.
Precision@K = hits/K, including unfilled slots. MRR uses the first gold match in
the retained ranking (default top 10); reports must state this truncation.
Strict Success@K requires all nonempty gold paths in top K.

Candidate ceiling = accessible gold / all gold. Conditional Recall@K = hits /
accessible gold, undefined when none is accessible. Macro-average conditional
recall only across tasks with accessible gold and publish that count. It is a
diagnostic; primary recall retains unreachable gold and preparation failures.

Keep all selected instances in the population. Known-gold preparation/prediction
failures score zero recall/MRR and fail strict success. Empty gold has undefined
recall/MRR and cannot count as success. Macro recall averages nonempty known gold;
publish its denominator and the total selected count. Any unknown label makes a
complete primary aggregate undefined; known-label diagnostics are labeled separately.
Report all-file and implementation-only quality separately.

## Measurements and evidence

Per-task wall/CPU time covers ranking, validation and raw serialization. It excludes
data acquisition, tree export, candidate preparation, file I/O, gold joining and
evaluation. Failed preparation has no ranking latency; publish latency task count.
CPU times are process time; wall quantiles use nearest rank. GPU-seconds are known
zero for this CPU program. Tokens do not apply. Unpriced monetary cost and CPS are
null. Include all failure costs whenever measured; zero successes gives undefined
CPS. No total-system economics claim follows from ranking latency alone.

`tools/predict-isolated.sh` uses Linux bubblewrap to mount only the stdlib runtime,
four inference source modules, inputs and fresh output staging. Gold, evaluation
code, project checkout, Git history/cache and upstream datasets are absent. Network
and process namespaces are separate. An independent probe verifies project
invisibility, a separate network namespace, zero IPv4 routes and failed connection.
Ordinary non-isolated prediction is supported but does not establish OS isolation.

Audit invariants: deterministic rebuilt trees/manifests/inputs/labels; forbidden
source-field mutation leaves inputs, candidate set/order and predictions identical;
gold mutation changes only evaluation; repeated evaluation is identical; schemas
validate; dev/final split IDs are disjoint. Compare semantic predictions, excluding
measurements and machine/runtime metadata. Independent second-host reproduction
must be reported separately from a same-host fresh-directory rebuild.
