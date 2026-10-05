# Efficient Agentic Inference

Researching when smaller and specialized language models can reduce the cost
and latency of AI agents while preserving task quality.

## Research question

When can a smaller or specialized model replace a larger generalist inside an
agent system, and when does that substitution improve the economics of
successful tasks?

The project studies the trade-off between
**quality × latency × compute × cost × generalization**.

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
and reproducible result records. See the [benchmark contract](docs/benchmark-localization-v1.md)
and [reproduction guide](docs/reproducibility.md) for measurement definitions.

To run the included CPU lexical example, use Python 3.11+ and uv from the
repository root:

```bash
uv sync --locked
uv run eai baseline --synthetic \
  --tasks examples/localization-v1/tasks.jsonl \
  --gold examples/localization-v1/gold.jsonl \
  --output results/runs/first-fixture
```

The example uses synthetic inputs to verify the evaluation pipeline; it is not a
SWE-bench performance result. Choose a fresh output directory for each run.

## Research documentation

- [Research plan](RESEARCH_PLAN.md)
- [Benchmark contract](docs/benchmark-localization-v1.md)
- [Reproducibility](docs/reproducibility.md)
- [Experiment schemas](schemas/v1/README.md)
- [Results and artifacts](results/README.md)
