# Reproducibility and evidence

Each run uses an immutable manifest conforming to schemas/v1/experiment.schema.json.
Each prediction uses schemas/v1/result.schema.json. Record UTC timestamps; human
planning dates use the project's Europe/Moscow timezone. Do not overwrite run
directories. Corrections create a new run with an explanation and parent ID.

Use JSONL per-task results and raw events initially. Parquet is a later typed export;
never claim it exists until an implementation and validation exist. SHA-256 hashes
identify task/gold bytes, configs, rendered prompts, token IDs and artifacts. A
dataset file hash does not replace pinned upstream provenance or split membership.

Git identity is commit + dirty state. A dirty run additionally needs a source-tree
snapshot/checksum; a commit alone is insufficient. Model identities include exact
model, tokenizer and template revisions. Non-model baselines have model=null and
must explicitly state why model-specific gates are UNSUPPORTED.

The CPU runner's source checksum covers pyproject.toml, uv.lock and regular files
under src/, schemas/, tests/, examples/ and docs/, excluding bytecode. Sorted relative
paths and each file's SHA-256 are combined with NUL separators. This detects local
implementation changes; retain the matching source checkout to reproduce a dirty
run, since a checksum alone cannot recover its bytes.

| Gate | What PASS establishes |
| --- | --- |
| G0 Identity | Pinned source/data/model identities |
| G1 Render | Deterministic canonical input and rendering |
| G2 Tokens | Exact model input/output token provenance |
| G3 Output | Strict classification, retained raw failures |
| G4 Resource fit | Successful measured load/generation on stated hardware |
| G5 Useful localization | Useful outputs on untouched pilot data |
| G6 Trainability | Reproducible adaptation run |
| G7 Frozen evaluation | Frozen data/evaluator executed as declared |
| G8 Economics | Complete quality, timing and cost accounting |
| G9 Generalization | Independently held-out repo/time/family evidence |
| G10 Systems | Separate serving/concurrency/composition contract |

Each gate is PASS, FAIL, NOT_RUN, UNKNOWN or UNSUPPORTED, with reasons. Software
fixture success does not pass useful-task, frozen-evaluation or economics gates.
Separate unsupported measurement from missing evidence and actual failure.

Publish artifact checksums, sample counts, failure counts, raw result provenance,
commands and environment. Retain negative outcomes. A partial run remains partial;
interrupted jobs cannot silently omit costly failed tasks.

Normal CI is CPU-only. Model downloads, GPU tests, paid runs and final evaluation
are explicit campaigns, independently authorized and recorded.
