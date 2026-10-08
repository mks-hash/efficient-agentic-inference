# Candidate scores on fresh validation — campaign contract v2

Prepared 2026-10-07. Validation inference NOT_RUN; paid execution NOT_AUTHORIZED.
[ADR 0009](../../decisions/0009-score-vector-ranking.md).
[Machine-readable contract](../../configs/score-ranking-validation-v2.json).

## Question and frozen population

Does a complete candidate-score recipe improve all-attempt localization quality
over candidate-constrained path generation? This changes the system prompt,
output representation and deterministic ranking rule together. It cannot isolate
the causal effect of uniqueness. The previous reliability campaign is exposed;
its small-model quality gain was zero. No training experiment is justified yet.

Use all 30 IDs/base commits in [validation-v2](../../splits/validation-v2.json),
SHA-256 `ec782a79b046dff8731f3d5570aebd647a5bd47eaf449ebd36dc884d33fe4635`.
Selection is repo-round-robin-sha256-v1, seed `eai-validation-v2`, reading only
allowlisted issue metadata. Exclude dev-v1, dev-v2, validation-v1 and Verified IDs
and normalized same-repository issue equivalents. No selection by patches,
retrieval ceiling, difficulty, preparation success or model outcomes; no replacements.
Two independent freezes have identical bytes. The allocation is eight pvlib,
eight pydicom, seven astroid and seven sqlfluff issues. Only four previously seen
repositories remain eligible. This is new-issue validation within seen repositories;
four blocks limit statistical confidence. Near duplicates and pretraining
contamination remain unproven. Verified stays reserved. Future training excludes
all frozen evaluation populations and their equivalents.

## Four recipes and exact mapping

| Arm | Model artifact | Prompt / generation policy |
| --- | --- | --- |
| S-paths | Pinned 4B Instruct Q4_K_M | localization-v1 / candidate-json-array-v1 |
| S-scores | Same 4B | candidate-scores-v1 / candidate-score-vector-v1 |
| G-paths | Pinned 14B Q4_K_M, native non-thinking | localization-v1 / candidate-json-array-v1 |
| G-scores | Same 14B | candidate-scores-v1 / candidate-score-vector-v1 |

Reuse the pinned backend/model artifacts from the previous campaign. Each arm
gets exactly the same canonical user message: full issue and unchanged
`bm25-top20-prefix1200-v1` evidence, up to twenty candidates sorted by path.
The system prompts and therefore full native token IDs differ across recipes;
record their token/resource overhead. No gold or resolution metadata enters
messages, schema, candidate order or mapping. Localization-v2, artifact schema
2.0.0 and accounting v1 stay unchanged.

The score schema permits exactly N integers, one per candidate in that order,
each drawn from the finite enum 0..100. For N=0 only `[]` is valid. Scores are
ordinal relevance estimates, not probabilities. Zero excludes a candidate.
Sort positive entries by descending score, break ties by lexicographic path,
then take at most ten. A complete all-zero vector yields an empty ranking.
The fixed rule is `positive-score-desc-path-asc-top10-v1`. There is no learned
threshold, normalization, secondary retrieval or adaptive tie-breaking.

Wrong length, booleans, floats (including 100.0), strings, null, out-of-range
values, path arrays, trailing text, truncation or failed native provenance remain
invalid. Repeated numeric scores are legitimate ties; candidate positions are
unique. This is the declared inference representation, not a repair of historical
answers. The path-array parser still rejects duplicate/unknown paths. Neither
parser nor evaluator rescues failures; all failed attempts score zero.

Inspect the pinned converter locally before execution:
[limitations](https://github.com/ggml-org/llama.cpp/blob/7049ff0cbeb1f5ead231de4522af6b75d8d773c0/grammars/README.md),
[implementation](https://github.com/ggml-org/llama.cpp/blob/7049ff0cbeb1f5ead231de4522af6b75d8d773c0/common/json-schema-to-grammar.cpp).
`uniqueItems` is unsupported. Use fixed-length arrays and primitive enums,
then verify effective eager grammar and strict native outputs. No backend upgrade.

## Preparation and execution gates

1. Freeze this protocol, ADR, split, four configs, prompts, parser/mapping,
   selection, labeler, evaluator and analysis source bytes before reconstruction.
   `tools/freeze-score-ranking.py` preserves them in an ignored immutable bundle.
2. Independent CPU fixtures cover integer strictness, wrong length, zero/all-zero,
   ties, empty/twenty candidate boundaries, tampered binding and native stop rules.
   Preserve all attempts. Run an isolated short synthetic 4B score probe plus a
   historical path probe: verify user-message identity, expected system difference,
   exact native counters/decoding/EOS, binding/schema hashes and eager grammar.
   These prove implementation only; no synthetic quality claim.
3. Reconstruct repositories at exact base commits and labels separately with the
   existing snapshot coordinator. Rebuild packets independently and compare bytes.
   Preserve failures/IDs; do not inspect validation quality or send labels upstream.
4. On a separately authorized host, verify pinned weights/build/template/full
   offload and gold-free namespace. Both models must pass score grammar/native
   probes, including empty/twenty/escaped-path boundaries. Run one old dev-v1
   issue per model/recipe only as a technical trace check, without tuning to its
   answer. Freeze exact configs and code archive for all four arms before any
   validation generation. CPU 4B evidence cannot satisfy GPU/14B gates.

Fixed serial order: S-paths, S-scores, G-scores, G-paths; a fresh server per arm,
one resident model, one slot, four threads. Opposite within-model order does not
remove cache/order confounding. Follow frozen task order. Native template,
16,384 context tokens, output limit 512, greedy temperature 0, seed 0, one attempt,
no prompt cache, retries or repair. G keeps native thinking disabled and verified
closed-think suffix, server reasoning off. Startup 180s, per task 120s, per arm
1,800s. A separate session cap/cleanup reserve takes precedence. Interrupted or
unattempted instances remain failures. The plan has 120 research slots; historic
predictions cannot substitute for fresh controls.

## Frozen analysis and economics

Open gold for evaluation only after all four arms and transport checks complete.
Report all 30 instances per arm: Recall@1/3/5/10, Strict Success@5, candidate
ceiling, validity/failures, token counts, p50/p95 latency, setup/load/lifecycle.
Require exact paired candidate lists/checksums, input IDs and gold identity.
Unknown labels block complete primary aggregates. Raw score diagnostics include
zero counts, positive-score ties, output length, ranking length and top-5 tie
boundary frequency; never tune the recipe from these diagnostics on this set.

Primary: S-scores minus S-paths mean Recall@5. A material signal requires:

- gain at least 0.05;
- strict success and valid prediction counts not lower;
- paired repository-block 95% interval lower bound strictly above zero;
- all independent technical/isolation/provenance gates PASS.

Reuse 5,000 repository-block resamples, seed 20261006, nearest-rank percentiles,
with paired tasks preserved. Four repository blocks provide limited uncertainty
estimation. Failure is negative/inconclusive evidence, not population equivalence.
Report validity discordance in both directions. G-scores minus G-paths and G gain
minus S gain are secondary exploratory estimates; do not promote a secondary
winner or selected valid-only subgroup to a primary finding.

Use accounting v1; include schema preparation, grammar, score prompt/output tokens,
mapping CPU, downloads, setup, failed attempts, transfers and cleanup. Report
actual campaign spending separately from explicit per-treatment deployment
scenarios. Missing invoice components, active GPU time and full CPS remain null.
Ties impose a path-order prior; full-prompt length, output length and model families
also differ. No uniqueness-only, calibration, model-size, generalization, training
or cost-saving claim follows from quality alone.

Retain every raw response, SSE/token trace, schema/binding/grammar/hash, error and
source/config identity in ignored artifacts; compact report exports are separate.
Collect and checksum artifacts before deleting any newly authorized VM/disk.
Preparation does not authorize paid resources, validation inference, new model
downloads, training or publication. A concrete session proposal follows CPU gates.
