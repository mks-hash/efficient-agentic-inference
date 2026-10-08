# Output reliability on fresh validation — campaign contract v1

Prepared: 2026-10-07. Research inference NOT_RUN; paid execution NOT_AUTHORIZED.
[ADR 0007](../../decisions/0007-constrained-output-validation.md).
Machine-readable rules: [campaign config](../../configs/reliability-validation-v1.json).

## Research question and exposure

Does generation-time restriction to JSON and supplied candidate paths improve
all-attempt localization quality without changing prompt, evidence or evaluation?
The prior 60-task comparison is exposed development evidence. Its both-valid
subgroup motivated this question but is selected post hoc; it cannot establish
an underlying 14B capability advantage.

Use exactly the 20 IDs/base commits in [validation-v1](../../splits/validation-v1.json),
SHA-256 `fcf962e4e37bcfdf9243739c4930dbb0eedea41f90080b3cd6542381a5362121`.
Exclude frozen dev populations, Verified and normalized equivalents using the
existing manifest. It is new-issue validation in the previously seen repositories, not
repository/time generalization. No task replacement, prompt search or selection
by patch complexity, candidate ceiling, prediction or preparation success.
The fixed membership contains four issues in each of five previously seen
repositories; marshmallow has no remaining eligible issues. This count corrects
the initial preparation wording about six repositories without changing membership.
Verified remains untouched. After this campaign the 20 issues are exposed and
cannot serve as fresh validation for later tuned recipes.

## Four matched arms

| Arm | Model | Generation constraint |
| --- | --- | --- |
| S-free | Pinned Qwen3-4B-Instruct-2507 Q4_K_M | Historical unconstrained request |
| S-constrained | Same S artifact/template | candidate-json-array-v1 |
| G-free | Pinned Qwen3-14B Q4_K_M, native non-thinking | Historical unconstrained request |
| G-constrained | Same G artifact/template | candidate-json-array-v1 |

Existing model/GGUF/backend revisions and prompt bytes are copied into four new
base configs; old configs/results/tags are immutable. For each issue use the
unchanged `bm25-top20-prefix1200-v1` packet, sorted paths, full issue, native template,
16,384-token capacity, output limit 512, temperature 0, seed 0, one attempt,
no cache_prompt, one slot and four threads. G keeps `enable_thinking=false`,
verified closed-think suffix and server reasoning off. No training or retries.

The only completion-request change is `json_schema` in constrained arms. It permits
an array of 0–10 strings, each drawn from the input candidate paths, in arbitrary
rank order. No scores or labels enter that schema. Do not inject it into chat
messages. The empty-candidate schema permits only `[]`.

Uniqueness is deliberately **not** enforced by the schema: the pinned converter
does not support `uniqueItems`. Duplicates still fail the unchanged parser, as do
unknown paths, malformed JSON, extra text, more than ten paths, truncation or
incorrect native provenance. A valid empty answer is still unsuccessful for
nonempty gold. Do not repair outputs or relax the evaluator.

Source review uses the clean pinned backend `7049ff0cbeb1f5ead231de4522af6b75d8d773c0`:
[API](https://github.com/ggml-org/llama.cpp/blob/7049ff0cbeb1f5ead231de4522af6b75d8d773c0/tools/server/README.md),
[grammar limitations](https://github.com/ggml-org/llama.cpp/blob/7049ff0cbeb1f5ead231de4522af6b75d8d773c0/grammars/README.md),
[converter tests](https://github.com/ggml-org/llama.cpp/blob/7049ff0cbeb1f5ead231de4522af6b75d8d773c0/tests/test-json-schema-to-grammar.cpp).
Inspect local pinned source as well as documentation: unsupported schema keywords
can be silently ignored. No backend upgrade during this campaign.

## Preparation and freeze gates

1. Freeze this protocol, campaign rules, four base configs, prompt and split byte
   hashes before validation reconstruction. Preserve the local preparation bundle.
2. Test schema derivation on independent synthetic paths, escaping, empty candidates,
   unknown policy rejection, no-op free request, and unchanged strict failure rules.
   Gold/evaluator data must be absent from schema derivation.
3. Run short isolated synthetic CPU S-free/S-constrained probes. Verify identical
   rendered prompt and input token IDs; constrained response must report a nonempty
   eager grammar, and saved schema hash must match the request. No quality claim.
4. Reconstruct base repositories/labels in separate namespaces using the existing
   coordinator; rebuild packets and verify semantic/hash identity. Keep labels
   local and uninspected. Build/freeze four exact execution configs on the proposed
   host after synthetic/old dev-v1 gates (marshmallow-1810, pvlib-1165, pydicom-811).
   Invalid old-task model answers are recorded, not a prompt-tuning gate.
5. Before research verify weights, clean inference archive, backend/binary/template,
   full offload, native counters, schema/effective grammar, capacity, and physical
   isolation. Upload neither gold/evaluator nor upstream dataset/full repositories.

Local code may be dirty during preparation; record exact inference source hashes.
Research requires a clean committed inference identity or a documented immutable
archive of exact sources, frozen before generation. All four complete configurations
and input identities must freeze before any validation generation.

Fixed serial arm order: S-free, S-constrained, G-constrained, G-free. Opposite
within-model orders reduce a uniform direction bias but do not remove cache/order
confounding. Each arm has a fresh backend process; no simultaneous model residency.
Task order follows the frozen packet unchanged. Request timeout 120s, startup 180s,
arm budget 1,800s; an independently authorized session cap and cleanup reserve take
precedence. Preserve unattempted instances as failures; never replace an incomplete
fresh control with historical predictions. Any failed technical identity/isolation
gate blocks primary claims, even if remaining artifacts are available diagnostically.

## Frozen analysis and interpretation

All 20 instances per arm stay in quality and measured-resource denominators. Report
Recall@1/3/5/10, Strict Success@5, candidate ceiling, disposition/failure counts,
tokens, p50/p95 wall, load and lifecycle phases. Empty/unknown gold retains the v2
rules; unknown labels block complete primary aggregates. Compare exact paired IDs,
candidate lists/checksums and gold identity before calculating differences.

Primary comparison: **S-constrained minus S-free** mean Recall@5. A material
validation signal requires all of:

- Recall@5 gain at least 0.05;
- strict success count not lower;
- valid prediction count not lower;
- paired repository-block 95% interval lower bound above zero;
- all technical and immutable-provenance gates PASS.

Reuse 5,000 repository-block resamples, seed 20261006, nearest-rank percentiles.
Report validity discordance counts (free invalid/constrained valid and the reverse).
With only 20 issues/five repository blocks uncertainty can be wide. Failure of the
signal rule is inconclusive or negative evidence, not proof of equivalence.

G-constrained minus G-free and the difference between those two within-model
changes are secondary exploratory point estimates. Report their paired quality,
validity and resource changes without selecting a new primary winner. Cross-model
comparisons cannot identify parameter-count effects. Validity-conditioned results
are explicitly selected diagnostics; do not omit invalid answers from primary quality.

No outcome alone authorizes training, tuning this validation set, or a cost-saving
claim. Freeze a new population before refining recipes from these failures.

## Accounting, artifacts and authorization

Use accounting v1. Preserve separate actual spending for the whole campaign and
explicit deployment scenarios. Join provider usage/invoice evidence when available;
do not divide a pooled VM invoice into supposedly measured per-model cost. Record
shared setup, failed attempts, schema preparation/grammar request overhead, download,
load, warm requests, transfers and cleanup. Unknown active GPU time, missing charges,
external preparation and cost per success remain null.

Save every raw output/SSE/native token trace, derived schema/hash, effective grammar,
configuration, source identity and errors in ignored local artifacts. Keep source-free
report derivatives separate and verify transport checksums before VM/disk deletion.
The source-bearing raw environment must not be modified during the run.

Preparation approval does not supply a paid budget or authorize new VM creation.
Prepare a concrete one-session proposal after CPU gates, then obtain explicit budget
and run authorization. Publication follows its own user authorization. No new model
download, paid provisioning, validation inference or release is part of CPU preparation.
