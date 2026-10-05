# Results storage

The first measured development pilot is
[SWE-bench dev-v1: lexical localization](reports/swebench-dev-v1/README.md):
12 tasks across six repositories, with pinned sources and a local leakage audit.
It is not a final evaluation or a model/specialization claim.

[SWE-bench dev-v2: preparation and lexical controls](reports/swebench-dev-v2-preparation/README.md)
adds 60 new development issues and matched context packets. Full-corpus and
context lexical quality/coverage are reported separately. Untuned model execution
remains NOT_RUN; this is preparation for the next model comparison.

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
