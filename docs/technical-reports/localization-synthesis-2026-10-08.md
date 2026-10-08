# What the localization experiments establish

Research synthesis · 2026-10-08 · Efficient Agentic Inference, Track 1

The strongest positive finding is useful untuned small-model localization over
lexical ranking of identical bounded evidence. The strongest negative finding
is substantial quality loss from the tested integer-score recipe despite correct
output formatting and unique mapping. Specialization and full-system economic
substitution remain untested.

Original experiments and decision rules remain unchanged. Additional model
contrasts, oracle bounds and decompositions below are **post hoc descriptive**;
they introduce no acceptance criteria or confirmatory winner. All four model-report
checksum sets pass (296 entries). See [diagnostics and source hashes](localization-synthesis-analysis.json).

## Experimental sequence

| Population | Question | Result | Interpretation |
| --- | --- | --- | --- |
| dev-v1: 12 issues / 6 repos | Is the dataset/lexical pipeline reproducible? | Recall@5 0.5417, strict 6/12, ceiling 1.0; separate-host reproduction | Reproducible pilot |
| dev-v2: 60 issues / 6 repos | Does untuned 4B help on matched evidence? | Lexical 0.2283 → 4B 0.6569; strict 8/60 → 33/60 | Primary development signal passes |
| Same dev-v2, fresh 4B / 14B | Does the larger candidate provide a useful gap? | 4B 0.6569 vs 14B 0.6091 | Larger-candidate improvement rule fails; historical 4B outputs reproduce |
| validation-v1: 20 new issues / 5 seen repos | Do candidate-generation constraints help? | 4B gain 0; exploratory 14B gain +0.05, interval [0, 0.15] | No primary improvement |
| validation-v2: 30 new issues / 4 seen repos | Does the complete score recipe help? | 4B 0.6528 → 0.3222; 14B 0.6750 → 0.1389 | Tested score recipe substantially harms quality |

Sources: [pilot](../../results/reports/swebench-dev-v1/README.md),
[untuned baseline](../../results/reports/untuned-dev-v2-l4/README.md),
[matched models](../../results/reports/generalist-dev-v2-l4/README.md),
[generation constraints](../../results/reports/reliability-validation-v1-l4/README.md),
[candidate scores](../../results/reports/score-ranking-validation-v2-l4/README.md).
Different populations/recipes cannot be pooled into one headline accuracy or
interpreted as a chronological performance trend.

## Useful small-model evidence, with limits

The 4B-minus-matched-lexical gain is +0.4286, with preregistered repository-block
95% interval [0.3159, 0.5597]. Identical paths/excerpts make this a useful model
treatment comparison. It does not identify reasoning as the mechanism.

Full-corpus lexical scores 0.5523. The model's observed +0.1047 advantage has a
supplementary interval [−0.0012, 0.2164] including zero; representations and candidate
sets differ. A general victory over lexical retrieval is not established.

Small-model path/free results remain around 0.63–0.66 on three issue populations.
This is descriptive consistency within seen repositories. Later populations lack
a repeated matched lexical control and cannot independently confirm that original
model-versus-lexical gain.

## Larger parameter count did not establish a stable quality advantage

| Matched recipe / population | G-minus-S Recall@5 | Repository-block 95% interval | Status |
| --- | ---: | --- | --- |
| Unconstrained dev-v2, 60 tasks | −0.0478 | [−0.0790, −0.0281] | Original preregistered model contrast |
| Constrained validation-v1, 20 tasks | +0.0125 | [−0.1500, +0.1667] | Post hoc descriptive |
| Constrained paths validation-v2, 30 tasks | +0.0222 | [−0.0833, +0.1548] | Post hoc descriptive |

There is no consistent observed material 14B advantage. These results do not
prove equivalence or small-model noninferiority. Different post-training/conversion
histories prevent attribution to parameter count. The 4B is untuned for the task;
SS-H1 about a trained specialist remains untested despite favorable point ratios.

Observed path request medians favor 4B by roughly 3.3–4 times across the matched
serial batches. Latest p50 is 3.654 versus 12.052 seconds; sampled memory maxima
are 4,942 versus 11,006 MiB. These are resource observations, not concurrency,
cold-start or full-system monetary measurements.

## Output validity is not localization quality

Candidate-path grammar removes unknown paths but does not enforce uniqueness.
On validation-v1 the 4B invalid count remains one: an unknown-path failure is
replaced by a duplicate-path failure; every per-task Recall@5 difference is zero.
The 14B improvements are exploratory, with an interval including zero.

The score recipe yields 30/30 valid vectors for each model and unique mapped
paths. The primary 4B gain is nevertheless −0.3306, interval [−0.5753, −0.1667].
Strict success falls 15/30 → 7/30; exploratory 14B strict falls 17/30 → 4/30.
This changes prompt, representation and mapping together, not uniqueness alone.

Additional descriptive analysis shows:

- Mean score-minus-path quality decreases in all four repositories for both models.
- 4B has one empty score ranking, contributing −0.0111 to the all-task difference;
  its 29 nonempty answers contribute −0.3194. Empty answers alone do not explain it.
- 14B has 15 empty score rankings, contributing −0.3389; the 15 nonempty answers
  contribute another −0.1972. Empty answers account for much, but not all, of its loss.
- Positive-score ties cross the top-five boundary in 14/30 small-model and 5/30
  large-model cases. This does not establish ties as the cause.

Positional binding difficulty, score semantics, zero exclusion, prompt wording
and tie rules remain hypotheses. The experiments do not isolate their effects.
Do not revise thresholds/ties and claim confirmation on these exposed 30 issues.
Retain the frozen path recipe as the stronger tested comparator.

## Evidence availability and ranking both limit quality

Dev-v2 full-corpus candidate ceiling is 0.9854; the bounded ceiling is 0.7835.
Validation-v2 bounded ceiling is 0.8028. Inaccessible files cannot be selected;
file presence does not prove the first 1,200 characters contain useful evidence.

Candidate ceiling differs from a top-five oracle when a task has more than five
gold files. Evaluator-only bounds account for both availability and K:

| Population | Ideal candidate top-five Recall | Ideal strict successes | Observed 4B path/free strict |
| --- | ---: | ---: | ---: |
| dev-v2 | 0.7813 | 39/60 | 33/60 |
| validation-v1 | 0.8792 | 14/20 | 9/20 |
| validation-v2 | 0.8028 | 21/30 | 15/30 |

On validation-v2 the small model is 0.15 Recall@5 below the ideal candidate-bound
ranker. Nine tasks cannot attain strict success under the current candidate/K
contract; six further successes separate observed 4B from the ideal 21/30.
These are upper-bound arithmetic, not semantic causes or promised training gains.

This supports studying broader file coverage and more useful excerpts under a
fixed token budget. Training cannot recover files absent from its candidates.

## Fallback complementarity is limited and population-dependent

An evaluator with perfect knowledge could choose between the saved model outputs:

| Population / recipe | 4B strict | 14B-only successes | Perfect-choice strict |
| --- | ---: | ---: | ---: |
| dev-v2, unconstrained | 33/60 | 1 | 34/60 |
| validation-v1, constrained | 9/20 | 3 | 12/20 |
| validation-v2, paths | 15/30 | 3 | 18/30 |

This is a gold-aware post-hoc oracle, not an implemented router, merged ranking
or economic result. On the latest set both models fail strict coverage for 12
tasks; choosing between those outputs cannot fix them. Any router requires
allowed inference features, fresh validation, a matched-rate random control and
accounting for escalation/repeated work. The oracle does not establish worthwhile
14B fallback economics.

## The economic and specialization thesis remains open

Training, amortization, attributable full-system CPS, repository/time generalization
and downstream issue repair have not been evaluated. Cloud rate scenarios are
not invoices. Gold describes files in one accepted patch; alternative valid repairs
may differ. Runtime gold isolation does not prove absence of pretraining contamination
or near duplicates. Four to six repository blocks limit uncertainty estimates.

Preserve 4B path generation as the default research comparator. Stop pursuing
this frozen score recipe as an improvement. Infrastructure readiness alone does
not justify a LoRA run; no positive trained-specialist claim has been tested.

## Recommended next milestone

Prepare an **evidence-budget comparison** using a few declared candidate/excerpt
policies at the same model input budget. CPU-only work can first measure file
coverage, strict ceilings, packet sizes and excerpt placement. Post-hoc inspection
generates hypotheses rather than validation. Include lexical full-corpus and
matched-evidence controls to distinguish changed retrieval from model gains.

Then preregister one comparison with the frozen 4B path recipe and fresh evaluation
membership, excluding every previous evaluation population/equivalent and keeping
Verified reserved. Freeze minimum useful gain and accounting boundaries before
execution. A broader repository/time evaluation needs its own source/population
contract, particularly if the eligible development source is exhausted.

Fallback is secondary if fresh complementarity and deployment accounting justify
it. Training should target an identified learnable ranking gap with separate data,
a matched untuned comparator and amortized cost. This recommendation authorizes
no new model/GPU run, training or publication.

## Reproduce the additional diagnostics

From the repository root with its existing environment:

```bash
uv run python docs/technical-reports/analyze-localization-synthesis.py
```

The analysis verifies report checksums and reuses the existing paired bootstrap.
It reads saved metrics, path-only predictions and split membership, runs no model
and opens no gold patches or labels. Original report files remain unchanged.
