# Work tracker

Updated: 2026-10-08 (Moscow). Track: Small Specialist. Development baselines, matched 4B/14B comparison and both new-issue validation campaigns are complete; all newly created cloud resources are deleted. Historical preparation entries below retain their original status and date.

| ID | Work | Status | Completion evidence / next gate |
| --- | --- | --- | --- |
| EAI-001 | Local Git and GitHub origin | DONE | main; mks-hash/efficient-agentic-inference |
| EAI-002 | Local planning sources | DONE | Two original files preserved in ignored .develop/ |
| EAI-003 | Bootstrap docs, ADR, schema, benchmark contract | DONE | Initial bootstrap commit a3a7157; versioned schemas validated by runner/tests |
| EAI-004 | CPU lexical runner and synthetic contract fixture | DONE | 14 contract tests, ruff lint/format and locked sync pass; CLI fixture complete |
| EAI-005 | SWE-bench acquisition/reconstruction + patch labeler | DONE_PILOT | Clean-code local and separate-host audits PASS; pinned sources/splits and all 12 tasks prepared/labeled |
| EAI-006 | Frozen full-corpus lexical baseline + candidate ceiling | DONE_PILOT | Full candidate corpus per each of 12 dev tasks; Recall@5 0.541667, ceiling 1; broader population not measured |
| EAI-007 | Untuned small/generalist matrix | ONE_LARGER_CANDIDATE_DONE | clean f0a654c: fresh S Recall@5 0.656926 / strict 33/60; G 0.609120 / 30/60; 120/120 attempted; G−S −0.047806, repo-block 95% CI [−0.079036, −0.028107]; generalist material-gap rule FAIL; held-out substitution/training/economics unconfirmed |
| EAI-008 | Training decision | NO_PILOT_JUSTIFIED_FOR_THIS_CANDIDATE | 14B provides no positive matched gap; frozen ADR 0006 rule FAIL. No training run authorized or performed. Future adaptation needs new independent evidence, accounting/validation gates and a separate budget |
| EAI-009 | Public README positioning and documentation separation | DONE | Research narrative and CPS formula in README; scope/candidates in plan, implementation/check details in reproduction guide |
| EAI-010 | Independent second-host reproduction | DONE | GitHub run 37379561857, clean 397df23; snapshot/input/gold/semantic prediction hashes and metrics match local 0edd9e6 |
| EAI-011 | Broader dev baseline and CPU/system cost accounting | FOUNDATION_VALIDATED | Clean 0bd7571 audit PASS: 60/60 prepared/labeled, 123 identical artifacts, 88638 file hashes; full Recall@5 0.552265 / ceiling 0.985450 / strict 25/60; matched context 0.228326 / ceiling 0.783487 / strict 8/60; phase accounting explicit, no prices or model results |
| EAI-012 | v0.1.0 research milestone release | DONE | Annotated tag at 392722c; public release with evidence, provenance, release-commit audit and checksums; CPU CI 37381457746 and second-host reproduction 37381481917 PASS |
| EAI-013 | v0.2.0 report and release preparation | DONE | Report/README published; package 0.2.0, contract/schemas unchanged; 46 CPU tests, saved-prediction re-evaluation and remote CPU CI 37412035383 PASS; annotated tag e097c22 and public GitHub Release with verified assets; release-commit CPU CI 37412299183 PASS |
| EAI-014 | Matched generalist and cost accounting | DONE_FIRST_COMPARISON | Both weights/native/full-offload/isolation/EOS gates PASS; S 52 valid / 8 invalid, G 49 / 11; fresh S repeats 60/60 semantic records; 900 archive checksum entries PASS; 51.55-minute one-VM session ended, VM/disk absent; partial scenarios recorded, actual/full CPS UNKNOWN; local report ready |
| EAI-015 | New validation membership | DONE_EXPOSED | 20 fixed issues / 5 seen repositories; reconstructed snapshots and contexts match; all four recipes evaluated under the frozen contract; no longer untouched validation |
| EAI-016 | Constrained output on fresh validation | DONE_PRIMARY_RULE_FAIL | 80 research / 32 technical requests; 4B gain 0, strict 9/20 in both arms; 14B gain +0.05 exploratory; all attempts retained, VM/disk absent |
| EAI-017 | Complete candidate-score recipe | DONE_PRIMARY_RULE_FAIL | 30 fresh issues / 4 seen repositories; 120 research / 24 technical requests; S gain −0.330556, G exploratory −0.536111; all score vectors valid; VM/disk absent |
| EAI-018 | Cross-report synthesis | DONE | Source-hashed post-hoc diagnostics; 296 model-report checksum entries verified; no new inference or confirmatory rule |
| EAI-019 | v0.3.0 milestone | LOCAL_READY_PUBLICATION_PENDING | Experimental sources preserved at f167abc; package/lock/runtime 0.3.0, release notes and validation record prepared; 67 CPU tests and 380 saved-attempt re-evaluations PASS; no v0.3.0 publication yet |

## Open decisions before further reference/adaptation work

- A fresh evidence-budget intervention with matched controls and separately frozen membership; the completed validation populations are now exposed.
- Train memberships and broader repository/time controls; dev/final and new validation memberships are frozen.
- SS-H2 margin and SS-H3 quality, fallback and economic targets.
- Full-system cost attribution; any new paid campaign needs its own explicit budget and run authorization.

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
At v0.2.0 release time, independent GPU repetition was NOT_RUN; the later fresh matched comparison is recorded below.

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

## Authorized matched-model session — 2026-10-06

The user authorized one new `eai-generalist-l4-20261006` g2-standard-4/L4 session
in us-central1-a, USD 5 maximum and three-hour automatic DELETE backstop, with
early collection/deletion after completion. Execution uses a minimal clean
`f0a654ca81a8a7a17151ea37e3ec3855377ac728` archive; both model configurations
freeze after resource probes and before research generation. New GPU/model evidence
is NOT_RUN until the gates finish; actual monetary charges remain UNKNOWN.
Existing workloads are excluded from all provisioning/cleanup actions.

Provisioning returned capacity errors twice in us-central1-a and once in each
of us-central1-b, us-central1-c and us-east4-a. Each failed request was followed
by an absence check before the next attempt. The single allocation succeeded
in us-east4-c (instance 690047964406146351), with the same g2-standard-4/L4,
pinned image and three-hour DELETE policy. This availability fallback changes
location only; both matched arms use this host, with host/region differences from
the historical run retained as replication limits. Reviewed us-east4 on-demand
compute rate is USD 0.704517824/hour; it is a scenario rate, not an actual charge.

Execution update (2026-10-06 UTC / 2026-10-07 Moscow): both downloaded weights
passed their pinned byte/hash checks; four synthetic/old-dev resource probes
passed. Full offload is 37/37 for S and 41/41 for G; G native non-thinking suffix
passed. Both research configurations froze at 21:10:17 UTC before the first
new dev-v2 generation. This was the execution state at freeze; both completed outcomes are recorded below.

## Completed matched comparison — 2026-10-06 UTC / 2026-10-07 Moscow

[Local report](results/reports/generalist-dev-v2-l4/README.md): both 60-task arms
finished with all native decoding/token/EOS gates and physical isolation PASS.
S replicated all 60 historical ranked-path/disposition/failure records and its
Recall@5 0.656926 / strict 33/60. G measured 0.609120 / 30/60, with 9 unknown-path
and 2 duplicate-path invalid answers (S: 8 unknown-path answers). Both failures
and unsuccessful valid tasks remain in denominators. G median request wall is
11.545s versus S 3.221s; this is one serial fixed-host batch, not a serving study.

The preregistered positive generalist-gap rule fails: G−S −0.047806, paired
repository-block 95% interval [−0.079036, −0.028107]. This candidate/configuration
does not justify an adaptation pilot. It is not a validated stronger generalist,
and no SS-H1/generalization/repair/economic substitution claim is made.
Supplemental validity/oracle diagnostics are explicitly post hoc and do not alter
the primary rule, dataset or grader. Validation-v1 and Verified were untouched.

The final raw archive is 7,643,248 bytes, SHA-256
`05ee9d882296c294a156a5c780458aaf3afc23f7a40a2e03983155fd7139816e`;
900 checksum entries verified. Both VM and its auto-delete boot disk were absent
at 21:27:58.460987 UTC; existing instance identities remained. The conservative
provider-start-to-confirmed-absence wall boundary is 3,093.153987s (51.55min).
Compute-only list-rate scenario is USD 0.605328; actual charges are UNKNOWN.
Region-specific storage rate is USD 0.000150685/GiB-hour (0.11/GiB-month); IP
scenario uses USD 0.005/h before account credits. Network/external preparation/
other costs remain null, so complete actual and scenario CPS remain unknown.
Standalone cold lifecycle scenarios replay shared phases and observed post-probe
load/request timings; no independently cold-cache startup was measured.

Source-bearing raw outputs remain unchanged in ignored local storage. Source-free
review exports redact raw_output and retain original prediction/archive hashes;
re-evaluation produces byte-identical per-task metrics. v0.1.0/v0.2.0 release
artifacts and previously frozen reports remain unchanged. The new report and
documentation are local review changes; no new release or public push occurred.

Final local checks PASS: 53 CPU tests, ruff lint/format, diff whitespace, 49
new report file checksums, 120 prediction schema/original-field comparisons,
120 native trace hashes, both accounting recalculations and local document links.
The frozen protocol body remains byte-identical from its first treatment section
to the end relative to f0a654c. Verification is in the report verification.json.

## Reliability validation preparation — 2026-10-07

User approved preparing the next reliability/validation milestone. [ADR 0007](decisions/0007-constrained-output-validation.md)
and [campaign contract v1](docs/experiments/reliability-validation-v1.md) prescribe
four fresh arms: each existing model with free and candidate-constrained generation.
Prompt/context/grader and localization-v2 schemas remain unchanged. Only constrained
requests add a gold-blind JSON schema. The pinned backend lacks uniqueItems;
duplicates remain strict failures. S within-model Recall@5 is the single primary;
G change/interaction are exploratory. No adaptation or paid run is authorized.

[Preparation checks](docs/experiments/reliability-preparation-checks.json): 60 CPU
contracts, lint/format and two actual isolated synthetic S probes PASS. Rendered
prompt and all 192 input IDs match; both outputs are valid and the constrained
response records an eager grammar containing only the declared path literals.
This establishes implementation only; G constrained/GPU/validation quality are NOT_RUN.
The first sandbox launcher failed before inference at network-namespace creation;
the approved isolated local invocation succeeded, and the failed attempt is retained.

Initial preparation wording counted six repositories. The immutable membership
actually has four issues in each of five known repositories, with no remaining
marshmallow issue. Corrected that descriptive count and retained both preparation
bundles; no IDs, treatments, thresholds or analysis rules changed. Corrected freeze
SHA-256 de0031f856296d6c82955b25da27e7781bb6eef5d277f623c0d3ff67e3b9f07f.

The initial offline reconstruction prepared 1/20 because 19 exact base commits
were absent. That full snapshot/log remains retained. Fetching exact pinned objects
produced a complete 20/20 snapshot, followed by an offline rebuild with all 18,934
files byte-identical. Canonical packet bytes and 20 semantic context records match.
Input SHA-256 03ddfcbecd265350e6edc31a0536efa56cf5530bf8ed86a515bce81df82d9b7e.
Gold SHA-256 1f9419691c93806d1c290b1b8ff733a669e955cda86d277263c3e737d98d1001;
labels are local-only, not scored or transported to inference. Validation has zero
model attempts; Verified labels/predictions remain NOT_RUN. Preparation hashes
were frozen before reconstruction; final execution identities still need host gates.

A free read-only BigQuery dataset listing succeeded with no visible datasets in
the current GCP project. No invoice/usage evidence was obtained; exports could exist
elsewhere. Actual charges/full CPS remain UNKNOWN; no service/export was enabled.
The concrete local proposal `.develop/gcp-reliability-l4-proposal.md` requests one
new L4 allocation, USD 5 / three-hour DELETE backstop, 80 research slots, incremental
collection and early VM/disk deletion. It is NOT_AUTHORIZED, and no VM was created.
All changes remain local review material; no new push/tag/release was performed.

## Authorized reliability session — 2026-10-07

The user approved the proposed one-L4 allocation up to USD 5 and three hours,
conditional on readiness, and requested useful additional checks in the same VM.
[ADR 0008](decisions/0008-supplementary-session-checks.md) adds a separately versioned
[technical contract](docs/experiments/reliability-session-checks-v1.md): 32 fixed
synthetic/old-task replay requests and passive one-second GPU telemetry. The four
research arms, 80 validation slots, prompt/context/decoder/grader and primary
criterion remain unchanged. All technical gates and the joint execution freeze
precede validation generation. No new model, tuning, population or publication.
Resource creation and actual GPU/quality evidence remain NOT_RUN until execution.

Allocation update: capacity failures in all original supported zones and us-east1
were retained with VM/disk absence checks (us-east4-b is unsupported and is removed
from future proposals). The same single L4/g2-standard-4 allocation succeeded in
us-west1-a, instance 2006722488811859971, with maxRunDuration 10800s / DELETE and
auto-delete disk, no service account. Provider last start is 2026-10-07T18:27:03.636Z;
the derived three-hour termination boundary is 21:27:03.636Z. Current reviewed
us-west1 on-demand compute rate is USD 0.706832276/h, scenario only. The transport
archive is 227,034 bytes, SHA-256 e72a5a6ead1bec8d2f0a46a5214889499cee618c76972d4e7191d934ff8edc80,
with an explicitly dirty-base but immutable 11-member inference archive; exact
source hashes, not the base commit alone, identify execution. Other VM identities
are excluded. GPU/quality gates remain NOT_RUN until actual checks finish.

Execution started at 18:30:16 UTC in `eai-reliability-campaign.service` with a
150-minute process cap, below the provider's three-hour DELETE backstop. The
provider's observed termination timestamp is 21:26:54.441362 UTC (nine seconds
earlier than the last-start-derived estimate); the cleanup reserve covers that
difference. Transport integrity passed; CUDA compilation is in progress. No
validation inference/evaluation has run at this execution checkpoint. Local
collection/audit/report scripts are separately frozen before validation output;
23 preregistered research files and the 45/49-file earlier report checksum sets
remain unchanged. This is an execution checkpoint, not a completed result.

## Completed reliability validation — 2026-10-07

[Local report](results/reports/reliability-validation-v1-l4/README.md): all four
20-task arms completed once, after all 32 separately preregistered technical
requests passed. Full offload, isolation, native counters/decoding/templates/EOS,
effective eager grammar and immutable source/config provenance PASS. Twelve
same-backend replay pairs match token IDs/raw output/paths/dispositions. Both
modes have identical prompt and input IDs for all 20 validation issues per model.
The joint execution freeze was 19:07:26 UTC, before research generation.

S-free/S-constrained both Recall@5 0.633333, strict 9/20, valid 19/20; every
observed per-task Recall@5 difference is zero. Primary material-improvement rule
FAIL; its [0, 0] sample bootstrap interval is not a population-equivalence claim.
G-free 0.595833 / strict 8/20 / valid 16/20; G-constrained 0.645833 / 9/20 /
17/20. Exploratory G gain +0.05, five-repository-block interval [0, 0.15]; one
task accounts for the Recall@5 improvement. Candidate ceiling 0.879167 for all
arms. Unknown-path/duplicate failures respectively: S-free 1/0, S-constrained
0/1, G-free 2/2, G-constrained 0/3. No outputs were repaired or retries selected.
The unchanged evaluator scores all invalid answers zero. Validation-v1 is now
exposed; future recipes require new frozen validation. Verified remains untouched.
No training/generalization/issue-repair/economic substitution claim is established.

Observed p50/p95 request seconds: S-free 3.068/4.485, S-constrained 3.068/4.965,
G-free 12.146/14.448, G-constrained 12.155/14.437. Sampled peak GPU memory is
4,942 MiB for S and 11,006 MiB for G; one-second telemetry may miss peaks and
does not establish active GPU-seconds. These are serial fixed-host observations,
with post-probe caches and fixed order; not a concurrency or cold-cache benchmark.

All six unique milestone archives were collected and checked; final 6,471,308-byte
raw archive SHA-256 2a648ab09a90a64af7ded8a04664d8757299849c7fd8d1ec03d364c63f584728,
980 checksum entries verified. Evaluation opened local gold only after complete
four-arm collection; source-free exports re-evaluate to identical per-task metrics.
The new VM and boot disk were confirmed absent at 19:22:39.443641 UTC, with
existing instance/disk identities preserved. Provider last start to confirmed
absence is 3,335.807641 seconds (55.60 minutes), including setup/technical work,
idle/transfer/cleanup. No paid resource remains from this campaign.

Inclusive list-rate compute scenario USD 0.654960; compute/storage/IP subtotal
USD 0.672287. Actual charges, missing components and full-system CPS remain
UNKNOWN/null. Four standalone 20-task lifecycle scenarios replay common phases
and each model download, exclude explicitly recorded technical work/archives,
and are not additive portions of the shared bill. Original raw artifacts/failures,
prior reports, frozen contracts and published tags remain unchanged. The new
report and documentation are local review changes; no new push/tag/release.

Final verification PASS: 103 compact report files / 485,234 bytes checksummed,
80 prediction schema/original-field comparisons, 80 native trace hashes, 80
byte-identical re-evaluated per-task metrics, four accounting recalculations,
62 updated-document local links, lint/format (74 Python files) and diff whitespace.
The 23 preregistered research files and six pre-output postprocessing scripts remain
byte-identical to their freezes. Sixty CPU contracts passed during preparation;
no implementation change followed those checks. Adaptation, broader validation,
new paid sessions and publication remain separate future decisions.

## Score-ranking preparation — 2026-10-07

The user accepted preparation of a unique-ranking recipe and fresh validation.
[ADR 0009](decisions/0009-score-vector-ranking.md) and the
[new protocol](docs/experiments/score-ranking-validation-v2.md) define a complete
candidate-score vector, without repairing the historical path parser or relaxing
localization-v2. This compares the entire prompt/representation/mapping recipe.
Primary S-scores minus S-paths, exploratory G, 120 planned research slots; no
new paid/validation/training/publication authorization follows from preparation.

Two metadata-only freezes produce identical `validation-v2` bytes: 30 fresh
issues (8 pvlib, 8 pydicom, 7 astroid, 7 sqlfluff), excluding both dev splits,
validation-v1 and Verified IDs/normalized equivalents. Split SHA-256
ec782a79b046dff8731f3d5570aebd647a5bd47eaf449ebd36dc884d33fe4635.
Four seen repositories remain eligible; this is not repo/time generalization.
The completed 29-file preparation freeze precedes repository reconstruction;
an earlier incomplete analysis snapshot is retained, superseded before validation.
CPU unit contracts PASS (67), lint/format PASS (35 Python files). Short isolated
synthetic probes and exact-base snapshot reconstruction are in progress. Native
GPU/14B score output, validation quality and actual cost remain NOT_RUN/UNKNOWN.

Preparation completed: [checks](docs/experiments/score-ranking-preparation-checks.json).
All seven isolated synthetic CPU requests passed format/native/schema/binding/EOS
gates, including zero/two/twenty candidates. Historical path request, native prompt,
input/output IDs, raw response and disposition match the previous CPU probe exactly.
Three matched user messages are identical across recipes; full system prompt and
native input IDs differ as expected. These are implementation checks, not semantic
localization evidence. Every raw response and timing journal remains local.

Both fresh-directory base snapshots prepare and label all 30 issues; 63 snapshot
artifacts match byte-for-byte and all 52,106 exported regular-file contents were
verified across both snapshots. Inference packets are byte-identical; context
provenance matches excluding only measured cpu_ms/wall_ms. An initial overbroad
context-journal byte comparison failed on those timings; the failed audit is
retained alongside the corrected measurement-aware check. No research input,
output or timing journal was changed. This is a same-host offline rebuild,
not independent-machine reproduction.

Preparation freeze SHA-256
d7f048f4f33f17d6a928d63404389781ec127b058c9f2e725b747bbd3c3fbee6;
all 29 source/config/contract identities remain unchanged. Matched packet SHA-256
efc0b4f8620558087103242e66d3314a142b32fdf17737b1c8837cbe45a84b91.
All 197 prior report checksums remain valid. Validation-v2 has zero model attempts
and zero quality evaluations; gold stays separate/untransported. GPU/14B score
gates remain NOT_RUN, cost UNKNOWN, paid execution/publication NOT_AUTHORIZED.
No VM, training, commit/push/tag/release was performed during this preparation.
Final checks: lint/format (35 Python files), diff whitespace, 52 local document
links, synthetic example checksums and clean CPU backend exits PASS. Exact toy
probe inputs are retained in examples/score-ranking-v1 for reproduction; they
establish no model-performance claim.

## Prepared score-ranking L4 session — 2026-10-08 (local date)

[ADR 0010](decisions/0010-score-session-preflight.md) adds a separately frozen
[technical supplement](docs/experiments/score-ranking-session-checks-v1.md), without
changing the 29-file research freeze: 20 synthetic boundary/greedy-repeat requests
and four exposed dev-v1 trace checks, separate from 120 validation slots. Technical
gates precede the joint execution freeze; wrong semantic answers and path duplicates
are retained without tuning/repair. G-score GPU/native and fresh quality remain NOT_RUN.

The concrete ignored proposal `.develop/gcp-score-ranking-l4-proposal.md` requests
one NEW us-west1-a L4/g2-standard-4 allocation (same-region capacity alternative
us-west1-b), USD 5 maximum / three-hour automatic DELETE backstop, early deletion,
100 GiB auto-delete boot disk, no service account and a 150-minute controller cap.
Read-only preflight confirmed the pinned image READY, regional L4 quota 1/usage 0,
and only the existing prx-us/secure-us instances. Quota does not establish capacity.
Current primary-source list-rate compute/disk/IP three-hour subtotal is USD 2.176593,
scenario only; actual spending and missing components remain UNKNOWN/null.

Transport is 261,443 bytes, SHA-256
d9d1dcd25180f7dd3a8b29856442b77cdded3605ea897bdb84e27a6e39899997,
with a twelve-member immutable minimal inference archive and three allowlisted
packets (30 validation / 5 synthetic / 1 old issue). No gold/evaluator/full repos,
upstream dataset, weights, Git history or credentials are included. The dirty base
revision is supplemented by exact archive/member hashes. New launcher tests PASS
(six simulated CPU contracts; initial fixture-import failure retained and corrected).
The download loop and independent provider/controller limits reserve cleanup time;
collection keeps immutable technical/arm/final-or-failure milestones.

The new session is NOT_AUTHORIZED. No paid resource, validation prediction,
training, commit/push, public claim or release was performed in this preparation.
Prior completed-session paid budgets do not authorize this allocation.

## Score-ranking session authorized — 2026-10-08 (local date)

The user explicitly authorized the proposed NEW L4 session: USD 5 maximum,
three-hour provider DELETE limit, 150-minute controller limit, 120 validation
attempts plus 24 separate technical checks, artifact collection and deletion of
the allocated VM and auto-delete boot disk. The previous NOT_AUTHORIZED entry
records the preparation state; the new authorization is retained separately in
ignored `.develop/score-ranking-l4-session/authorization.json`. Publication and
training remain outside this authorization. The frozen transport is unchanged.

At execution, both authorized zones us-west1-a and us-west1-b returned
ZONE_RESOURCE_POOL_EXHAUSTED_WITH_DETAILS. Read-only checks after each failed
creation confirm no matching VM or boot disk. Successful allocations: zero;
research/technical model requests: NOT_RUN. Geographic fallback clarification
is pending; budget and frozen research inputs remain unchanged. The independent
gold-free audit and post-collection evaluation/report wiring are prepared locally.

A single bounded retry within the approved geography obtained the NEW L4 in
us-west1-a. The geographic clarification is obsolete; no geographic expansion
was used. VM ID 8728510203003864785, provider DELETE and disk auto-delete verified.
Frozen inference package is now being launched; gold remains local.

Authorized execution is RUNNING under systemd and the provider deadline.
The 261,443-byte transport checksum passed on the VM before extraction; one
VM is allocated in us-west1-a. CUDA backend compilation precedes the separately
preregistered technical gates. Fresh validation quality remains NOT_RUN until
all four arms finish and are collected. Actual spending remains UNKNOWN/null.

## Score-ranking validation completed — 2026-10-08 (local date)

One approved us-west1-a L4 allocation completed the exact frozen four-arm campaign:
120 fresh research attempts plus 24 separate technical requests. Capacity failures
in a/b and one successful bounded a retry are retained. The geographic clarification
became obsolete; no other region/zone or second allocation was used. All six
technical/arm/final immutable archives were collected and checksummed. Final raw
archive SHA-256 c9bd93a43b3ed9071fda3140335afb5d653fc40b78a01b059461a158c4d85207;
1,128 nested checksum entries PASS. Source/native/isolation audit PASS for all
144 native requests; all 29 original research identities remained unchanged.
Gold was evaluated only after complete four-arm collection.

[Local report](results/reports/score-ranking-validation-v2-l4/README.md):

| Arm | Recall@5 | Strict@5 | Valid |
| --- | ---: | ---: | ---: |
| S-paths | 0.652778 | 15/30 | 30/30 |
| S-scores | 0.322222 | 7/30 | 30/30 |
| G-paths | 0.675000 | 17/30 | 29/30 |
| G-scores | 0.138889 | 4/30 | 30/30 |

Primary score-minus-path gain −0.330556, four-repository-block 95% interval
[−0.575269, −0.166667]: numerical/primary improvement gate FAIL, independent
technical/provenance PASS. The 14B gain −0.536111 is exploratory. All-attempt
candidate ceiling 0.802778 is common. Integer grammar and unique mapping work;
this complete score recipe damages ranking quality. Post-run diagnostics show
one/15 empty score rankings for 4B/14B and 14/5 top-five boundary-tie vectors;
these do not establish causality or select a revised recipe. No repairs/reruns.
Validation-v2 is now exposed and excluded from future training/confirmation.

VM ID 8728510203003864785 and disk ID 6323082686200743632 were deleted; absence
confirmed 2026-10-08 01:19:11 MSK and checked again directly after an interrupted
process-status handle. Existing prx-us/secure-us identities preserved. Inclusive
allocation boundary 55.87 minutes; compute list-rate scenario USD 0.658150,
compute/storage/IP subtotal USD 0.675561 (scenario, not invoice). Actual spending,
active GPU-seconds and full CPS remain UNKNOWN/null. No paid resources remain
from this campaign.

Independent local review verification PASS: all 120 source-free prediction rows
validate against schema and preserve every original field except raw_output;
all 120 per-task metrics are byte-identical to original evaluation, native traces
and four accounting ledgers verify, previous three report checksum sets unchanged,
local report links/credential scan/cleanup PASS. CPU launcher invariants: six PASS;
67 repository CPU checks passed in preparation, not repeated without source changes.
The first report export failed before writing results on a legacy flat IP-rate
field; corrected to the retained nested rate review, with failed log/empty directory
preserved. No inference/evaluator/statistical rule or measured artifact was edited.
Publication, commit/push/tag/release and training were not performed.

## Cross-report synthesis — 2026-10-08

At the user's request, reviewed the lexical, untuned, matched-model, reliability
and score reports together with the relevant contracts. Added
[research synthesis](docs/technical-reports/localization-synthesis-2026-10-08.md),
[source-hashed post-hoc diagnostics](docs/technical-reports/localization-synthesis-analysis.json)
and a reproducible report-only analysis script. Original report bytes, inference,
evaluator, protocols and acceptance rules remain unchanged. All 296 model-report
checksum entries PASS; 17 analysis-source hashes, three paired matrices/oracle
bounds, four score-loss conservation checks and six synthesis links verified.
The original dev-v2 paired contrast/interval reproduces exactly. Script lint and
format PASS; formatting leaves every numerical diagnostic unchanged.

Post-hoc constrained cross-model G-minus-S gains are +0.0125 on validation-v1
(interval [-0.15, +0.166667]) and +0.022222 on validation-v2 paths
(interval [-0.083333, +0.154762]). These do not establish equivalence or a new
confirmatory model winner. Perfect choice between observed S/G outputs yields
strict 34/60, 12/20, 18/30 on dev-v2 / constrained validation-v1 / validation-v2
paths; gold-aware oracle only, not a router or economic result. Latest ideal
candidate-bound top-five strict ceiling is 21/30 versus observed S 15/30.
Both models' score losses are negative within all four repositories; S nonempty
score answers contribute -0.319444 of its -0.330556 all-task recall difference.

Recommendation: keep 4B path generation as the research comparator; stop this
score recipe as an improvement; investigate evidence budget/coverage/excerpts
with matched lexical controls and fresh, separately frozen evaluation membership.
Training, measured full CPS, repository/time generalization and downstream repair
remain untested. No new inference, cloud allocation, gold-patch/label access,
training, commit/push or publication occurred during synthesis.

## v0.3.0 local release preparation — 2026-10-08

The user requested commits and a release decision. Preparing
`v0.3.0 — Localization Baselines and Negative Results` around the completed
matched-model, output-constraint and candidate-score campaigns plus their synthesis.
All 67 CPU tests, repository lint/format and diff checks pass. Re-evaluation of
all 380 saved model attempts across eleven arms reproduces both per-task metrics
and summaries byte-for-byte. Five report envelopes verify 320 checksum entries;
all 29 files in the score research preparation freeze match exactly before
release version metadata changes. Seventeen synthesis-source hashes and 139
local links pass. Pending public files pass size and credential-pattern checks;
ignored planning/data/weights/raw archives are excluded.

First preserve the exact experimental sources in a local commit, then change
package metadata to 0.3.0 and record that difference explicitly. Contract v2,
artifact schemas 2.0.0, historical measurements and acceptance rules remain
unchanged. Release preparation runs no new inference or cloud resources.
Push, tag publication and GitHub Release are pending; no v0.3.0 is published.

Experimental sources are now preserved at
`f167abc90ceac2ab93b9b79076244fa34c316dda`; every frozen file matches the
score preparation snapshot at that commit. Release metadata is 0.3.0 and
locked offline installation passes. The only source difference from that snapshot
is the explicitly recorded `__init__.py` version string. All 67 tests and the
380-attempt byte-identical evaluation check pass again after this change.
See [milestone notes](docs/releases/v0.3.0.md) and
[validation record](docs/releases/v0.3.0-validation.json). Exact release-commit
provenance and an evidence archive with member checksums are prepared separately
under ignored `.develop/releases/v0.3.0/`; publication state is tracked outside
the immutable historical research report envelopes.

The two prepared commits were pushed to main. GitHub
[CPU CI 37829046763](https://github.com/mks-hash/efficient-agentic-inference/actions/runs/37829046763)
passes at `d7d4c826dec68e70837b9653df50215b47f918af`, including both supported
CI Python versions. Changelog now indexes the v0.2.0 and v0.3.0 milestones.
Final release-commit CI, annotated tag, asset publication and download verification
follow before marking the release published.
