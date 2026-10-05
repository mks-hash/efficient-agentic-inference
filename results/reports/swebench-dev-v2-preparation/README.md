# SWE-bench dev-v2 — preparation and lexical controls

Date: 2026-10-06. Code: `0bd75714686b365334936e7faa7e5211816d1540`.
60 new development issues across the same six repositories. No model was run.

## Quality

| Treatment | Recall@5 | Strict Success@5 | Candidate ceiling |
| --- | ---: | ---: | ---: |
| Lexical, full corpus | 0.552265 | 25/60 | 0.985450 |
| Lexical, matched context | 0.228326 | 8/60 | 0.783487 |
| Untuned model, matched context | NOT_RUN | NOT_RUN | Same packet intended |

All 60 tasks prepared/labeled, zero prediction failures and zero unknown labels.
All-file metrics above use localization-v2 denominators, retaining inaccessible
reference paths. Implementation-only metrics are in the saved summaries.
Strict success means file-set coverage of a reference patch, not successful repair.
No ranker parameter or context policy changed after these outcomes were observed.

The context profile selects up to 20 paths with the frozen full-corpus BM25 method,
then supplies the first 1,200 Unicode characters of each file in path order plus
the complete issue. Matched lexical recomputes BM25 on exactly that evidence.
The lower ceiling shows lost file availability; the prefix representation can
also lose useful code. A model improvement over this matched comparator alone
would not establish improvement over full-corpus lexical retrieval or economics.
The original profile stays frozen; future retrieval profiles are separate treatments.

## Evidence and identity

The two base reconstructions produced 123 identical deterministic artifacts;
88,638 regular-file hashes were checked across them. Patch applicability, v2
schema validation, forbidden-field and gold mutation invariants, repeated
full-corpus evaluation and filesystem/network isolation passed.
Context inputs and semantic context provenance matched across both reconstructions.
Both context construction and matched prediction ran with project/gold/evaluator
files and external networking absent. Linux bubblewrap probes are retained.
These are local rebuilds; no second-host dev-v2 reproduction has been run yet.

Selection uses the original pinned 225-task dev source, seed eai-dev-v2,
repository round-robin SHA-256, excluding dev-v1 IDs and normalized equivalent
issues before selection. Verified remains reserved. Allocation is 7/11/11/11/10/10
for marshmallow/pvlib/pydicom/astroid/pyvista/sqlfluff due to source capacity.
The released dev-v1 manifests remain byte-identical. This new scored development
population is now exposed; it is not an untouched evaluation or a new-repository test.

- [Population](../../../splits/dev-v2.json), [population checksum](../../../splits/dev-v2.sha256)
- [Protocol and accounting](../../../docs/experiments/untuned-dev-v2.md)
- [Decision](../../../decisions/0003-untuned-baseline-and-new-development-population.md)
- [Comparison](comparison.json), [snapshot](snapshot.json), [audit](audit.json)
- [Full summary](full-evaluation/summary.json), [context summary](context-evaluation/summary.json)
- [Context provenance](context-provenance.jsonl), [preparation measurements](context-a-manifest.json)
- [Context isolation probe](context-isolation.json), [checksums](SHA256SUMS)

Each prediction/evaluation subdirectory has its own original checksums. The bundle
contains metrics, predictions, candidate paths and hashes, without issue text,
repository source, gold patches, labels or source-bearing context packets.
Rebuild those private inputs with the protocol's pinned-source commands.

## Resource scope and next gate

CPU-only preparation and lexical controls. Monetary cost remains unknown.
Ranking latency excludes context preparation and other system overhead; phase
measurements are stored separately. CPU timings concern the measured process.
No GPU/model utilization, model-quality or economic gain claim is made.
38 software tests passed, including context ceiling loss and previous-population
exclusion. Model revisions and a GGUF candidate are pinned in the execution
proposal, with model/token/resource/isolation/quality gates explicitly NOT_RUN.
The next step is model resource-fit and format checks on dev-v1 or synthetic inputs,
then a single frozen model run on this dev-v2 context, with all failures retained.
