# Work tracker

Updated: 2026-10-06. Track: Small Specialist. Research runs: none.

| ID | Work | Status | Completion evidence / next gate |
| --- | --- | --- | --- |
| EAI-001 | Local Git and GitHub origin | DONE | main; mks-hash/efficient-agentic-inference |
| EAI-002 | Local planning sources | DONE | Two original files preserved in ignored .develop/ |
| EAI-003 | Bootstrap docs, ADR, schema, benchmark contract | DONE | Initial bootstrap commit a3a7157; versioned schemas validated by runner/tests |
| EAI-004 | CPU lexical runner and synthetic contract fixture | DONE | 14 contract tests, ruff lint/format and locked sync pass; CLI fixture complete |
| EAI-005 | SWE-bench acquisition/reconstruction + patch labeler | TODO | Pin revision; independent gold audit and leakage checks |
| EAI-006 | Frozen full-corpus lexical baseline + candidate ceiling | TODO | Measured on development data |
| EAI-007 | Untuned small/generalist matrix | TODO | Verify primary model sources; freeze config and authorize resources |
| EAI-008 | Training decision | BLOCKED_BY_EAI-007 | Material gap, preregistered targets and authorized budget |

## Open decisions before model evaluation

- Pinned dataset/model revisions and confirmed license/access conditions.
- Frozen implementation-file path policy and audited edge-case labels.
- Exact train/dev/final memberships, overlap removal and repository/time controls.
- SS-H2 margin and SS-H3 quality, fallback and economic targets.
- Hardware/backend/pricing boundary and approved GPU budget.

No models have passed evidence gates. Synthetic/local verification must not
promote any model gate or research hypothesis to PASS.

## Bootstrap verification

Local environment: Python 3.12.14 in the uv virtual environment. Locked dependency
sync, ruff checks, formatting and 14 unittest cases passed. `eai baseline --synthetic`
produced all three expected fixture records, including the unreachable new-file
label. Cost/CPS remain null. Artifacts live in ignored
`results/runs/bootstrap-fixture/`; no SWE-bench/model measurement was made.

GitHub CPU CI is configured for Python 3.11 and 3.14; its remote outcome is recorded
separately from local checks. Next step: EAI-005, the pinned dataset/labeling and
leakage contract, before any model or training campaign.
