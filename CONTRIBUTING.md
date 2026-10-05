# Contributing

Read AGENTS.md and the relevant versioned research contract first. Keep changes
small, explain their effect on comparability, and preserve all failed attempts.

```bash
uv sync --locked --extra data
uv run ruff check .
uv run ruff format --check .
uv run python -m unittest discover -s tests -v
```

Ordinary pull requests require CPU checks only. A fixture pass is software evidence,
not a model quality or efficiency claim. Dataset/model campaigns require separately
frozen configurations and an authorized resource budget. Never commit `.develop/`,
credentials, downloaded models or full datasets.

Include problem/result, contract changes, verification performed and any unrun
checks in a pull request. Changes to graders or split policies require a decision
record and an explicit new comparison/version policy.
