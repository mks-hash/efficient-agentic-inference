# Results storage

No research results exist yet.

```
results/
  README.md
  runs/<unique-run-id>/      # ignored local immutable runs
    manifest.json
    predictions.jsonl
    summary.json
    checksums.json
  reports/                  # reviewed compact reports can be tracked
    local/                  # ignored drafts
```

Keep run artifacts separate from checked-in synthetic examples. Commit reviewed
small summaries/manifests only when useful, with checksums and reproduction commands;
publish large artifacts separately. Never commit model weights or cloned repositories.
Synthetic runs must say synthetic in both manifest and report. Do not publish
anticipated quality, cost savings or model support as measurements.
