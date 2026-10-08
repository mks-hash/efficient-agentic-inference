# Reproducibility and evidence

The active benchmark is [localization-v2](benchmark-localization-v2.md), with separate
[artifact schemas](../schemas/v2/README.md) and frozen [split manifests](../splits/README.md).
v1 records retain their original meaning; the combined baseline command is retired.

## CPU verification

Use Python 3.11+ and uv from the repository root:

```bash
uv sync --locked --extra data
uv run ruff check .
uv run ruff format --check .
uv run python -m unittest discover -s tests -v
uv run eai-predict --synthetic --inputs examples/localization-v2/tasks.jsonl \
  --output results/runs/fixture-predictions
uv run eai-evaluate --predictions results/runs/fixture-predictions \
  --gold examples/localization-v2/gold.jsonl --output results/runs/fixture-evaluation
```

Without the optional data extra, tiny Parquet contract tests are explicitly skipped.
CI installs it and runs the complete CPU suite on Python 3.11 and 3.14. Synthetic
fixtures establish software behavior, not research quality or model support.

The new [untuned-dev-v2 preparation protocol](experiments/untuned-dev-v2.md) freezes
60 new development instances and introduces `eai-context`. The isolation wrapper
accepts an optional third argument `context`; its default remains `predict`.
Context construction mounts only its four inference source modules and canonical
inputs, with the same filesystem/network boundary. Context tasks still use the
v2 inference schema; context provenance uses its own v1 records. Model execution
uses a separate model/backend isolation and resource check. The
[untuned L4 comparison](../results/reports/untuned-dev-v2-l4/README.md) retains
measured identities, all failures, native counters and physical isolation evidence.
See the [CUDA runbook](experiments/cuda-execution.md) for reproduction; paid
execution always requires its own budget/authorization.

## Rebuild the pinned SWE-bench pilot

The source download and first Git-object fetch require network access. All subsequent
snapshot rebuilding can run offline with the verified source files and object cache.
No repository code is executed and no Docker or GPU is needed for localization.

```bash
uv run eai-snapshot fetch --config configs/swebench-sources-v1.json \
  --output data/local/upstream
uv run eai-snapshot build --config configs/swebench-sources-v1.json \
  --upstream data/local/upstream --split splits/dev-v1.json \
  --output data/local/snapshots/reproduction-a --cache data/local/git-cache
uv run eai-snapshot build --config configs/swebench-sources-v1.json \
  --upstream data/local/upstream --split splits/dev-v1.json \
  --output data/local/snapshots/reproduction-b --cache data/local/git-cache --offline
```

For physical isolation, Linux and bubblewrap are required. The wrapper mounts only
private inference inputs, four source modules, stdlib runtime and fresh output staging;
network and process namespaces are separate. Gold, evaluation code, Git history/cache
and the project checkout are physically absent. The probe's result is checksummed
alongside predictions. If this OS boundary is unavailable, report it as NOT_RUN;
a Python network mock does not establish physical isolation.

The manually dispatched `SWE-bench CPU reproduction` GitHub workflow downloads
the same pinned sources, reconstructs two fresh trees and compares deterministic
hashes and quality with the published local reference. On its hosted Linux runner
it uses sudo only for the bubblewrap wrapper (`--sudo-isolation`), retaining an
unprivileged builder/evaluator. It is separate from ordinary pull-request CI.

```bash
tools/predict-isolated.sh data/local/snapshots/reproduction-a/inference_inputs/tasks.jsonl \
  results/runs/reproduction-predictions
uv run eai-evaluate --predictions results/runs/reproduction-predictions \
  --gold data/local/snapshots/reproduction-a/gold/labels.jsonl \
  --output results/runs/reproduction-evaluation
uv run python tools/audit_snapshot.py \
  --snapshot data/local/snapshots/reproduction-a \
  --rebuild data/local/snapshots/reproduction-b --upstream data/local/upstream \
  --output results/runs/reproduction-audit
```

The audit compares deterministic snapshots, every regular exported file, tree and
candidate manifests, inputs and labels; validates schemas; checks base patch
applicability and split overlap; mutates forbidden upstream fields and gold; runs
three isolated prediction processes and repeats evaluation. Semantic predictions
exclude measurements. Byte-identical labels/quality do not imply identical timings
across hosts. An independently operated second machine is separate evidence.

The selection command is for creating a new preregistered split, not silently
refreshing the published pilot:

```bash
uv run eai-snapshot freeze --config configs/swebench-sources-v1.json \
  --upstream data/local/upstream --output data/local/new-splits --count 12 --seed eai-dev-v1
```

## Immutable artifacts and provenance

Use fresh output directories; programs reject overwrites. Predictions are saved
and checksummed before evaluation. Retain failed preparation, malformed outputs
and runtime failures. Each selected ID must have both a preparation and label
status. Unknown labels block a complete primary quality claim; unknown monetary
cost and zero success block a numeric CPS claim. Corrections create a new run.

Source provenance is pinned dataset revisions, source bytes and split membership;
Git commit/tree/blob identities and exported file hashes; versioned candidate/label
policies; exact predictor source hashes, interpreter/platform and config. Reports
also name the clean code commit used and retain per-task outputs and checksums.
Dirty runs require the matching source snapshot; a checksum cannot recover bytes.
No model experiment may omit exact model/tokenizer/template identities or raw
input/output token provenance when making model or performance claims.

Ranking wall/CPU time excludes preparation, process startup, file I/O and evaluation.
Failed preparation has no ranking timing. Report task counts and timing boundaries;
setup and resource reservation costs must be added for total-system economics.
For this CPU baseline GPU time is known zero, tokens inapplicable, CPU cost unpriced.

## Independent evidence gates

Each dimension is PASS, FAIL, NOT_RUN, UNKNOWN or UNSUPPORTED with a reason.
A fixture check does not establish useful model behavior or efficiency.

| Gate | What PASS establishes |
| --- | --- |
| G0 Identity | Pinned source/data/model identities |
| G1 Render | Deterministic canonical input and rendering |
| G2 Tokens | Exact model input/output token provenance |
| G3 Output | Strict classification, retained raw failures |
| G4 Resource fit | Measured model load/generation on declared hardware |
| G5 Useful localization | Useful outputs on untouched pilot data |
| G6 Trainability | Reproducible adaptation run |
| G7 Frozen evaluation | Frozen data/evaluator executed as declared |
| G8 Economics | Complete quality, timing and cost accounting |
| G9 Generalization | Independently held-out repo/time/family evidence |
| G10 Systems | Separate serving/concurrency/composition contract |

Lexical results cannot promote any model gate. The dev pilot is not final evaluation.
Model downloads, paid runs, GPU tests and final evaluation are separate campaigns.

## Matched generalist preparation

The [next protocol](experiments/generalist-dev-v2.md) and
[preparation checks](experiments/generalist-preparation-checks.json) record an
opt-in non-thinking renderer and a reserved validation population. Actual 14B
weights, native API, resource fit and quality remain NOT_RUN. The new cost ledger
is a separate post-evaluation namespace; never mount it into inference.

## Completed matched larger-candidate comparison

The [report](../results/reports/generalist-dev-v2-l4/README.md) records two fresh
60-task runs on the same L4, complete configuration/native trace hashes, paired
analysis, phase accounting and confirmed VM/disk deletion. Original raw output
and source-bearing traces are retained in the ignored archive; review predictions
redact raw_output with original hashes recorded. Fresh evaluation of those exports
produces identical per-task metrics. The 4B replication matches every historical
ranked-path/disposition/failure record. The 14B candidate has no positive gap.

Preparation-only statuses above remain historical; they are not the current model
fit/quality state. Contract v2, schemas and previously frozen report bytes remain
unchanged. Unknown costs stay unknown in actual and complete scenario CPS.

## Reliability validation preparation

The [campaign contract](experiments/reliability-validation-v1.md) freezes four new
base configs and an output-constraint policy while retaining localization-v2.
[Preparation checks](experiments/reliability-preparation-checks.json) record two
synthetic native probes, two matching validation reconstructions, private artifact
hashes and the failed initial preparation attempts. Validation quality is NOT_RUN.

Before constructing new validation inputs, preserve an immutable preparation bundle:

```bash
uv run python tools/freeze-reliability.py --output .develop/reliability-freeze-new
```

After independently authorized inference and local evaluation of all four arms,
arrange each arm's immutable `predictions/` and `evaluation/` directories under
one root and analyze them without regenerating predictions:

```bash
uv run python tools/analyze-reliability.py \
  --runs /path/to/four-arm-root --output /path/to/fresh-comparison
```

The analyzer checks artifact hashes, frozen membership, model/prompt/decoding,
candidate/input/gold identities and prediction dispositions. It reports a numerical
signal separately from technical/provenance gates, which metrics cannot establish.
Unknown accounting remains null. This command does not authorize GPU execution.

## Completed reliability validation

The [four-arm report](../results/reports/reliability-validation-v1-l4/README.md)
records 80 validation attempts and 32 separate technical requests on one L4.
Both modes have identical rendered prompt and native input IDs for all 20
issues within each model. Twelve same-backend replay pairs match native input/
output IDs, raw response, paths and dispositions. Those checks establish execution,
not additional quality samples. All four exact configs froze before validation;
evaluation used local-only gold after complete collection.

Execution identity is the immutable selected-source archive and its source hashes;
the dirty base revision alone is insufficient. The campaign contract, primary
rule, evaluator and earlier report bytes remain unchanged. Final transport verified
980 checksum entries. Original raw traces remain private; the source-free report
exports were independently re-evaluated to identical per-task metrics. VM/disk
absence and existing-resource preservation are recorded. Actual cost and active
GPU-seconds remain unknown. Validation-v1 is now exposed; Verified is untouched.

## Prepared score-ranking validation

The [score-ranking protocol](experiments/score-ranking-validation-v2.md) reserves
30 fresh issues. [Preparation checks](experiments/score-ranking-preparation-checks.json)
record 67 CPU contracts, seven isolated synthetic native requests and a same-host
online/offline snapshot rebuild. Complete inference packet bytes match; provenance
matches with only measured cpu_ms/wall_ms excluded. Both original timing journals
remain unchanged. No validation model inference or quality evaluation has run.

Freeze the current preparation to a fresh ignored directory, then reconstruct
with the existing snapshot commands, replacing the split with validation-v2.
Keep gold separate and defer quality evaluation until all four authorized arms
have been collected. Never overwrite an existing snapshot or freeze.

```bash
uv run python tools/freeze-score-ranking.py --output .develop/score-freeze-new
```

To reproduce the short 4B synthetic score-format check with the already acquired,
pinned weights and CPU backend, use [fabricated inputs](../examples/score-ranking-v1/README.md):

```bash
uv run python tools/configure-cpu-run.py \
  --base-config configs/score-ranking-validation-v2/S-scores.json \
  --binary .develop/backends/llama.cpp/build-cpu/bin/llama-server \
  --build-dir .develop/backends/llama.cpp/build-cpu \
  --inputs examples/score-ranking-v1/tasks.jsonl \
  --campaign score-synthetic-reproduction --run-budget-s 300 \
  --task-timeout-s 120 --synthetic --device cpu \
  --output .develop/score-synthetic-new.json
bash tools/llama-isolated.sh examples/score-ranking-v1/tasks.jsonl \
  .develop/score-synthetic-new.json models/Qwen3-4B-Instruct-2507-Q4_K_M.gguf \
  .develop/backends/llama.cpp/build-cpu/bin/llama-server \
  configs/prompts/candidate-scores-v1.txt .develop/score-synthetic-new-run
```

The backend build/weights and native binding/schema/counters/EOS must be checked;
format acceptance says nothing about localization quality. For the matched path
probe use S-paths and localization-v1; for historical compatibility use the
separate historical input unchanged. These local CPU commands authorize no paid
resources or validation evaluation.

After a separately authorized complete four-arm run and unchanged evaluation,
place ARM/predictions and ARM/evaluation under one root:

```bash
uv run python tools/analyze-score-ranking.py \
  --runs /path/to/four-arm-root --output /path/to/fresh-score-comparison
```

The analyzer verifies hashes, membership, prompt/model/decoding/constraint/mapping,
candidate/input/gold identities and dispositions. Retained valid score vectors
must map to the reported rankings. Tie/zero diagnostics are selected diagnostics;
primary quality includes every attempt. Numerical signals never substitute for
independent technical/provenance gates or actual monetary accounting.
