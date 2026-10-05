# Work tracker

Updated: 2026-10-06. Track: Small Specialist. Research runs: one frozen lexical dev pilot; no model runs.

| ID | Work | Status | Completion evidence / next gate |
| --- | --- | --- | --- |
| EAI-001 | Local Git and GitHub origin | DONE | main; mks-hash/efficient-agentic-inference |
| EAI-002 | Local planning sources | DONE | Two original files preserved in ignored .develop/ |
| EAI-003 | Bootstrap docs, ADR, schema, benchmark contract | DONE | Initial bootstrap commit a3a7157; versioned schemas validated by runner/tests |
| EAI-004 | CPU lexical runner and synthetic contract fixture | DONE | 14 contract tests, ruff lint/format and locked sync pass; CLI fixture complete |
| EAI-005 | SWE-bench acquisition/reconstruction + patch labeler | DONE_PILOT | Clean-code local and separate-host audits PASS; pinned sources/splits and all 12 tasks prepared/labeled |
| EAI-006 | Frozen full-corpus lexical baseline + candidate ceiling | DONE_PILOT | Full candidate corpus per each of 12 dev tasks; Recall@5 0.541667, ceiling 1; broader population not measured |
| EAI-007 | Untuned small/generalist matrix | PREPARING | ADR 0003 and untuned-dev-v2 protocol; Qwen3-4B-Instruct-2507 original/GGUF/backend revisions pinned; model execution and physical isolation NOT_RUN; local NVIDIA driver unavailable |
| EAI-008 | Training decision | BLOCKED_BY_EAI-007 | Material gap, preregistered targets and authorized budget |
| EAI-009 | Public README positioning and documentation separation | DONE | Research narrative and CPS formula in README; scope/candidates in plan, implementation/check details in reproduction guide |
| EAI-010 | Independent second-host reproduction | DONE | GitHub run 37379561857, clean 397df23; snapshot/input/gold/semantic prediction hashes and metrics match local 0edd9e6 |
| EAI-011 | Broader dev baseline and CPU/system cost accounting | IN_PROGRESS | dev-v2 frozen at 60 disjoint new tasks; matched context builder implemented; rebuilding base trees; no priced economics |
| EAI-012 | v0.1.0 research milestone release | DONE | Annotated tag at 392722c; public release with evidence, provenance, release-commit audit and checksums; CPU CI 37381457746 and second-host reproduction 37381481917 PASS |

## Open decisions before model evaluation

- Exact model revisions, licenses/access and resource fit.
- Train/validation memberships and broader repository/time controls; dev/final pilot IDs are frozen.
- SS-H2 margin and SS-H3 quality, fallback and economic targets.
- Hardware/backend/pricing boundary and approved GPU budget.

No models have passed evidence gates. Synthetic/local verification must not
promote any model gate or research hypothesis to PASS.

## Released milestone

[v0.1.0 — Reproducible SWE-bench Localization Baseline](https://github.com/mks-hash/efficient-agentic-inference/releases/tag/v0.1.0)
is published at code `392722c34ec0e10a0ba8db01179961cf8f885cf8`. Package version is
0.1.0; artifact schemas remain v2.0.0. Original pilot result bytes and experiment
code identities are retained. The release assets add a provenance manifest and
the audit from fresh second-host reproduction on the release commit.

Release-commit CPU CI passed on Python 3.11/3.14 (run 37381457746). Reproduction
passed (run 37381481917): snapshot/input/gold hashes, semantic predictions and
quality match the original reference exactly. The version metadata change in
`__init__.py` is recorded separately from the original runtime source hashes.

## Clean-code dev pilot

Code 0edd9e6; local audit PASS with 17,698 regular-file hashes verified across two
fresh-directory exports, 27 matching deterministic artifacts, 12/12 patch applicability,
forbidden-field and gold mutation invariants, repeated evaluation and physical
network/filesystem isolation. Thirty local tests pass. GitHub CPU CI is green on
Python 3.11/3.14: run 37378939520. Full compact evidence is under
results/reports/swebench-dev-v1/. Monetary cost/CPS are unknown; no efficiency claim.

Separate-host confirmation PASS: GitHub-hosted Xeon 8573C, Python 3.12.3 / Git
2.55.0, versus local i5-7600, predictor Python 3.14.7 / Git 2.56.0. Fresh pinned-source
downloads and snapshots yielded identical deterministic hashes and quality. The
evidence bundle retains local/remote audits and a cross-host comparison. CPU CI
for the report/workflow commit also passed: run 37379554165.

## Bootstrap verification

Local environment: Python 3.12.14 in the uv virtual environment. Locked dependency
sync, ruff checks, formatting and 14 unittest cases passed. `eai baseline --synthetic`
produced all three expected fixture records, including the unreachable new-file
label. Cost/CPS remain null. Artifacts live in ignored
`results/runs/bootstrap-fixture/`; no SWE-bench/model measurement was made.

This section records the historical v1 fixture check. The active contract is v2:
predict/evaluate are independent programs, and GitHub CPU CI includes Parquet
fixtures plus 30 contract tests on Python 3.11 and 3.14.

## SWE-bench foundation

Frozen dev-v1 selects 12 of 225 source tasks, two per each of six repositories,
without reading patches for selection. All Verified IDs are reserved. Snapshot
labels use solution patch only. Candidate policy and edge cases are frozen in ADR
0002 and localization-v2. No model evidence gates have changed.
