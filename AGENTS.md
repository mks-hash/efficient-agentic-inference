# Agent working agreement

## Scope and sequence

Efficient Agentic Inference studies the economics of agent inference. Small
Specialist is Track 1. Start with a bounded, reproducible localization benchmark;
do not turn this repository into a generic agent framework or a training demo.

Read README.md, RESEARCH_PLAN.md, WORK_TRACKER.md, the relevant decision records,
and docs/benchmark-localization-v1.md before changing research behavior.
The initial planning sources are local-only in ignored `.develop/`.

Work in this order: contract and preregistration, deterministic dataset and labels,
lexical baseline, untuned small/generalist baselines, then a justified training
pilot. Treat model lists, prices, competition rules and deadlines in the planning
sources as unverified until checked against primary sources and recorded.

## Evidence discipline

- Never fabricate measurements or tune the grader to favor an experiment.
- Label synthetic fixtures as synthetic. They establish software behavior only.
- Keep PASS, FAIL, NOT_RUN, UNKNOWN and UNSUPPORTED separate for every evidence
  gate. A load test proves neither useful localization nor efficiency.
- Freeze dataset IDs, split membership, label/retrieval policies, metric thresholds
  and configs before final evaluation. Record changes in an ADR and a new contract
  version; never silently revise a frozen run.
- Preserve all attempted instances, raw outputs, errors, timeouts, malformed and
  truncated outputs. Failures remain in quality and cost denominators.
- Unknown cost, GPU time or tokens are null, never an invented zero. Zero means
  known absence; zero successful tasks makes cost per success undefined.
- Record code identity, model/tokenizer revisions, prompts, configs, hashes,
  hardware, accounting boundaries and artifact checksums.
- Keep gold patches, gold locations and test metadata outside inference evidence.
  Training/dev must exclude frozen evaluation instances and duplicate equivalents.
- Report negative findings, retrieval ceilings, training costs, failed attempts,
  fallback overhead and generalization limitations.

## Engineering and execution

Prefer small typed Python interfaces and standard ML/data libraries. Avoid unused
backend abstractions, runtime/cache dependencies and speculative training modules.
Use independently specified fixtures for meaningful invariants. Run CPU checks
before committing; record which checks ran and which did not.

Never commit credentials, local planning context, datasets, model weights, full
repository copies or large run artifacts. Keep `.develop/` ignored.
Paid GPU/cloud runs require explicit budget and run authorization. Preparing
configs and CPU checks does not authorize paid runs. Do not send external messages
or publish research claims without user authorization.

Update WORK_TRACKER.md when scope, completion, evidence or blockers change.
Changes to the benchmark contract require an accompanying explanation of how
comparability is affected. Do not mark models supported or hypotheses confirmed
based on tests of implementation alone.
