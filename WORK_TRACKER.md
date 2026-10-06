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
| EAI-013 | v0.2.0 report and release preparation | DONE | Report/README published; package 0.2.0, contract/schemas unchanged; 46 CPU tests, saved-prediction re-evaluation and remote CPU CI 37412035383 PASS; annotated tag e097c22 and public GitHub Release with verified assets; release-commit CPU CI 37412299183 PASS |
| EAI-014 | Matched generalist and cost accounting preparation | PREPARED_PAID_AUTHORIZATION_PENDING | Pinned 14B candidate, ADR 0006, matched protocol, opt-in non-thinking/native suffix gate, separate cost ledger/CLI; 53 CPU tests and native 4B synthetic parity PASS; actual generalist/GPU/CPS NOT_RUN/UNKNOWN |
| EAI-015 | New validation membership | RESERVED | 20 deterministic same-repository issues; dev-v1/dev-v2/Verified overlaps and normalized equivalents excluded; byte-identical freezer rebuild; labels/predictions NOT_RUN |

## Open decisions before generalist/adaptation

- Stronger generalist revision, license/access, resource fit and explicit run budget.
- Train memberships and broader repository/time controls; dev/final and new validation memberships are frozen.
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
The user explicitly authorized push to main and publication of the L4 report
and its metrics on 2026-10-06, resolving the earlier automatic approval review
rejection. All seven prepared commits through b3fe107 were published to main.
Remote CPU contracts passed on Python 3.11 and 3.14:
[GitHub Actions run 37411402418](https://github.com/mks-hash/efficient-agentic-inference/actions/runs/37411402418).
This publication-status update does not change the frozen experiment artifacts.

## v0.2.0 preparation

The user authorized push to main on 2026-10-06 after discussing the next milestone.
The [technical report](docs/technical-reports/untuned-dev-v2.md) explains the matched
comparison, supplementary full-reference uncertainty, invalid answers and resource
boundaries. The figure reads saved comparison records only; it adds no new analysis.
README now places the development results nearer the top and links the report and
[milestone notes](docs/releases/v0.2.0.md). The results index and research plan now
describe the completed model campaign rather than its historical NOT_RUN state.

Package/lock/runtime version metadata is 0.2.0; benchmark contract and schema
versions are unchanged. No runtime behavior changes; the original f67e499 source
identity and experiment bundle bytes remain intact. All 46 CPU tests, lint and
format pass; a fresh local re-evaluation of saved predictions reproduces the exact
original summary and per-task metrics. The figure was visually checked. GPU
inference repetition is NOT_RUN; no paid resources were started. The preparation
was published at 9b1b109; [remote CPU CI](https://github.com/mks-hash/efficient-agentic-inference/actions/runs/37412035383)
passed on Python 3.11/3.14. A source-free evidence archive, exact-commit provenance
and SHA256SUMS are prepared under ignored `.develop/releases/v0.2.0/`; asset
membership and hashes are verified against committed bytes. The user explicitly authorized tag and GitHub Release publication on 2026-10-06.

[v0.2.0 — Untuned Small-Model Localization Baseline](https://github.com/mks-hash/efficient-agentic-inference/releases/tag/v0.2.0)
is published as Latest. The annotated tag remains at
`e097c22f571d4b5b38e8095abfbce9d24fe5f465`;
[release-commit CPU CI](https://github.com/mks-hash/efficient-agentic-inference/actions/runs/37412299183)
passed on Python 3.11/3.14. Three uploaded assets (evidence archive, provenance,
SHA256SUMS) were downloaded and verified byte-identical before publication. The
85-file archive is 318,435 bytes, SHA-256
`08d59ec2119da6d037d76b7be157c0fbb41feaecdc3875a833488256887bc0a9`.
The post-publication tracker update does not move the tag or replace assets.
Independent GPU repetition remains NOT_RUN; no additional paid run occurred.

## Matched generalist preparation

The user asked to continue with a bounded generalist/accounting milestone.
[ADR 0006](decisions/0006-matched-generalist-and-cost-accounting.md) and
[protocol](docs/experiments/generalist-dev-v2.md) select one Qwen3-14B Q4_K_M
non-thinking candidate plus a fresh 4B replication. No claim that the larger model
is better is made. API metadata pins the official/quantized revisions, Apache-2.0
license and expected 9,001,753,984-byte weight hash; actual download/hash/fit/output
gates remain NOT_RUN. The quantizer's exact upstream conversion revision is UNKNOWN.

The runner adds opt-in template kwargs, server reasoning off and a verified native
closed-think suffix; the historical default request is unchanged. The config
freezer accepts an explicit base config. Fifty-three CPU tests and lint/format pass.
An actual isolated 4B CPU synthetic probe matches historical rendered prompt,
192 input / 7 output token IDs and raw output. It is implementation evidence only.
The [preparation audit](docs/experiments/generalist-preparation-checks.json) retains
hashes/isolation and explicitly separates unrun model gates.

[Cost accounting v1](docs/cost-accounting-v1.md) separates joint research spending
from standalone deployment scenarios and preserves missing charges, unknown labels,
zero successes and failed-task denominators. Its schema/CLI and examples are CPU
software fixtures. Real ledgers start with every charge null; billing evidence is
not invented from wall time or pooled VM invoices. Inference v2 schemas, gold,
old result bytes and published tags are unchanged.

`validation-v1` reserves 20 new issues under the existing gold-blind selection
policy, with an identical fresh-directory rebuild. It is same-repository validation,
not repository/time generalization. No labels or predictions were produced; Verified
remains reserved. Future training must exclude these reserved instances/equivalents.

Read-only cloud checks find one unused regional L4 quota and the pinned image READY;
capacity is not guaranteed. The concrete ignored proposal is
`.develop/gcp-generalist-l4-proposal.md`: one new L4 VM, two 60-task arms, USD 5 /
three-hour requested cap, resource gates before research, incremental collection
and confirmed VM/disk deletion. The old one-session authorization is complete.
This new paid session is NOT_AUTHORIZED and has not been provisioned. Training,
prompt changes, retries/fallback and additional hardware are outside this proposal.

Preparation was published at de4752d; [remote CPU contracts](https://github.com/mks-hash/efficient-agentic-inference/actions/runs/37524034350)
passed on Python 3.11/3.14, including the new synthetic accounting CLI. No paid
resource has been created; explicit authorization of the proposed session remains
the next gate.
