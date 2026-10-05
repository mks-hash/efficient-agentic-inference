# Frozen split manifests

`dev-v1.json`: 12 tasks, two per repository, selected before evaluation from the
225-row pinned SWE-bench dev source by repo-round-robin-sha256-v1, seed eai-dev-v1.
`evaluation-v1.json`: all 500 Verified IDs reserved for later final evaluation.
`checksums.json`: immutable manifest byte hashes.

No final labels or predictions are stored here. Freeze a new named split for any
population change; do not silently update IDs after seeing quality. Exact-ID and
normalized same-repository issue overlap are audited; near-duplicate and future
training boundaries require additional controls.
