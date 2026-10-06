# Research releases

Publish a release when a bounded research milestone has a frozen contract,
reproducible artifacts, completed relevant checks and an explicit statement of
what the evidence establishes. Negative findings qualify. Routine documentation,
CI and refactoring changes can remain ordinary commits.

While the harness is evolving, use 0.x versions. A minor release records a new
experimental milestone or a meaningful contract change. A patch release records
a correction or maintenance update to a released milestone. Future versions
depend on completed evidence; they do not promise positive specialization results.

Each release must retain:

- an annotated Git tag pointing to the exact release commit and matching package version;
- source dataset revisions, frozen split manifests, contract and schema versions;
- the result bundle, checksums and original experiment code identities;
- configurations, environment and measurement boundaries;
- reproduction evidence and limitations, with links that resolve at the tag.

Release code identity and experiment code identity may differ. Record both and
explain changes; do not attribute historical timings to a new commit. Recheck
predictions and quality if runtime sources change. A package version change also
changes the checksummed `__init__.py`, even when the ranker is unchanged.

Never move a published tag or replace evidence assets in place. Corrections retain
the original result and identify the superseding run in a new release. Releasing
a pilot does not turn its development data into an untouched evaluation set.

The first milestone is [v0.1.0](releases/v0.1.0.md). The completed untuned
small-model comparison has [v0.2.0 milestone notes](releases/v0.2.0.md);
publication of its tag and GitHub Release is a separate step. Training requires a separate evidence-based
decision and any necessary resource authorization.
