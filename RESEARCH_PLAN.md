# Research plan — Small Specialist

Status: development baselines and new-issue validation, 2026-10-08; localization contract v2. A lexical
pilot has a separate-host reproduction; a frozen untuned Qwen3-4B development
comparison is recorded in [the report](results/reports/untuned-dev-v2-l4/README.md).
One matched larger candidate has been evaluated; validated stronger-generalist
substitution, specialization and full-system economics remain unconfirmed.
The untuned dev protocol freezes its own numerical decision rule; future adaptation
and fallback targets below require their own dated, hashed preregistration.

## Objective and boundary

Determine when specialization is economically rational for a bounded agent
function. Start with file localization on SWE-bench; add symbol localization and
fixed downstream repair only after independent contracts exist. Use established
model/training machinery; own the data, evaluator, routing and evidence contracts.

ToolGap remains an independent runtime/cache study. Reuse its methodological
discipline without importing its runtime or SGLang code. Gemma/Kaggle is an
optional opportunity track; competition requirements do not define the core.

Initial model candidates include Qwen and Gemma small models and larger references.
Before selecting the matrix, verify availability, licenses, exact revisions,
hardware fit and any applicable competition details against primary sources.

## Hypotheses

| ID | Claim to test | Falsification or limit |
| --- | --- | --- |
| SS-H1 | A small specialist retains ≥90% of a stronger generalist's mean Recall@5. | Paired evaluation fails the frozen retention criterion; an ineffective generalist cannot establish substitution. |
| SS-H2 | Adaptation adds material value over the same small model with frozen evidence. | Gain below a preregistered margin, or no improved amortized economics. |
| SS-H3 | Selective fallback approaches generalist quality while escalating a minority of tasks and reducing CPS. | Quality target, fallback cap or CPS target fails. |
| SS-H4 | Smallest parameter count need not minimize CPS. | No interior optimum observed; report the tested range only. |
| SS-H5 | Gains survive repository-disjoint and temporal evaluation. | Gains disappear or uncertainty precludes a claim. |
| SS-H6 | Narrow adaptation can degrade unrelated behavior. | Measure an independently frozen control workload; do not assume safety from target quality. |
| SS-H7 | Training data size changes quality with eventual diminishing returns. | Report learning curve and uncertainty, including no improvement. |
| SS-H8 | Cheap uncertainty outperforms random fallback at equal escalation rate. | No advantage against a matched-rate random policy. |
| SS-H9 | Smaller serving footprint improves concurrency economics. | Equal-hardware, equal-arrival-trace measurements show no benefit. |
| SS-H10 | Architecture and residency predict economics beyond parameter count. | Evidence insufficient across architectures; retain a narrow claim. |

Before the first model campaign freeze: the SS-H2 improvement margin; SS-H3
quality tolerance, fallback cap (<50%) and CPS reduction; primary K=5; success
definition; sample membership; repetitions; random fallback seeds; statistical
acceptance rule. Do not choose these after seeing test outcomes.

## Treatments

| Arm | Treatment | Evidence |
| --- | --- | --- |
| R0 | Lexical ranking | Frozen repository candidate corpus |
| R1 | Untuned small model | Frozen retrieval profile A |
| R2 | Untuned small + improved prompt/retrieval | Explicit profile B treatment |
| R3 | LoRA/QLoRA specialist | Exactly the matched untuned comparator's evidence/profile |
| R4 | Larger generalist | Same canonical evidence as matched small model |
| R5 | Specialist + fallback | Same initial evidence; extra work explicitly accounted |

Do not attribute retrieval improvements to training. Across model families match
semantic evidence and candidate budgets, while preserving each native tokenizer
and exact rendered/tokenized inputs.

## Metrics and statistics

File Recall@1/3/5/10, Precision@K, MRR and strict all-gold-files Success@K;
all-changed and implementation-only metrics reported separately. Latency p50/p95,
input/output tokens, accelerator time with an explicit measurement boundary, peak memory, monetary cost, fallback
rate and errors. CPS = sum(cost of all attempts) / strict successes at frozen K.
Unknown cost blocks a numeric CPS claim. Zero successes gives undefined CPS.

Report training and setup costs separately and show training-amortized CPS(N).
Fallback includes specialist, generalist, router and repeated preparation costs.
Use paired task sets and repository-aware confidence intervals. Confirm the
winning training recipe with multiple seeds before broad adaptation claims.

## Data and generalization

Pin data revision and reconstruct repositories at base_commit. Derive gold solely
in evaluation/labeling. Preserve Verified as final evaluation; remove every overlap
with it from training/dev, including equivalent issues/patches. Report remaining
pretraining contamination as a limitation. Freeze repository-disjoint and temporal
tests independently; do not tune routing or prompts against final evaluation.

The reserved [validation-v1](splits/validation-v1.json) membership contains 20 new
same-repository issues excluding both exposed dev populations and Verified, with
normalized equivalents excluded. Labels/predictions are not produced during
preparation. It is not a repository/time hold-out; future training must exclude
this membership and its equivalents.

## Milestones and stop/go gates

1. Bootstrap: readable contracts, schema, evidence rules, tracker and CPU fixture.
2. Dataset: pinned sources, deterministic patch labeler, implementation-path policy,
   leakage audit and manually audited gold fixtures. Stop if labels are ambiguous
   or reconstruction is not reliable; resolve the contract before running models.
3. Baselines: full-corpus lexical floor and candidate recall ceiling, then useful
   untuned small/generalist outputs. Fix retrieval if its ceiling prevents testing
   model capability. Stop a model campaign if its output contract is unusable.
4. Adaptation: proceed only if an untuned gap exists and budget is authorized.
   Stop a pilot with no frozen material dev gain; publish that outcome. A strong
   untuned small model can make training unnecessary.
5. Frozen comparison: quality, cost and latency on identical held-out instances.
   Do not publish efficiency if accounting, provenance or evaluator gates fail.
6. Fallback and generalization: only after independent core measurements. Broader
   serving/concurrency and ToolGap composition require separate evidence gates.

The released v0.1.0 records a reproducible lexical dev pilot. The completed
[untuned-dev-v2](docs/experiments/untuned-dev-v2.md) campaign compares 60 new
issues under full-corpus and matched-context lexical controls with one untuned
model on the identical packet. The [technical report](docs/technical-reports/untuned-dev-v2.md)
records a positive matched-context development finding. The [matched 14B comparison](results/reports/generalist-dev-v2-l4/README.md)
replicated the small baseline and recorded lower quality for this larger candidate.
Its preregistered positive-gap rule fails; this candidate does not justify training.
Training follows new independent evidence and a separately authorized protocol
and budget. No future campaign is authorized by these milestone notes.

[Matched generalist preparation](docs/experiments/generalist-dev-v2.md) selects one
larger 14B non-thinking candidate and a fresh 4B replication under the existing
packet contract. [Cost accounting v1](docs/cost-accounting-v1.md) distinguishes
actual charges from deployment scenarios. The completed comparison records actual fit/native/quality gates and partial
cost scenarios separately from CPU implementation evidence. Actual full-system
CPS remains unknown; validation-v1 was reserved for the intervention below,
and Verified remains reserved.

## Next bounded intervention: output reliability

[ADR 0007](decisions/0007-constrained-output-validation.md) and the
[reliability validation protocol](docs/experiments/reliability-validation-v1.md)
compare both pinned models with/without generation-time JSON/candidate constraints
on the 20 reserved validation issues. Membership has five previously seen repositories,
four issues each. Exact datasets/labels and contexts were reconstructed twice;
CPU/native synthetic checks established implementation before the separately
authorized paid campaign. The primary small-model contrast and decision rule were
frozen; larger-model effects remain exploratory. The
[completed report](results/reports/reliability-validation-v1-l4/README.md) records
all 80 research and 32 technical requests. S Recall@5 gain is zero, strict 9/20
and valid 19/20 in both modes; the primary rule fails. G gain is +0.05 with
repository-block interval [0, 0.15], an exploratory result. Candidate ceiling is
0.879167 in all four arms. JSON/path constraints do not enforce uniqueness, and
duplicate paths remain strict failures. This tests reliability without changing
the localization-v2 grader and does not justify training, economics or
repository/time generalization. Validation-v1 is now exposed and must not validate
later recipes tuned from these failures. Future training still excludes its
membership/equivalents; a new validation population/contract is required.

## Completed recipe: complete candidate scores

[ADR 0009](decisions/0009-score-vector-ranking.md) and the
[score-ranking contract](docs/experiments/score-ranking-validation-v2.md) reserve
30 new issues in four previously seen repositories, excluding every prior frozen
population and Verified IDs/normalized equivalents. Compare fresh path-constrained
controls with one fixed-length integer score per candidate. Positive scores map
to unique paths by descending score, path-order ties, top ten; zero excludes.
This changes prompt, representation and mapping together, not uniqueness alone.
The evaluator, retrieval evidence, pinned artifacts and all-attempt denominators
stay unchanged. Primary remains the 4B within-model gain, with strict/valid
noninferiority and positive repository-block interval; 14B remains exploratory.
Four blocks limit statistical confidence. Preparation and synthetic CPU evidence
authorize neither validation inference, paid resources, training nor publication.

The separately authorized L4 campaign is complete; see the
[score-ranking report](results/reports/score-ranking-validation-v2-l4/README.md).
All 120 research and 24 technical attempts were collected and independently
audited before local evaluation. The primary 4B score-minus-path Recall@5 gain
is −0.330556 (repository-block 95% interval [−0.575269, −0.166667]); strict successes
fall from 15/30 to 7/30 despite 30/30 format-valid outputs in both arms. The 14B
exploratory gain is −0.536111, strict 17/30 → 4/30, with score validity 30/30
versus path validity 29/30. Candidate ceiling is 0.802778 in all four arms.
This frozen score recipe is rejected for improvement; preserve path generation
as the stronger tested recipe. Do not repair thresholds/ties and revalidate on
these now-exposed 30 issues. No general scoring-method, training, parameter-count
or economic-substitution claim follows. Actual billing/full CPS remain unknown.
The new VM and auto-delete disk are absent; existing resource identities survived.
