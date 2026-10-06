# Work tracker

Updated: 2026-10-06. Track: Small Specialist. Research runs: dev-v1 pilot plus dev-v2 lexical controls; untuned L4 dev-v2 baseline complete; CPU smoke ended at its time limit; cloud resources deleted.

| ID | Work | Status | Completion evidence / next gate |
| --- | --- | --- | --- |
| EAI-001 | Local Git and GitHub origin | DONE | main; mks-hash/efficient-agentic-inference |
| EAI-002 | Local planning sources | DONE | Two original files preserved in ignored .develop/ |
| EAI-003 | Bootstrap docs, ADR, schema, benchmark contract | DONE | Initial bootstrap commit a3a7157; versioned schemas validated by runner/tests |
| EAI-004 | CPU lexical runner and synthetic contract fixture | DONE | 14 contract tests, ruff lint/format and locked sync pass; CLI fixture complete |
| EAI-005 | SWE-bench acquisition/reconstruction + patch labeler | DONE_PILOT | Clean-code local and separate-host audits PASS; pinned sources/splits and all 12 tasks prepared/labeled |
| EAI-006 | Frozen full-corpus lexical baseline + candidate ceiling | DONE_PILOT | Full candidate corpus per each of 12 dev tasks; Recall@5 0.541667, ceiling 1; broader population not measured |
| EAI-007 | Untuned small/generalist matrix | SMALL_DONE_GENERALIST_NOT_RUN | clean f67e499 L4: 60/60 attempted, 52 valid / 8 invalid; Recall@5 0.656926 / strict 33/60; native tokens/full offload/isolation PASS; matched development rule PASS; generalist/training/economics not established |
| EAI-008 | Training decision | BLOCKED_BY_GENERALIST_AND_ACCOUNTING | Untuned dev signal is positive; stronger matched generalist, adaptation justification/targets and separate training budget still required |
| EAI-009 | Public README positioning and documentation separation | DONE | Research narrative and CPS formula in README; scope/candidates in plan, implementation/check details in reproduction guide |
| EAI-010 | Independent second-host reproduction | DONE | GitHub run 37379561857, clean 397df23; snapshot/input/gold/semantic prediction hashes and metrics match local 0edd9e6 |
| EAI-011 | Broader dev baseline and CPU/system cost accounting | FOUNDATION_VALIDATED | Clean 0bd7571 audit PASS: 60/60 prepared/labeled, 123 identical artifacts, 88638 file hashes; full Recall@5 0.552265 / ceiling 0.985450 / strict 25/60; matched context 0.228326 / ceiling 0.783487 / strict 8/60; phase accounting explicit, no prices or model results |
| EAI-012 | v0.1.0 research milestone release | DONE | Annotated tag at 392722c; public release with evidence, provenance, release-commit audit and checksums; CPU CI 37381457746 and second-host reproduction 37381481917 PASS |

## Open decisions before generalist/adaptation

- Stronger generalist revision, license/access, resource fit and explicit run budget.
- Train/validation memberships and broader repository/time controls; dev/final pilot IDs are frozen.
- SS-H2 margin and SS-H3 quality, fallback and economic targets.
- Hardware/backend/pricing boundary and approved GPU budget.

The pinned Qwen L4 treatment passed actual identity, native tokens, resource and
physical-isolation gates. Its development decision rule passes. Specialization,
generalist replacement, held-out generalization and end-to-end economics remain
unconfirmed. Software fixtures establish implementation behavior only.

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

## Next campaign preparation

dev-v2 excludes all dev-v1 IDs/normalized equivalent issues before selection and
reserves Verified. The named split freezer reproduces the original dev-v1 bytes.
Thirty-eight CPU tests passed, including exposure exclusions and context ceiling
loss. Context preparation and matched prediction passed physical-isolation probes;
context inputs and semantic provenance match across two fresh base reconstructions.
The scored dev-v2 population is now exposed development data.

The [preparation report](results/reports/swebench-dev-v2-preparation/README.md)
retains both lexical controls and audit/checksum evidence. The simple prefix
context reduces file coverage and lexical quality; model results must be compared
against both controls. Source-bearing inputs remain ignored and reproducible.
ADR 0004 selects local CPU capability checks: synthetic API probe followed by the
old 12 dev-v1 tasks, then conditional full dev-v2 execution. The pinned llama.cpp
CPU binary has been built; weights match their exact byte length and SHA-256. Forty-six CPU contract tests
and lint pass. The synthetic native API probe passed physical isolation, exact input/output
token counter agreement and strict JSON (192 input / 7 output tokens). The old dev-v1 CPU smoke ended at its one-hour campaign limit: 9/12
started, seven valid, one unknown-path output, one timeout and three unattempted.
All twelve remain in evaluation (Recall@5 0.375, strict 4/12); this incomplete
exposed smoke is not a new research baseline. Eight completed native requests
fit the context and verify token counters. Native completed-request p50 is
410.780 seconds; extrapolated 60-request CPU time is about 6.85 hours, not measured
dev-v2 latency. CPU dev-v2 is NOT_RUN. An active outer launcher was edited during
its child run, causing post-inference shell parsing to fail; internal result hashes
and ce08620 staged-module identity passed. The outer checksum manifest was
recovered once without changing inference files or repeating attempts. The
immutable transported GPU launcher is unaffected. This host has a GTX 1060 with unavailable
NVIDIA driver; CPU timing will identify the exact hardware/backend.
No training or fallback has been used. Google Cloud
inventory/quotas/prices and a read-only SSH hardware check are authorized and
completed: existing micro-VMs lack model capacity; one T4/L4 quota is available.
One L4 session is explicitly authorized up to USD 5 and three hours. The new
`g2-standard-4` VM had automatic DELETE after 10,800 seconds and is now deleted;
CUDA 12.9 / driver 580.178.04 and NVIDIA L4 23,034 MiB are verified.
Inference receives a minimal eight-file code archive and source-bearing context
packets only; no evaluator or benchmark gold is uploaded.

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
0002 and localization-v2. The foundation did not alter model evidence thresholds.

## Untuned L4 development baseline

[Report and compact evidence](results/reports/untuned-dev-v2-l4/README.md).
Clean inference code f67e499; pinned CUDA backend 7049ff0; original Qwen and
Q4_K_M revisions/weights/binary/template/input hashes are retained. Synthetic
GPU native rendering, input/output IDs and raw response match both earlier CPU
probes exactly. Three preregistered old tasks passed resource/API checks; then
the new config was frozen before its first dev-v2 generation. Model-layer offload
is 37/37; no context truncation/overflow or native-counter mismatches occurred.
All 60 final prediction records passed schema and checksum checks, and all 192
private run files verified after local transport.

All 60 tasks completed once: 52 valid and eight unknown-path outputs; every
invalid output scores zero. Recall@5 0.656926, strict 33/60, matched ceiling
0.783487. Gain versus matched lexical is 0.428600, repository-block 95% interval
[0.315904, 0.559686]; the preregistered development rule passes. Full-corpus
reference gain is 0.104661, with supplementary post-run interval
[-0.001196, 0.216399]; the advantage over that reference remains uncertain.
Only six exposed development repositories are represented; Verified is untouched.
This does not confirm specialization, substitution, repair quality or economics.

Request wall p50/p95 3.205/4.215 seconds; total request wall 196.445 seconds;
model load 2.009 seconds. Native tokens total 477,333 input / 2,190 output,
including invalid attempts/EOS. Whole-backend CPU is 198.737 seconds; per-task
server CPU and active GPU-seconds remain unknown. All monetary cost/CPS fields
remain null. Start to confirmed VM/disk absence was 46.19 minutes. The list-rate
compute-only scenario is USD 0.5441; setup/probes/collection are included, but
additional charges and actual billing are unknown. The new VM and auto-delete
boot disk are confirmed absent; no paid job remains running from this session.

The initial GPU bind failed through a protected home directory; moving the
unchanged workspace to /opt resolved access without widening model mounts.
A second technical start blocked generation because default logging omitted
full-offload evidence; explicit native trace logging was committed before any
GPU generation. Both starts and their logs remain in the private final archive,
with source-free failure descriptions in the compact report. No model output was
repaired or retried. The old CPU post-inference launcher collection error is also
retained separately. The GPU source/launcher remained immutable during execution.

Forty-six CPU tests, lint/format and shell syntax pass. Exact baseline artifacts,
native audit, fixed primary analysis and checksum evidence are retained for review.
The user requested commit/push on 2026-10-06. Local commits and CPU checks
are complete. Automatic approval review rejected the public push because it
requires explicit confirmation of publishing the L4 report/metrics; push remains
pending that confirmation. Remote CPU CI has not run for these local revisions.
