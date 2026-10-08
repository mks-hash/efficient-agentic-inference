# Efficient Agentic Inference

Researching when smaller and specialized language models can reduce the cost
and latency of AI agents while preserving task quality.

## Research question

When can a smaller or specialized model replace a larger generalist inside an
agent system, and when does that substitution improve the economics of
successful tasks?

The project studies the trade-off between
**quality × latency × compute × cost × generalization**.

## Development results

The frozen SWE-bench dev-v2 file-localization comparison covers **60 tasks across 6 repositories**.

| Method | Recall@5 | Strict Success@5 | Candidate ceiling |
| --- | ---: | ---: | ---: |
| Lexical, full corpus | 0.5523 | 25/60 | 0.9854 |
| Lexical, matched context | 0.2283 | 8/60 | 0.7835 |
| Untuned Qwen3-4B-Instruct-2507 Q4_K_M, matched context | **0.6569** | **33/60** | 0.7835 |
| Qwen3-14B Q4_K_M, non-thinking, matched context | 0.6091 | 30/60 | 0.7835 |

All 60 attempts per model are included, with eight invalid 4B answers and eleven
invalid 14B answers scored as failures. A fresh 4B run reproduced all 60 ranked-path
and disposition records. The larger candidate did not improve quality in the
[matched comparison](results/reports/generalist-dev-v2-l4/README.md); its Recall@5
difference versus fresh 4B is −0.0478 (repository-block 95% interval
[−0.0790, −0.0281]). This finding is specific to the tested models/configurations.
The positive development finding concerns matched evidence; the observed advantage
against full-corpus lexical remains uncertain. These are localization measurements
on exposed development data. Generalization, issue repair and economic benefit
remain untested; cost per successful task is unknown.
Read the [technical report](docs/technical-reports/untuned-dev-v2.md),
[experiment artifacts](results/reports/untuned-dev-v2-l4/README.md) and
[v0.2.0 release](https://github.com/mks-hash/efficient-agentic-inference/releases/tag/v0.2.0).

On a separate **20-issue validation set from five seen repositories**, generation
constraints left 4B Recall@5 unchanged at 0.6333 (strict 9/20). The 14B change
from 0.5958 to 0.6458 is exploratory; its paired interval includes zero. Unknown
paths were eliminated, but duplicate paths still caused failures. The primary
small-model improvement rule did not pass. See the
[reliability validation report](results/reports/reliability-validation-v1-l4/README.md).
This tests new issues within seen repositories, not repository/time generalization.

A further **30-issue validation in four seen repositories** found that a complete
candidate-score recipe reduced Recall@5 from 0.6528 to 0.3222 for 4B and from
0.6750 to 0.1389 for 14B, despite format-valid scores in every task. This negative
finding concerns the frozen prompt/representation/mapping recipe; it does not
reject scoring methods generally. See the
[score-recipe validation report](results/reports/score-ranking-validation-v2-l4/README.md).

The [cross-report synthesis](docs/technical-reports/localization-synthesis-2026-10-08.md)
connects these findings, candidate-coverage limits and the remaining economic questions.

The earlier 12-task lexical pilot achieved Recall@5 0.5417, strict 6/12 and
candidate ceiling 1.0; a separate machine reproduced its deterministic artifacts
and quality. See the [pilot report](results/reports/swebench-dev-v1/README.md) and
[v0.1.0 release](https://github.com/mks-hash/efficient-agentic-inference/releases/tag/v0.1.0).

## Track 1 — Small Specialist

The first study focuses on repository issue localization:

> issue description + repository at its base commit\
> → ranked files likely to require modification

We compare several approaches under the same evaluation contract:

- lexical retrieval
- untuned small language models
- prompt and retrieval improvements
- task-specialized models
- larger generalist models
- small specialists with selective fallback

The goal is to determine **when specialization is economically useful**.
Localization provides a bounded first experiment; downstream evaluation will
measure its effect on end-to-end task quality.

## Primary metric

**Cost per successful task**

```text
cost per successful task =
total measured system cost / successful tasks
```

We also measure task quality, latency, token usage, accelerator time, training
amortization, fallback behavior and generalization.

**A negative result is a result.**

## Reproducibility

Experiments use versioned configurations, explicit model and dataset revisions,
and reproducible result records. See the [benchmark contract](docs/benchmark-localization-v2.md)
and [reproduction guide](docs/reproducibility.md) for measurement definitions.

To run the included CPU lexical example, use Python 3.11+ and uv from the
repository root:

```bash
uv sync --locked
uv run eai-predict --synthetic \
  --inputs examples/localization-v2/tasks.jsonl \
  --output results/runs/first-fixture
uv run eai-evaluate --predictions results/runs/first-fixture \
  --gold examples/localization-v2/gold.jsonl \
  --output results/runs/first-evaluation
```

The example uses synthetic inputs to verify the evaluation pipeline; it is not a
SWE-bench performance result. Choose a fresh output directory for each run.

## Research documentation

- [Research plan](RESEARCH_PLAN.md)
- [Benchmark contract](docs/benchmark-localization-v2.md)
- [Reproducibility](docs/reproducibility.md)
- [Artifact schemas](schemas/v2/README.md)
- [Cost accounting](docs/cost-accounting-v1.md)
- [Results and artifacts](results/README.md)
