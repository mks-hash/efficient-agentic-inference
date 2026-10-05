# Data boundaries

Upstream Parquet and private Git object caches belong in ignored `data/local/`.
Never copy upstream evaluation fields into inference inputs. The raw-record
projection is an explicit allowlist: instance_id, repo, base_commit, problem_statement.
New upstream fields remain excluded by default. `hints_text` is not allowed.

The snapshot coordinator freezes the inference projection/tree/candidates before
calling the independent labeler. Gold may exist before prediction but remains in a
separate namespace. The isolated prediction process cannot access the upstream
datasets, labels, evaluator code, Git history or any other runs.

Candidate construction is gold-blind: base Git blobs only, versioned file policy,
path-sorted order and full candidate checksum. All skipped entries are manifested.
Exports retain content hashes and Git identities; no repository scripts are run.
Symlinks and submodules are recorded as inaccessible and never followed.

Reserved final evaluation is represented by pinned source identity and all Verified
IDs. Selection/overlap checks read ID/repo/base/issue columns only, never final gold,
difficulty or test metadata. Exact normalized issue overlap does not establish
absence of near duplicates. Training/validation and temporal controls must be
frozen separately before supervised adaptation.

All selected tasks remain in snapshot population records, including failed checkout,
candidate parse failures, unsupported/empty solution patches and declared overlap
exclusions. No replacement task is selected based on preparation or quality.
Incomplete snapshots without a final snapshot.json are not complete evidence.

Publish only compact derivative run outputs, checked source/split manifests and
reproduction recipes. Keep source datasets, exported repositories, model weights
and local planning material out of Git. Gold patch labels are a reference solution's
locations, not proof that every valid alternative repair must modify those files.
