# ADR 0010: Fixed technical checks for the score-ranking session

Date: 2026-10-07. Status: accepted for preparation; paid execution NOT_AUTHORIZED.

Supplement the frozen score-ranking-validation-v2 campaign with a separately
versioned [session contract](../docs/experiments/score-ranking-session-checks-v1.md).
The research population, four recipes, primary rule, evaluator and 120 slots stay
unchanged. This supplements execution after dataset reconstruction, before any
validation generation; it does not use validation quality or labels.

For each arm fix five synthetic requests (two, empty, twenty, escaped candidates,
then the same two-candidate payload again) and one exposed dev-v1 trace check.
Twenty-four technical requests test schema/binding/template/counters/EOS, full
offload/isolation and same-backend greedy repeatability. The synthetic requests
remain separate from the real old issue; neither contributes quality samples.
Semantic correctness does not select a prompt or justify proceeding with training.

Preserve the original 29-file research preparation freeze and older reports.
Freeze this supplement, exact input hashes, immutable inference archive and
launcher before paid execution. Use the unchanged native models/backend and
opposite within-model order. Passive one-second telemetry and technical work
stay in total session accounting. No active GPU-time or actual-cost claim follows.

A new one-L4 proposal specifies USD 5 / three-hour automatic DELETE ceiling,
early collection/deletion and existing-resource exclusion. Prior completed-session
authorization does not cover this new allocation. Preparation does not authorize
new VM creation, validation inference, training, publication or release.
