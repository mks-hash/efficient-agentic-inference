# Changelog

## 0.3.0 — 2026-10-08

Matched 4B/14B localization, two separately frozen new-issue validation campaigns
and a source-hashed cross-report synthesis. The tested larger candidate fails its
development improvement rule; output constraints give no primary 4B gain; the
complete score recipe substantially reduces quality despite valid vectors.
All attempted instances remain in reported denominators. Training, broader
generalization, downstream repair and actual full-system CPS remain untested or
unknown. See the [release notes](docs/releases/v0.3.0.md) and
[research synthesis](docs/technical-reports/localization-synthesis-2026-10-08.md).

## 0.2.0 — 2026-10-06

First untuned small-model localization baseline: Qwen3-4B Q4_K_M on L4 achieves
Recall@5 0.6569 and strict file coverage 33/60 versus matched lexical 0.2283 and
8/60. Exposed development data only; actual monetary cost remains unknown.
See the [release notes](docs/releases/v0.2.0.md).

## 0.1.0 — 2026-10-06

First reproducible SWE-bench file-localization milestone: frozen development
snapshot, patch-derived labels, isolated prediction, separate evaluation and a
CPU lexical baseline independently reproduced on a second machine.

The 12-task, six-repository pilot achieved Recall@5 0.541667, Strict Success@5
6/12 and candidate recall ceiling 1.0. Monetary cost remains unknown. No model,
specialization, downstream repair or final Verified evaluation claim is made.

See the [release notes](docs/releases/v0.1.0.md) and
[complete evidence report](results/reports/swebench-dev-v1/README.md).
