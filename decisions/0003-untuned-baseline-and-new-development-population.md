# ADR 0003: Untuned comparison on new development instances

Date: 2026-10-06. Status: accepted for dataset and context preparation.
Model execution configuration remains a separate gate.

## Decision

Retain the released dev-v1 pilot as regression/debug data. Freeze dev-v2 with 60
new instances from the same pinned SWE-bench dev source, seed `eai-dev-v2`, using
the existing repository round-robin SHA-256 policy. Exclude dev-v1 IDs and
normalized same-repository issue fingerprints, as well as reserved Verified
overlaps, before selection. Store the hash of the excluded development manifest.
No patch, label, difficulty, model output or preparation success affects selection.
Repository capacity may make allocation uneven. Sixty tasks is a bounded experiment
size, not a statistical power or representativeness guarantee.

This tests new issues in already represented repositories. Repository-disjoint
generalization and pretraining contamination remain separate questions. Once used
for research feedback, dev-v2 must be recorded as exposed development data.

Compare the unchanged full-corpus lexical method with two treatments sharing one
gold-blind context packet: lexical ranking on that packet and an untuned model
ranking the same paths and excerpts. Select up to 20 paths by full-corpus lexical
ranking; display them sorted by path, without retrieval scores/ranks. Include the
first 1,200 Unicode characters of each base-file source, plus the full issue.
Record original candidate count, selected paths and excerpt checksums. This fixed
prefix representation is a deliberately simple starting profile, not complete
repository understanding. Context selection is timed and shared between arms.

File-level context ceiling and conditional recall must be evaluated separately
from the full-corpus ceiling. Presence of a path does not prove that its excerpt
contains all useful evidence. Context overflows are retained failures; neither
tokenizer nor server may silently truncate the packet. Models use their native
chat template, with exact rendered text and token IDs retained locally.

Freeze model/tokenizer/quantization/backend revisions, context limit, prompt,
decoding, output budget and resource identity before scoring dev-v2. Use dev-v1
and synthetic fixtures for format/resource checks. One model, one frozen prompt,
one attempt per task; no training, fallback, output repair or retries in this
campaign. Failures remain in denominators. A generalist reference and later
training decisions require their own execution configuration.

## Accounting and completion

Distinguish acquisition/export, context preparation, model load/warmup and request
execution. Preserve actual tokens, wall time and known resource measurements.
Unknown GPU utilization or monetary rates remain unknown. The milestone measures
file localization; cost per successful localization is not downstream repair CPS.
No paid execution is authorized by this decision.

Completion requires frozen membership and execution config, context identity and
leakage checks, preserved raw model outputs/failures, paired lexical/model quality,
coverage and resource tables, with limitations and reproducible provenance.
Positive gains are not required for completion.
