# Results storage

The first measured development pilot is
[SWE-bench dev-v1: lexical localization](reports/swebench-dev-v1/README.md):
12 tasks across six repositories, with pinned sources and a local leakage audit.
It is not a final evaluation or a model/specialization claim.

[SWE-bench dev-v2: preparation and lexical controls](reports/swebench-dev-v2-preparation/README.md)
adds 60 new development issues and matched context packets. Full-corpus and
context lexical quality/coverage are reported separately. Those frozen controls
are now compared with
[untuned Qwen3-4B on L4](reports/untuned-dev-v2-l4/README.md): 60 attempts,
including eight invalid answers scored as failures. The
[technical report](../docs/technical-reports/untuned-dev-v2.md) explains the
matched-context finding and its development-only scope. A fresh 4B run in the
[matched 14B comparison](reports/generalist-dev-v2-l4/README.md) reproduced all
60 historical ranked-path/disposition records. Economic benefit remains unmeasured.

[Output reliability validation](reports/reliability-validation-v1-l4/README.md)
compares free/candidate-constrained generation for both models on 20 new issues
in five previously seen repositories. All 80 attempts remain in denominators.
The primary 4B improvement rule fails; the 14B +0.05 gain is exploratory with
an interval including zero. Technical/repeatability/paired-input gates passed;
the validation population is now exposed. No training or economic claim follows.

[Candidate-score validation](reports/score-ranking-validation-v2-l4/README.md)
compares fresh constrained-path and integer-score recipes on 30 new issues in
four seen repositories. All 120 research attempts are retained. Format-valid
scores substantially reduce Recall@5: 4B 0.6528 → 0.3222, 14B 0.6750 → 0.1389.
The primary improvement rule fails; technical/provenance checks pass. This
whole-recipe negative result does not reject other scoring methods. The set is
now exposed; actual full-system cost and generalization remain unknown/untested.

```
results/
  README.md
  runs/<unique-run-id>/      # ignored local immutable runs
    manifest.json             # inference provenance; no gold identity
    predictions.jsonl
    summary.json
    checksums.json
  reports/                  # reviewed compact derivative outputs and reports
    local/                  # ignored drafts
```

Keep run artifacts separate from checked-in synthetic examples. Commit reviewed
small summaries/manifests only when useful, with checksums and reproduction commands;
publish large artifacts separately. Never commit model weights or cloned repositories.
Synthetic runs must say synthetic in both manifest and report. Do not publish
anticipated quality, cost savings or model support as measurements.
