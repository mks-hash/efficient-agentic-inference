# Efficient Agentic Inference

Measuring when smaller and specialized models can make AI agents cheaper and
faster without sacrificing task success.

**Research question:** when can a smaller or specialized model replace an
expensive generalist inside an agent system, and when does that substitution
actually reduce cost per successful task?

Track 1, **Small Specialist**, begins with repository issue localization:
issue description + repository at its base commit → ranked files likely to
require modification. We compare lexical retrieval, untuned small models,
prompt/retrieval improvements, learned specialists, larger generalists and
specialist systems with selective fallback.

The primary economic measure is total measured cost divided by successful tasks.
Quality, latency, tokens, allocated GPU time, training amortization, fallback and
generalization determine whether a change is useful. A negative result is a result.

## Current status

Repository bootstrap; no SWE-bench or model results exist yet. The first executable
baseline will be a CPU lexical runner on synthetic contract fixtures. Those
fixtures are software checks and cannot support research claims.

## Start here

- [Research plan](RESEARCH_PLAN.md): hypotheses, treatments and decision gates.
- [Work tracker](WORK_TRACKER.md): completed work and the next actionable steps.
- [Benchmark contract v1](docs/benchmark-localization-v1.md): inputs, labels and metrics.
- [Evidence and reproduction](docs/reproducibility.md): immutable runs and readiness.
- [Schemas v1](schemas/v1/README.md): versioned experiment and prediction records.
- [Scope decision](decisions/0001-bounded-task-and-economics.md).

ToolGap remains an independent runtime/cache study. We reuse its methodological
discipline, without importing its runtime or SGLang code. Gemma/Kaggle is an
optional opportunity track; competition requirements do not define the core.

Model candidates from the planning material include Qwen and Gemma small models
and larger references. Availability, licenses, exact revisions, hardware fit and
competition details must be verified before use.
