# Research plan — Small Specialist

Status: research design, 2026-10-06; localization contract v2. A small lexical dev
pilot is recorded with a separate-host reproduction; no model or specialization
claims exist. This plan is not a
completed preregistration: numerical decisions below must be frozen in a dated,
hashed experiment config before model evaluation.

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

The released v0.1.0 records a reproducible lexical dev pilot. The next campaign
is [untuned-dev-v2](docs/experiments/untuned-dev-v2.md): 60 new development issues,
full-corpus and matched-context lexical controls, followed by one untuned model
on the identical context packet. Its execution/resource gates remain separate.
Dates and model choices are planning inputs. Training follows an evidence-based
decision; paid runs require budget authorization.
