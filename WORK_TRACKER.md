# Work tracker

Updated: 2026-10-06. Track: Small Specialist. Research runs: none.

| ID | Work | Status | Completion evidence / next gate |
| --- | --- | --- | --- |
| EAI-001 | Local Git and GitHub origin | DONE | main; mks-hash/efficient-agentic-inference |
| EAI-002 | Local planning sources | DONE | Two original files preserved in ignored .develop/ |
| EAI-003 | Bootstrap docs, ADR, schema, benchmark contract | IN_PROGRESS | Review and validate files before initial commit |
| EAI-004 | CPU lexical runner and synthetic contract fixture | TODO | Run fixture, failure accounting and schema checks |
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
