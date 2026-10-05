# Work tracker

Updated: 2026-10-06. Track: Small Specialist. Research runs: none.

| ID | Work | Status | Completion evidence / next gate |
| --- | --- | --- | --- |
| EAI-001 | Local Git and GitHub origin | DONE | main; mks-hash/efficient-agentic-inference |
| EAI-002 | Local planning sources | DONE | Two original files preserved in ignored .develop/ |
| EAI-003 | Bootstrap docs, ADR, schema, benchmark contract | DONE | Initial bootstrap commit a3a7157; versioned schemas validated by runner/tests |
| EAI-004 | CPU lexical runner and synthetic contract fixture | DONE | 14 contract tests, ruff lint/format and locked sync pass; CLI fixture complete |
| EAI-005 | SWE-bench acquisition/reconstruction + patch labeler | DONE_LOCAL | Clean commit 0edd9e6, pinned sources/splits, all 12 tasks prepared/labeled, schemas and leakage audit PASS; second-host check pending |
| EAI-006 | Frozen full-corpus lexical baseline + candidate ceiling | DONE_PILOT | Full candidate corpus per each of 12 dev tasks; Recall@5 0.541667, ceiling 1; broader population not measured |
| EAI-007 | Untuned small/generalist matrix | TODO | Verify primary model sources; freeze config and authorize resources |
| EAI-008 | Training decision | BLOCKED_BY_EAI-007 | Material gap, preregistered targets and authorized budget |
| EAI-009 | Public README positioning and documentation separation | DONE | Research narrative and CPS formula in README; scope/candidates in plan, implementation/check details in reproduction guide |
| EAI-010 | Independent second-host reproduction | IN_PROGRESS | Manual CPU workflow compares a fresh GitHub-hosted rebuild with the published local reference |

## Open decisions before model evaluation

- Exact model revisions, licenses/access and resource fit.
- Train/validation memberships and broader repository/time controls; dev/final pilot IDs are frozen.
- SS-H2 margin and SS-H3 quality, fallback and economic targets.
- Hardware/backend/pricing boundary and approved GPU budget.

No models have passed evidence gates. Synthetic/local verification must not
promote any model gate or research hypothesis to PASS.

## Clean-code dev pilot

Code 0edd9e6; local audit PASS with 17,698 regular-file hashes verified across two
fresh-directory exports, 27 matching deterministic artifacts, 12/12 patch applicability,
forbidden-field and gold mutation invariants, repeated evaluation and physical
network/filesystem isolation. Thirty local tests pass. GitHub CPU CI is green on
Python 3.11/3.14: run 37378939520. Full compact evidence is under
results/reports/swebench-dev-v1/. Monetary cost/CPS are unknown; no efficiency claim.

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
