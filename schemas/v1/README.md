# Experiment schemas v1

`experiment.schema.json` defines run provenance and independent evidence states.
`result.schema.json` defines per-task predictions, measurements and failure states.
Schema version is `1.0.0`; benchmark contract is independently `localization-v1`.

All required fields must be present. Unknown/inapplicable measurements use null
with reasons. Known zero is allowed only when actually measured or structurally
absent. Schema validation checks structure; evidence gates still require audited
semantics. An example manifest does not establish that an experiment happened.

Breaking semantics require a new version, migration notes and explicit comparability
limits. Additive fields must not silently change existing metric definitions.
