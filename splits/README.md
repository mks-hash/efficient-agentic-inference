# Frozen split manifests

`dev-v1.json`: 12 tasks, two per repository, selected before evaluation from the
225-row pinned SWE-bench dev source by repo-round-robin-sha256-v1, seed eai-dev-v1.
`evaluation-v1.json`: all 500 Verified IDs reserved for later final evaluation.
`checksums.json`: immutable manifest byte hashes.

`dev-v2.json`: 60 new development tasks, seed eai-dev-v2, with dev-v1 IDs and
equivalent normalized issues excluded before selection. Its byte hash is in
`dev-v2.sha256`; original v1 manifests/checksums remain unchanged. Allocation follows
repository capacity: marshmallow 7, pvlib 11, pydicom 11, astroid 11, pyvista 10,
sqlfluff 10. This is new-issue development within the same six repositories.

`validation-v1.json`: 20 issues in five seen repositories, seed eai-validation-v1,
excluding both dev populations and Verified IDs/normalized equivalents. This
population was exposed by the completed reliability campaign and cannot validate
recipes developed from its failures. Its checksum remains frozen in its campaign.

`validation-v2.json`: 30 fresh issues, seed eai-validation-v2, excluding dev-v1,
dev-v2, validation-v1 and Verified IDs/normalized equivalents. Byte identity is in
`validation-v2.sha256`. Allocation: pvlib 8, pydicom 8, astroid 7, sqlfluff 7.
Only four seen repositories remain eligible; no repository/time hold-out claim.
Membership was frozen before reconstruction or inference. This reserved population
belongs to the [score-ranking protocol](../docs/experiments/score-ranking-validation-v2.md).

No final labels or predictions are stored here. Freeze a new named split for any
population change; do not silently update IDs after seeing quality. Exact-ID and
normalized same-repository issue overlap are audited; near-duplicate and future
training boundaries require additional controls.
