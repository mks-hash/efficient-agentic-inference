# ADR 0005: Bounded L4 execution for the untuned baseline

Date: 2026-10-06. Status: accepted; explicit user authorization received before provisioning.

## Decision

Run one dedicated on-demand `g2-standard-4` in `us-central1-a`, with one NVIDIA
L4, up to USD 5 total and three hours from allocation. The VM has no service
account/scopes, no automatic restart, and an auto-delete boot disk. Automatic
instance DELETE after 10,800 seconds is a backstop; save artifacts incrementally
and delete the VM/disk as soon as collection finishes. A 9,000-second job timeout
leaves a collection reserve. Existing cloud workloads are outside this session.

The old CPU smoke takes several minutes per issue; a 60-task CPU campaign would
exceed the provisional two-hour limit. L4 is available within checked quotas.
A100 is not available within those regional quotas, and its higher whole-VM price
requires a measured total-session speedup to justify substitution. No A100/H100
performance is assumed or measured by this decision.

Use the same pinned Qwen3-4B-Instruct-2507 Q4_K_M artifact, native template,
512-token greedy decoding, prompt, and `bm25-top20-prefix1200-v1` packet. Backend
source remains `7049ff0cbeb1f5ead231de4522af6b75d8d773c0`; CUDA is enabled and the
binary, compiler, cache and hardware identities are recorded independently.
The initial transported inference code is clean
`948d3e81a4bf56d1a7ac1b6bd0e69c17a1cdb121`. Before any GPU generation, two
technical starts failed: protected home-directory traversal, then a missing
full-offload log at default verbosity. The workspace moved to `/opt` without
loosening the model namespace. Library INFO is trace-level in this backend;
explicit `--log-verbosity 4` retains full-offload evidence. A new clean inference
archive/config identity records that instrumentation correction before dev-v2.
Both failed starts are retained. Model, prompt, evidence and decoding are unchanged.

## Sequence and gates

A synthetic API probe precedes the first three old dev-v1 context rows, selected
before GPU outputs: marshmallow-1810, pvlib-1165, pydicom-811. These resource
checks do not select tasks or tune quality. Require physical filesystem/network
isolation, full nonzero X/X layer offload, native token/effective-setting agreement,
no context truncation and no runtime failure before the new campaign. Invalid
localization outputs remain recorded failures; they are never repaired/retried.

Context capacity is 16,384 tokens. Startup deadline is 180 seconds, request
wall deadline 120 seconds. Synthetic/old-resource campaign budgets are 120/600
seconds after readiness. Freeze the new 60-task config before its first inference;
its campaign budget is 3,600 seconds. No generation occurs with evaluator, gold,
Git history, source repositories, or external network mounted. Only the minimal
inference archive and permitted context packets reach the model VM.

## Comparability and interpretation

This is a separate hardware/backend execution treatment, not a new dataset,
prompt or grader. GPU kernels can change greedy predictions. Different CPU/GPU
deadlines prohibit attributing a quality difference solely to hardware. Keep all
60 selected tasks in the denominator, including errors, output exhaustion,
timeouts and budget-exhausted unattempted tasks. An incomplete campaign is not a
completed baseline. Do not modify frozen dev-v2 membership after model exposure.

Evaluate locally after saved prediction records are complete, against the same
separate gold as both lexical controls. Apply the existing paired repository-block
decision rule unchanged. Report the full-corpus reference separately from the
matched-context comparison. Localization success does not establish repair success,
model specialization or end-to-end agent economics.

GPU utilization seconds and per-task server CPU remain unknown. Record allocation
and model-load/request wall time separately. List-rate allocation scenarios are
not invoices or cost per successful task; unknown monetary values remain null.
Training, prompt tuning, fallback and publication are outside this authorization.
