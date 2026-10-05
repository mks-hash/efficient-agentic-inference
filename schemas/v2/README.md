# Artifact schemas v2

`inference.schema.json`, `prediction.schema.json` and `evaluation.schema.json`
define separate namespaces, all with schema_version `2.0.0`.

The inference program's strict data types reject unexpected input fields and
verify the ordered candidate checksum. The evaluator has its own label type and
checks saved prediction identity. Contract tests and the real snapshot audit also
validate records against these independently published JSON Schemas.

v1 combined fixture records and model experiment design remain archived in
schemas/v1. The combined CLI has been retired. v2 prediction manifests describe
the implemented lexical program; model/fallback campaigns need additional pinned
model/prompt/config metadata before they can claim model evidence.

See [contract v2](../../docs/benchmark-localization-v2.md) for semantic rules;
structural validation alone does not prove leakage independence or useful quality.
