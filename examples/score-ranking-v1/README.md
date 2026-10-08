# Synthetic score-format probes

These fabricated issues/repositories establish software behavior only. They are
not SWE-bench samples and have no research gold labels or quality metrics.

`tasks.jsonl` contains exactly the two, empty and twenty candidate packets used
in preparation. Candidates are path-sorted and candidate checksums are verified.
`historical-tasks.jsonl` preserves the previous unsorted two-candidate path probe
for request/token compatibility; the score recipe deliberately rejects unsorted
bindings. Do not reorder it and then claim historical identity.

Use `--synthetic` when configuring either probe. Instructions are in
[reproducibility](../../docs/reproducibility.md). Retain all outputs, even if
their semantic ranking looks wrong; valid format does not establish task quality.
