# ADR 0006: Matched larger-model comparison and explicit cost boundaries

Date: 2026-10-06. Status: accepted for preparation; paid execution NOT_AUTHORIZED.

## Decision

Prepare one Qwen3-14B Q4_K_M non-thinking candidate and a fresh Qwen3-4B-Instruct-2507
replication on the same pinned llama.cpp/L4 stack. Freeze their execution identities
after synthetic/old dev-v1 resource gates, before any new dev-v2 generation. Use
the unchanged 60-task packet, prompt, 16,384-token capacity, 512-token output budget,
greedy decoding and one attempt. No repair, constrained decoding, retries or training.

The dense 14B candidate has a published 9,001,753,984-byte artifact and an estimated
2.5 GiB FP16 KV cache at the declared capacity. This makes one L4 a plausible
bounded starting host; fit is NOT_RUN. A larger parameter count does not establish
better localization. If this candidate has no useful advantage, report it rather
than selecting another model based on dev-v2 outcomes. Different post-training
generations and GGUF conversions limit attribution to parameter count.

The pinned hybrid model requires explicit `enable_thinking=false`, native suffix
verification and server reasoning disabled. Generated output is never stripped
or repaired. The small model retains its historical default template request.
This introduces an opt-in execution contract, not a changed localization grader.
Source/binary/template identities and old-model probe parity must be recorded.

Separate actual session spending from standalone deployment scenarios. One shared
VM invoice does not directly measure two independent treatment prices. Keep
unknown external CPU preparation and unattributable charges unknown. Version the
post-evaluation cost ledger independently; inference/prediction/gold v2 schemas
and all v0.2.0 result bytes remain unchanged.

Reserve 20 new `validation-v1` issues deterministically before future prompt/output
interventions. Exclude dev-v1/dev-v2 IDs and normalized equivalents plus Verified
using the existing freezer. Only membership is created; no labels, repository
exports or predictions are generated. It is same-repository validation, not
repository-disjoint or temporal evaluation. Current dev-v2 remains exposed.

## Comparison and decision

The primary paired comparison is the generalist candidate minus the fresh small
replication under identical semantic evidence. A material development gap uses
the existing 0.05 recall margin, strict noninferiority and positive repository-block
95% interval lower bound, with 5,000 resamples/seed 20261006. Reuse the implemented
paired analysis; do not apply its original lexical decision to a full-corpus arm.
An inconclusive gap does not prove equivalence or generalist replacement.

A positive gap supports designing an adaptation pilot, conditional on accounting,
validation and separate budget gates. No gap supports stopping training work for
this candidate until new evidence exists. Cost scenarios alone do not establish
measured economic savings. No change to the frozen population, gold or thresholds
is authorized by a resource failure.
