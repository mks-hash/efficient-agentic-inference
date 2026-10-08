# Reliability session checks — supplementary contract v1

Prepared 2026-10-07, before any validation prediction. This supplements
[reliability-validation-v1](reliability-validation-v1.md) without changing its
population, treatments, primary criterion, analysis or evaluator.
[ADR 0008](../../decisions/0008-supplementary-session-checks.md).

## Fixed tests, separate from validation

For each of the four model/constraint arms:

- One existing synthetic temperature packet: native rendering/counters/EOS,
  full offload and isolation. The two modes must have identical rendered prompt
  and input token IDs within a model.
- A six-record technical replay packet from marshmallow-1810, pvlib-1165 and
  pydicom-811: those three already exposed payloads in order, then the same three
  again. Only technical instance IDs change to make records unique; the prompt
  excludes IDs, so message bytes and native input token IDs must match each pair.
  Record mapping to original IDs outside inference. Compare raw output, output
  token IDs, ranked paths, dispositions and failure reasons without selecting the
  better answer. Retain every repetition in its technical run. This is same-backend
  greedy repeatability, not another quality sample or a cross-host confirmation.

For each constrained arm only, add two synthetic packets:

- Empty candidate list: the sampling schema admits only `[]`; valid empty JSON
  tests the boundary and cannot establish localization success.
- Two candidates with an embedded quote and a non-ASCII character in their paths.
  Output must parse as an array of at most ten strings from those supplied paths.
  Uniqueness is still graded separately. This exercises escaping through the
  native template/tokenizer/schema-to-grammar conversion.

There are 32 technical requests: four ordinary synthetic, 24 old-task replay,
four constrained boundary requests. They are outside the 80 validation attempts.
No technical gold, labels, evaluator or benchmark patch is transported to inference.
No quality gate on old-task correctness; malformed/duplicate free outputs are
retained. A constrained output violating its schema, missing effective eager grammar,
overflow/truncation, incorrect counters/template/offload or failed isolation blocks
research. A repeatability mismatch is reported as a technical gate failure; do not
retry or silently select a stable subset.

## Resources and archive discipline

Use the identical pinned backend/weights/configs and one attempt per technical
record. Save first/repeated request timings separately; do not claim a clean-cache
cold start or a load/concurrency benchmark. Fresh backend process load times remain
separate from serial requests; the OS/model caches may be warm after verification.

For each run collect NVIDIA telemetry at a fixed one-second interval outside the
isolated inference process: GPU timestamp, index, memory used, utilization and power.
Retain raw CSV, sample count and sampled maximum memory. Sampling can miss peaks;
active GPU-seconds and task-level GPU attribution remain unknown. The monitor itself
has overhead and identical sampling is used in all validation arms. Stop it before
archiving to avoid a changing-file capture.

Fixed validation order remains S-free, S-constrained, G-constrained, G-free.
All technical gates precede the joint execution freeze and first validation output.
Technical work and its failed attempts remain in whole-session spending; exclude
them only in explicitly labeled standalone deployment scenarios.

After each validation arm, build a checksum-verified archive under a unique immutable
milestone filename. Build to a temporary file and rename only when complete. Keep
final and failure archives separately; do not overwrite any collected artifact.
Local collection verifies remote hash and every run checksum before evaluation/deletion.
Retain the same three-hour automatic DELETE backstop and early cleanup. The user's
single-session authorization is at most USD 5; no additional hardware/session is
implied by these tests. Research claim publication remains a separate authorization.
