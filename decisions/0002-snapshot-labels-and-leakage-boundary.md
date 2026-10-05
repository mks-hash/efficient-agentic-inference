# ADR 0002: Immutable snapshots and physically isolated inference

Date: 2026-10-06. Status: accepted before real baseline evaluation.

## Decision

Replace the combined v1 fixture CLI with two independent programs. `predict`
imports only inference types/ranking/artifact helpers. `evaluate` consumes saved,
checksummed predictions and separate evaluation labels. Gold may be prepared in
advance; inference may not access it. v1 artifacts are archived and not silently
reinterpreted. New artifacts use schema 2.0.0 and localization-v2.

Freeze the original SWE-bench dev source and Verified revisions/checksums. Reserve
all Verified IDs without producing final predictions or labels. Choose 12 dev
instances by SHA-256 of fixed seed + ID within repository, round-robin over sorted
repository names. Exclude exact instance and normalized same-repository issue
duplicates against Verified. Selection reads four allowlisted columns only.
This is a small development pilot, not a representative benchmark claim; exact
overlap checks do not prove absence of near duplicates or model contamination.

Export each exact base commit directly from a private Git object cache with
`git ls-tree` and `git cat-file`, verifying blob identities. Avoid Git archive
attributes that could omit or substitute file contents.
Inference receives no Git history. Record Git commit/tree IDs and sorted path,
size, mode and content hashes. Materialize regular files only; record symlinks
without following them and do not expand submodules. Never execute repository code.

Candidate policy python-full-corpus-v1: all regular `.py` files, including tests,
valid UTF-8 without NUL, at most 1 MiB each, ordered by relative POSIX path. No
gold-informed inclusion, ordering or generated-file removal. Record every skipped
file and reason. BM25 uses path + full source, k1=1.2, b=0.75, unique issue tokens,
path-sorted score ties. This is an existing-file ranking task.

Solution-patch-files-v2 uses `patch`, never `test_patch`. Git parses diff paths;
strict file metadata determines added/deleted/renamed/copied/mode/binary cases.
Modify/delete/rename use the old path; additions/copies use the new path. Preserve
unreachable new files. A test path is a path under test/tests/testing or a basename
starting test_; other .py files are implementation; the rest non-code. This coarse
classification is fixed for the pilot and is not an oracle about generated code.
Unknown/unsupported patches have explicit reasons and unknown metrics.

Report all solution-patch gold first, implementation subset second. Primary recall
uses all gold, including unreachable files. Candidate ceiling uses accessible
gold/all gold; conditional recall uses accessible gold only and is diagnostic.
Zero accessible gold gives undefined conditional recall, not success. Empty gold
does not give strict success. Preparation failures remain in selected-population
counts and primary task success rate; known-gold failed preparation scores zero.
Unknown labels stay unknown and block a complete aggregate quality claim.

## Technical boundary and acceptance

Linux bubblewrap mounts only the stdlib runtime, the four inference source modules,
an inference-input file, and a fresh writable output staging directory. It unshares
network/process namespaces and clears the environment. No project checkout,
upstream dataset, evaluation code/data, Git cache or other result folders are mounted.
Without bubblewrap, ordinary prediction is functional but physical isolation is
UNVERIFIED. Do not substitute a Python socket mock for OS isolation evidence.

Acceptance requires: independent label fixtures; identical deterministic artifacts
on rebuild; no dev/final ID intersection; prediction with evaluator files physically
absent; gold mutation leaves semantic predictions unchanged; forbidden upstream-field
mutation leaves input/candidate set/order and predictions unchanged. Timings and
runtime/platform metadata are excluded from prediction identity. Measure ranking
wall/CPU time and setup separately; do not claim priced economics without rates.
