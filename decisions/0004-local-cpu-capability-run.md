# ADR 0004: Local CPU capability run before accelerator benchmarking

Date: 2026-10-06. Status: accepted for local execution.

## Decision

Use Qwen3-4B-Instruct-2507, Q4_K_M, with the pinned llama.cpp revision from
`configs/untuned-dev-v2.json` on the local i5-7600 CPU. No paid resources, training,
output repair, retries or fallback. Build and weights remain ignored. Record the
actual binary checksum, compiler flags, native chat template and hardware.

Validate API/token provenance with synthetic input, then run the existing 12
exposed dev-v1 instances for resource and format checks. Do not use new dev-v2
model outcomes to choose prompts, context or decoding. Smoke results are not an
independent quality estimate. All attempts and failed API probes remain retained.

The smoke request deadline is 600 seconds, campaign deadline 3,600 seconds after
model readiness, and startup deadline 180 seconds. Context capacity is 16,384;
input plus the 512-token output reserve must fit without truncation. Freeze a
separate dev-v2 execution configuration before generation. Use measured dev-v1
request time to decide whether all 60 fit a reasonable local CPU campaign; report
an incomplete campaign if a time budget prevents execution. Never silently remove
unattempted instances or restart failures. Selection and both lexical controls
remain unchanged.

## Isolation and evidence

Run the client and backend in the same private Bubblewrap filesystem/network
namespace. Mount only system runtime, four inference modules, one canonical task
file, the pinned configuration/prompt, verified model/binary and fresh output.
The evaluator, gold, Git state and repository checkout are absent. A probe in the
same namespace must establish hidden project/evaluator and no external route.

Use the backend's native renderer and tokenizer, save rendered messages, exact
input/generated token IDs, streamed chunks and final backend counters. Require
strict JSON, unique supplied paths, at most ten predictions and EOS completion.
Reject context truncation, output exhaustion or effective configuration mismatch.
Received output token counts on interrupted requests are lower bounds; backend
compute after a disconnect cannot be inferred from client counters.

## Comparability

This adds an execution treatment, not a changed localization contract. Compare
against matched lexical evidence and full lexical separately. CPU latency applies
to this quantization/backend/hardware and includes rendering, tokenization,
prefill, decoding and validation. Model load/warmup and context preparation have
separate accounting. Record server process CPU time for its whole lifetime;
per-task server CPU time and dollar costs remain null. This campaign cannot
establish GPU economics, unquantized quality or issue repair performance.
