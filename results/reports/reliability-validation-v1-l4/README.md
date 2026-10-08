# Generation constraints on fresh localization validation

**20 issues / five seen repositories; four frozen arms, one attempt per task.**
Pinned Qwen3-4B-Instruct-2507 and Qwen3-14B Q4_K_M (non-thinking), the same
bounded repository evidence, prompt, greedy decoding and strict evaluator.
Constrained arms add a gold-blind candidate JSON schema during generation.

| Arm | Recall@5 | Strict@5 | Valid | Candidate ceiling | p50 / p95 request | Sampled peak GPU MiB |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| S-free | 0.633333 | 9/20 | 19/20 | 0.879167 | 3.068s / 4.485s | 4942 |
| S-constrained | 0.633333 | 9/20 | 19/20 | 0.879167 | 3.068s / 4.965s | 4942 |
| G-free | 0.595833 | 8/20 | 16/20 | 0.879167 | 12.146s / 14.448s | 11006 |
| G-constrained | 0.645833 | 9/20 | 17/20 | 0.879167 | 12.155s / 14.437s | 11006 |

Invalid outputs remain zero in all-attempt quality. Empty valid answers also
remain unsuccessful for nonempty gold. The schema allows at most ten supplied
paths but does not enforce uniqueness; duplicate paths still fail the parser.
Memory is sampled once per second and may miss the true peak. Latency is one
serial fixed-host batch, not a concurrency/serving benchmark.

The single primary contrast, **S-constrained minus S-free**, is
**+0.000000 Recall@5**, paired repository-block 95% interval
**[+0.000000, +0.000000]** (5,000 resamples, seed 20261006, nearest-rank).
The frozen rule requires gain >=0.05, strict/valid counts not lower, interval
lower bound >0, and independent technical/provenance gates PASS.
Primary signal: **FAIL**; numerical rule: FAIL;
technical/provenance: PASS.
All 20 observed S per-task Recall@5 differences are zero; the degenerate bootstrap
interval describes this sample, not equivalence in an unseen population.

G constrained-minus-free gain **+0.050000** and interaction
**+0.050000** are exploratory.
The G gain interval is **[0.000000, 0.150000]** and includes zero.
They do not select a different primary winner. Validity discordance, per-task
metrics and both within-model comparisons are in [comparison.json](comparison.json).

## Output contract findings

| Arm | Unknown-path failures | Duplicate-path failures |
| --- | ---: | ---: |
| S-free | 1 | 0 |
| S-constrained | 0 | 1 |
| G-free | 2 | 2 |
| G-constrained | 0 | 3 |

Constraining supplied paths removes unknown paths, but does not guarantee a valid
unique ranking. All duplicates remain failures under the unchanged evaluator.
Counts come from retained prediction dispositions, not repaired outputs.

## Execution and reproducibility

All 80 research records and 32 separately preregistered technical requests are
retained in the verified private archive. Technical tests cover full offload,
native templates/counters/EOS, input parity, three old payloads repeated per arm,
and constrained empty/escaped-path boundaries. They are not fresh quality samples.
All four execution configs froze jointly before any validation generation; gold
was kept local, absent from the VM/inference sandbox. Evaluation ran only after
complete four-arm collection. Source-free prediction exports are re-evaluated to
verify byte-identical per-task metrics while original raw outputs remain unchanged.

Execution used one g2-standard-4/L4 in us-west1-a, fixed arm order S-free,
S-constrained, G-constrained, G-free. Native caches, serial order and host state
limit timing interpretation. Opposite within-model order does not remove that
confounding. Code identity is an explicitly dirty-base **immutable selected-source
archive**, not the base commit alone. See [provenance](provenance.json),
[joint freeze](research-freeze.json), [technical audit](technical-audit.json),
[parity/repeatability](parity-repeatability.json) and [gates](evidence-gates.json).

The VM and auto-delete boot disk are confirmed absent; existing resource identities
were preserved. Provider start to confirmed absence: **55.60 minutes**.
See [cleanup](cleanup-summary.json), [archive integrity](final-integrity.json),
and [provisioning attempts](provisioning-attempts.json).

## Accounting and limits

Actual full-system cost and cost per successful localization remain **unknown**.
The inclusive session compute-only list-rate scenario is
**USD 0.6550**;
compute/storage/IP subtotal **USD 0.6723**.
These are scenarios, not invoices; network, external preparation, other charges
and active GPU-seconds remain null. Each arm's standalone 20-task lifecycle
scenario replays common preparation and its model download; these scenarios
are not additive parts of the shared campaign invoice. Observed loads follow
probes and do not measure an independently cold-cache startup.
See [session accounting](accounting/session-scenario.json) and
[reviewed region rates](accounting/rate-review.json).

This is new-issue validation in five already seen repositories. There are only
five bootstrap blocks; uncertainty is limited by the small population. Failure
of the rule is not equivalence. These 20 issues are now exposed and cannot
validate later tuned recipes. Verified remains untouched. No training, issue
repair, repository/time generalization, parameter-count causality or economic
substitution claim follows.
