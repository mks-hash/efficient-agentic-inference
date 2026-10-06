# Cost ledger v1

This post-evaluation namespace is separate from localization-v2 inference,
prediction and gold schemas. It does not change their contract or frozen records.

Every ledger retains exactly six cost components, the complete selected task
count and an explicit allocation policy. Known amounts need evidence references;
known zero also needs evidence. Actual charges and price scenarios are distinct.
Unknown values remain null and prevent a complete total/CPS. Zero successes yield
undefined CPS. Unknown labels prevent a complete success denominator.

`actual_evidence` references measured charges or a documented absence of a charge;
`scenario_basis` references rates, observed durations and allocation assumptions.
Validation checks structure and arithmetic, not the truth of billing evidence.
Single-session pooled costs do not establish separate treatment charges.

See [accounting boundaries](../../../docs/cost-accounting-v1.md) and the CPU-only
CLI `python -m efficient_agentic_inference.accounting`.
