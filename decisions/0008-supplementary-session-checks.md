# ADR 0008: Fixed technical checks alongside reliability validation

Date: 2026-10-07. Status: accepted before validation generation.

The user authorized the proposed one-L4 USD 5 / three-hour session conditional
on readiness, and asked to make useful additional tests in the same allocation.
Retain the four-arm primary reliability contract and all 80 validation slots.
Do not introduce new models, prompts, sampling recipes or validation populations.

Add a separate versioned [session-checks-v1 contract](../docs/experiments/reliability-session-checks-v1.md):
fixed synthetic boundary cases and repeated payloads from three already exposed
dev-v1 issues. They test implementation/native determinism and observed serial
request resources. They do not contribute to validation quality denominators,
select a winning model, or justify tuning after validation exposure.

Archive each completed validation arm under an immutable milestone filename to
avoid races between a subsequent snapshot and a local transfer. Sample GPU memory,
utilization and power once per second using a separate controller process, stopped
before archive creation. Call memory maxima sampled observations, not exact peaks;
do not convert utilization percentages into measured active GPU time.

Record all extra probes and telemetry overhead as research-only session work.
Keep the same allocation/budget/deletion boundary; no second paid allocation.
Collect evidence on gate failure and delete the newly created VM/disk. The initial
preparation NOT_AUTHORIZED statements retain their historical meaning; this ADR
records subsequent user authorization. Publication is not authorized by this run.
