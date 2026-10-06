# Cost accounting v1 — measured charges and explicit scenarios

Status: implementation/contract validated on synthetic CPU fixtures only.
No new cost or efficiency measurement is established by this document.

## Boundary and denominator

`localization-batch-v1` includes acquisition/context preparation, backend/model
setup, load/warmup, every attempted request (including invalid answers), failed
starts/probes, idle allocation, collection and resource teardown. Include compute,
storage, external IP, network, external preparation and other charges. The last
component covers taxes/fees or other applicable costs; do not silently omit it.
Human research labor is outside this machine-cost boundary and must be stated.

CPS is total boundary cost divided by strict file-localization successes at K=5.
Every selected task stays in the cost population. This is not downstream repair
CPS. Unknown labels block the complete success denominator; zero successes make
CPS undefined. CPU wall time cannot be converted to money without a declared rate.

## Record phases before interpreting cost

The host launcher must retain UTC start/end and monotonic elapsed time for
allocation/ready, backend build, each model download/verification, resource probes,
each backend load/request batch, transfer and confirmed VM/disk absence. Each
phase identifies treatment/shared/research-only work, failures and evidence hashes.
Serial phase intervals must not overlap or leave unreported idle time. Existing
backend `phases.json` covers model lifetime only; it is not the whole-session log.

Actual spending is the single session's attributable billable charges, preserving
the resource IDs, currency, usage dates, credits treatment and billing evidence.
A provider invoice/export can arrive later; until then actual charges remain null.
User budget authorization and list-rate planning are not cost observations.

## Two accounting views

**Research session spending:** count each actual allocation once, including both
models, failed starts, probes, collection and cleanup. Do not divide a pooled
invoice into supposedly measured model prices without attribution evidence.

**Independent deployment scenarios:** use observed treatment-specific phases and
declared rates. Replay common acquisition/context/backend preparation once for
each independently deployed treatment, plus that model's own download/load,
requests/failures, idle time, storage/network and teardown. These standalone
scenarios are not additive components of the actual shared experiment invoice.
Keep research probes/technical-debug overhead separate and publish an inclusive
session scenario alongside the deployment view. Unknown charges remain null.

Publish cold one-batch (60 tasks) scenarios first. Warm resident/request-only
scenarios may be supplementary, with explicit exclusions and no assumed
concurrency. Training amortization is NOT_APPLICABLE: no training occurred.
For allocation assumptions that cannot be measured, label the component scenario;
never put it into `actual_usd`. Full-system actual CPS can remain unknown even
when compute-only estimates are available.

## Executable ledger

The [ledger schema](../schemas/accounting/v1/ledger.schema.json) requires each
component once, selected population, currency and allocation policy. Each known
actual or scenario amount needs an evidence/basis reference, including known zero.
Evidence references require human review; schema validation cannot authenticate
an invoice. The calculator never fetches prices or substitutes scenario for actual.

Run after evaluation, from the repository root, with a fresh output directory:

```bash
uv run python -m efficient_agentic_inference.accounting \
  --ledger /path/to/ledger.json --evaluation /path/to/evaluation/summary.json \
  --output results/runs/unique-cost-record
```

The summary retains source hashes, both totals/CPS, unknown components, unsuccessful
tasks and separate cost/denominator states. Original prediction measurements and
evaluation records are not rewritten. The accountant reads evaluation data and
must never be mounted inside the inference sandbox.

See [synthetic ledger](../examples/accounting-v1/ledger.json) and
[synthetic evaluation](../examples/accounting-v1/evaluation.json). Their amounts
are independently specified software fixtures, not model or cloud measurements.
