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
