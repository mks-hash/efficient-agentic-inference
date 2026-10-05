# Synthetic separated-program fixture

These three manually specified cases are software fixtures, not SWE-bench evidence:
single-file localization, multiple gold files and an unreachable new file.
Expected mean Recall@5 = 2/3, strict Success@5 = 2/3. Candidate ceiling averages
2/3; conditional Recall@5 = 1 across the two tasks with accessible gold.

```bash
uv run eai-predict --synthetic --inputs examples/localization-v2/tasks.jsonl \
  --output results/runs/fixture-predictions
uv run eai-evaluate --predictions results/runs/fixture-predictions \
  --gold examples/localization-v2/gold.jsonl --output results/runs/fixture-evaluation
```

Gold is not an argument to prediction. Monetary cost/CPS remain null. The v1
example is retained for historical contract context; the old baseline CLI is retired.
