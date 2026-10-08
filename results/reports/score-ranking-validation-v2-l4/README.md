# Path and score recipes on fresh localization validation

**Result: this frozen score recipe substantially reduced localization quality.**
The primary 4B contrast is −0.330556 Recall@5; the exploratory 14B contrast is
−0.536111. All score vectors were format-valid, so format reliability did not
translate into useful ranking. Preserve the path recipe as the stronger tested
control; these findings do not reject other scoring prompts or representations.

**30 issues / four seen repositories; four frozen recipes, one attempt per task.**
Pinned Qwen3-4B-Instruct-2507 and Qwen3-14B Q4_K_M (non-thinking), the same
bounded user evidence, greedy decoding and strict evaluator. Both recipes use
gold-blind generation schemas. The score recipe changes the system prompt, output
representation and deterministic mapping together; this is not a uniqueness-only
causal experiment.

| Arm | Recall@5 | Strict@5 | Valid | Candidate ceiling | p50 / p95 request | Sampled peak GPU MiB |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| S-paths | 0.652778 | 15/30 | 30/30 | 0.802778 | 3.654s / 4.945s | 4942 |
| S-scores | 0.322222 | 7/30 | 30/30 | 0.802778 | 4.095s / 5.386s | 4942 |
| G-paths | 0.675000 | 17/30 | 29/30 | 0.802778 | 12.052s / 13.751s | 11006 |
| G-scores | 0.138889 | 4/30 | 30/30 | 0.802778 | 9.895s / 13.271s | 11006 |

Invalid outputs remain zero in all-attempt quality. Empty valid answers also
remain unsuccessful for nonempty gold. Path arrays allow at most ten supplied
paths and duplicate paths still fail the parser. Score vectors bind one integer
0–100 to each candidate; positive scores sort descending with path ties, then
truncate to ten. Repeated scores are allowed, zero scores exclude candidates.
Memory is sampled once per second and may miss the true peak. Latency is one
serial fixed-host batch, not a concurrency/serving benchmark.

The single primary contrast, **S-scores minus S-paths**, is
**-0.330556 Recall@5**, paired repository-block 95% interval
**[-0.575269, -0.166667]** (5,000 resamples, seed 20261006, nearest-rank).
The frozen rule requires gain >=0.05, strict/valid counts not lower, interval
lower bound >0, and independent technical/provenance gates PASS.
Primary signal: **FAIL**; numerical rule: FAIL;
technical/provenance: PASS.

G scores-minus-paths gain **-0.536111** and interaction
**-0.205556** are exploratory.
They do not select a different primary winner. Validity discordance, per-task
metrics and both within-model comparisons are in [comparison.json](comparison.json).

## Descriptive score diagnostics

The 4B score outputs contain 243 zero entries out of 600 and produce one empty
ranking. The 14B outputs contain 466 zero entries and produce 15 empty rankings.
Positive-score ties cross the top-five boundary in 14/30 and 5/30 cases,
respectively. These post-run descriptions do not identify the cause of the
quality loss or select a revised threshold/tie rule. No outputs were repaired or
rerun. The prompt, zero policy and path-order tie rule were frozen together.

## Execution and reproducibility

All 120 research records and 24 separately preregistered technical requests are
retained in the verified private archive. Technical tests cover full offload,
native templates/counters/EOS, matched user evidence, five synthetic boundaries
(including one greedy-repeat pair) and one exposed old issue per arm. They are not fresh quality samples.
All four execution configs froze jointly before any validation generation; gold
was kept local, absent from the VM/inference sandbox. Evaluation ran only after
complete four-arm collection. Source-free prediction exports are re-evaluated to
verify byte-identical per-task metrics while original raw outputs remain unchanged.

Execution used one g2-standard-4/L4 in us-west1-a, fixed arm order S-paths,
S-scores, G-scores, G-paths. Native caches, serial order and host state
limit timing interpretation. Opposite within-model order does not remove that
confounding. Code identity is an explicitly dirty-base **immutable selected-source
archive**, not the base commit alone. See [provenance](provenance.json),
[joint freeze](research-freeze.json), [technical audit](technical-audit.json),
[parity/repeatability](parity-repeatability.json) and [gates](evidence-gates.json).

The VM and auto-delete boot disk are confirmed absent; existing resource identities
were preserved. Provider start to confirmed absence: **55.87 minutes**.
See [cleanup](cleanup-summary.json), [archive integrity](final-integrity.json),
and [provisioning attempts](provisioning-attempts.json).

## Accounting and limits

Actual full-system cost and cost per successful localization remain **unknown**.
The inclusive session compute-only list-rate scenario is
**USD 0.6582**;
compute/storage/IP subtotal **USD 0.6756**.
These are scenarios, not invoices; network, external preparation, other charges
and active GPU-seconds remain null. Each arm's standalone 30-task lifecycle
scenario replays common preparation and its model download; these scenarios
are not additive parts of the shared campaign invoice. Observed loads follow
probes and do not measure an independently cold-cache startup.
See [session accounting](accounting/session-scenario.json) and
[reviewed region rates](accounting/rate-review.json).

This is new-issue validation in four already seen repositories. There are only
four bootstrap blocks; uncertainty is limited by the small population. Failure
of the rule is not equivalence. These 30 issues are now exposed and cannot
validate later tuned recipes. Verified remains untouched. No training, issue
repair, repository/time generalization, parameter-count causality or economic
substitution claim follows. No publication or release is implied by this local report.
