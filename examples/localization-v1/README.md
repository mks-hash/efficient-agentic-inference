# Synthetic localization fixture

Archived v1 fixture. Use [the separated v2 example](../localization-v2/README.md)
with current programs; the old combined baseline CLI has been retired.

Three manually authored cases: one relevant file, multiple relevant files and an
unreachable newly created file. These are not SWE-bench tasks or model evidence.
Gold is stored separately and never passed to rank_files. The new-file case must
stay in the denominator and fail strict success, despite valid output.

Expected quality: Recall@5 mean 2/3, strict Success@5 2/3, monetary cost and CPS null.
Timing varies. The fixture supports deterministic ranking/metric checks only.
