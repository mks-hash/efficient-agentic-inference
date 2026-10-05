# Untuned small-model baseline — dev-v2

Date: 2026-10-06. Dataset/context protocol frozen before new quality measurements.
Execution requires a separately pinned and validated model/backend configuration.

## Population and comparisons

60 instances in [dev-v2](../../splits/dev-v2.json), seed `eai-dev-v2`, disjoint
from dev-v1 IDs and normalized same-repository issues and from reserved Verified
overlaps. Source revision and selection algorithm are retained from the pilot.
Allocation: marshmallow 7, pvlib 11, pydicom 11, astroid 11, pyvista 10, sqlfluff 10.
The uneven allocation follows available repository capacity, not labels or outcomes.

| Treatment | Available evidence | Purpose |
| --- | --- | --- |
| lexical-full | All eligible base-tree Python paths and full source | Released algorithm on new development instances |
| lexical-context | Fixed context packet, BM25 recomputed on its paths/excerpts | Matched evidence comparator |
| untuned-context | Exactly the same packet through the native model chat template | Incremental model contribution |

Profile `bm25-top20-prefix1200-v1`: select at most 20 candidates by full-corpus
lexical ranking, then sort them by path. Show the first 1,200 Unicode characters
of each file and the full unchanged issue. No retrieval scores/ranks enter the
model prompt. All treatments retain preparation failures. File availability in
a packet is distinct from whether its prefix contains useful explanatory code.

The matched lexical treatment recomputes document statistics on exactly the
packet, so it can differ from the full-corpus ranking. Report both comparisons;
do not attribute context representation changes to model capability.

## Model execution gate

One untuned instruct model; no training or fallback. Freeze original model revision,
quantized artifact revision/file SHA-256 (if applicable), tokenizer/template identity,
backend commit/binary checksum, hardware, context capacity and execution parameters.
Quantized results must name the quantization; they are not an unquantized control.

Use [localization-v1 prompt](../../configs/prompts/localization-v1.txt). The user
message is canonical JSON containing `issue` and `candidates`, preserving packet
order and excerpt text. Native-template rendering and tokenization must be saved.
Greedy decoding, seed 0, output budget 512 tokens, one attempt per task. Initial
context capacity proposal: 16,384 tokens. Freeze its actual value after resource
checks on dev-v1/synthetic inputs, before inspecting dev-v2 model outcomes.

Never silently truncate input. Context overflow, token/output budget exhaustion,
malformed JSON, duplicate/unknown paths and backend failures remain failures;
preserve response text, token IDs and reason. No output repair or second attempt.
API/mock tests establish software behavior only. Model execution and physical gold
isolation must each have actual evidence before marking their gates PASS.

## Quality and analysis

Reuse localization-v2 gold policy and evaluator without revising denominators.
Primary comparison: paired macro Recall@5, untuned-context minus lexical-context.
Also report Strict Success@5, all-file and implementation-only metrics, full versus
context candidate ceilings, conditional recall, valid/failed/overflow counts and
the total selected population. A successful localization is coverage of reference
patch files, not successful issue repair.

A promising development finding requires observed Recall@5 gain at least 0.05,
no lower strict success rate and a paired repository-cluster bootstrap 95% interval
whose lower bound is above zero. Use 5,000 resamples, seed 20261006; sample the six
repository blocks with replacement, preserving paired task outcomes within each
block. This is a development decision rule with only six represented repositories,
not population-wide confirmation. Report uncertainty even when the rule fails.
Never change the threshold or packet after seeing these outcomes.

Failure of this rule yields a negative/inconclusive finding. Failure analysis may
motivate a new versioned treatment on a newly declared exposed development set.
Training is not automatically justified by a weak small model; compare a stronger
generalist on the same evidence before claiming a specialization opportunity.

## Resource and monetary accounting

Report these phases separately: dataset acquisition/export, context construction,
model load/warmup, and per-request render/tokenization/generation/validation.
Local process CPU time must identify which process was measured; client CPU time
cannot stand in for server compute. GPU reservation time, utilization and device
memory are different observations. Retain actual tokens for failed attempts.

Context preparation is shared work but must be charged once to each independently
executed treatment when estimating deployment cost. Include model setup under an
explicit workload/amortization assumption. Historical ranking-only timings remain
attributed to their original scope. Unknown prices remain null; scenario prices
must be labeled assumptions. No GPU/cloud spend is authorized by this document.

## Reproduction commands

```bash
uv sync --locked --extra data
uv run eai-snapshot freeze --config configs/swebench-sources-v1.json \
  --upstream data/local/upstream --output data/local/new-splits/dev-v2-copy \
  --count 60 --seed eai-dev-v2 --name dev-v2 --exclude-splits splits/dev-v1.json
uv run eai-snapshot build --config configs/swebench-sources-v1.json \
  --upstream data/local/upstream --split splits/dev-v2.json \
  --output data/local/snapshots/dev-v2-copy --cache data/local/git-cache
tools/predict-isolated.sh data/local/snapshots/dev-v2-copy/inference_inputs/tasks.jsonl \
  results/runs/dev-v2-context-copy context
tools/predict-isolated.sh results/runs/dev-v2-context-copy/tasks.jsonl \
  results/runs/dev-v2-lexical-context-copy
```

Evaluate only after the saved prediction records are complete, using the separate
snapshot gold. All commands require fresh output directories. Full-corpus lexical
prediction uses the original snapshot inference input. Source data/exports, prompts
with source excerpts and token logs remain local and ignored.
