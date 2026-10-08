# Matched generalist and cost accounting — preparation contract

Prepared: 2026-10-06. The preparation contract below froze at `f0a654c`; its
NOT_RUN/NOT_AUTHORIZED statements describe that preparation state. The user later
authorized execution, completed 2026-10-06 UTC. See the
[matched report](../../results/reports/generalist-dev-v2-l4/README.md): technical
gates PASS, positive generalist-gap rule FAIL, actual/full CPS UNKNOWN.
Preparation rules, model selection and numerical thresholds below are unchanged.
[ADR 0006](../../decisions/0006-matched-generalist-and-cost-accounting.md).

## Question and treatments

Does a larger generalist candidate add a material localization gain over the
untuned small model on identical bounded evidence, and what measured resource
differences and defensible cost scenarios accompany that gain?

| Arm | Fixed model | Native mode | Role |
| --- | --- | --- | --- |
| S | Existing Qwen3-4B-Instruct-2507 Q4_K_M | Historical default request | Fresh replication, primary small comparator |
| G | Qwen3-14B Q4_K_M | Explicit non-thinking | Larger candidate, advantage NOT_RUN |

Historical lexical controls and the released 4B result remain references.
Do not substitute the historical small run for a failed fresh replication, pool
attempts, average away failures or choose the best small result. Every new attempt
remains in its own run. The primary comparison uses the two fresh runs only.

Keep the [60 IDs](../../splits/dev-v2.json), base commits, gold policy and exact
`bm25-top20-prefix1200-v1` packet. Input SHA-256:
`880c534924526231362229bb84dd606e3ef35ab9f75f579152f65d7c9b3eb287`.
Use the unchanged localization prompt, path-sorted excerpts, one slot, four CPU
threads, full GPU offload, FP16 KV defaults, 16,384 context and 512 output tokens.
Greedy temperature 0/seed 0 is a controlled treatment, not a claim of optimal
model settings. The publisher recommends different sampling for non-thinking.

Both runs retain malformed/unknown paths, truncation, timeouts and unattempted
budget-exhausted instances as failures. No reasoning removal, JSON extraction,
grammar, repair, retries, fallback, LoRA or prompt adaptation is allowed.

## Source review and resource proposal

Exact metadata is in [generalist config](../../configs/generalist-dev-v2.json)
and [source review](../../configs/generalist-source-review-v1.json). Official model
revision: `40c069824f4251a91eefaf281ebe4c544efd3e18`, Apache-2.0. Unsloth GGUF
revision: `a04a82c4739b3ef5fa6da7d10261db2c67dd1985`; expected weight SHA-256:
`5eaa0870bd81ed3b58a630a271234cfa604e43ffb3a19cd68e54a80dd9d52a66`.
Metadata is verified; weight bytes have not been downloaded or checked.
The quantizer's exact upstream conversion revision is unknown; do not assert
that the selected official reference revision is its conversion input.

The official configuration has 40 layers, 8 KV heads and head dimension 128.
`2 × 40 × 8 × 128 × 16384 × 2 bytes` gives 2.5 GiB FP16 KV payload, excluding
weights, workspaces, padding and runtime overhead. This is a planning calculation,
not measured GPU memory. One g2-standard-4/L4 is proposed; real fit is NOT_RUN.

Sources checked 2026-10-06:

- [Pinned official model card](https://huggingface.co/Qwen/Qwen3-14B/blob/40c069824f4251a91eefaf281ebe4c544efd3e18/README.md)
- [Pinned official configuration](https://huggingface.co/Qwen/Qwen3-14B/blob/40c069824f4251a91eefaf281ebe4c544efd3e18/config.json)
- [Pinned quantized artifact](https://huggingface.co/unsloth/Qwen3-14B-GGUF/blob/a04a82c4739b3ef5fa6da7d10261db2c67dd1985/Qwen3-14B-Q4_K_M.gguf)
- [Pinned llama.cpp API](https://github.com/ggml-org/llama.cpp/blob/7049ff0cbeb1f5ead231de4522af6b75d8d773c0/tools/server/README.md)

## Resource gates and execution freeze

Before any new research generation: verify downloaded weights, clean code archive,
backend revision/build/binary, native template and isolated filesystem/network.
For each model run the same synthetic packet, then the already declared old tasks
marshmallow-1810, pvlib-1165, pydicom-811. Confirm native tokens/counters, completion
settings, no truncation and full nonzero X/X layer offload. Model invalid paths
are preserved quality failures, not an excuse to tune the prompt. Runtime failure,
partial offload, wrong suffix or context overflow blocks research execution.

The generalist `/apply-template` request includes `enable_thinking=false`; the
rendered native prompt must end with its pinned closed-think generation suffix.
The server also uses `--reasoning off`. Do not modify or replace the native template.
Generalist native GPU behavior remains NOT_RUN until checked with actual weights.

Freeze both complete configs before the first new dev-v2 generation, recording
the code/source/archive/binary/template/input/hardware hashes. Fixed research order:
S then G. Destroy the first backend before loading the second; simultaneous
residency is unsupported. Retain order/cache limitations; this is one serial batch
comparison, not a concurrency or repetition study. Request timeout 120 seconds,
startup timeout 180 seconds, campaign budget 3,600 seconds per arm. Common session
duration cannot exceed its separately authorized cap; collection/cleanup reserve
takes priority over starting a new arm.

The existing freezer now accepts an explicit base config:

```bash
python3 tools/configure-cpu-run.py --base-config configs/generalist-dev-v2.json \
  --binary .develop/backends/llama.cpp/build-gpu/bin/llama-server \
  --build-dir .develop/backends/llama.cpp/build-gpu --device cuda \
  --inputs /path/to/frozen/dev-v2.jsonl --campaign generalist-dev-v2 \
  --run-budget-s 3600 --task-timeout-s 120 --output /path/to/fresh/generalist-config.json
```

These are freeze instructions, not provisioning authorization. Use transported
code identity on the remote host and the existing isolated wrapper. Upload no gold,
evaluator, upstream benchmark, repository exports or Git history; evaluate locally
after collecting immutable predictions.

## Analysis and stop/go

Report macro Recall@5, Strict Success@5, candidate ceiling, valid/invalid counts,
native tokens, p50/p95 request wall, load and complete phase times for both arms.
All 60 selected tasks remain in denominators. Unknown labels block primary claims.
Require exact paired IDs, gold counts and candidate identities before analysis.

Primary gap: G minus S, paired repository-block bootstrap, 5,000 resamples, seed
20261006, nearest-rank 95% interval. A material development gap requires gain
at least 0.05, G strict success not lower than S, and interval lower bound above
zero. This rule is frozen before G outputs; S historical performance was already
known at preregistration. Only six exposed repositories are represented.

A passing gap motivates adaptation design, not training authorization. A failure
or inconclusive gap does not prove equivalence; do not call a weak candidate a
validated stronger generalist. Report the point small/generalist quality retention
ratio descriptively, undefined if G quality is zero. It does not confirm SS-H1.

Keep actual cost and price-scenario CPS separate under
[cost accounting v1](../cost-accounting-v1.md). A complete numeric scenario requires
all declared components and allocation assumptions. Actual unknown charges keep
actual CPS null. Report session spending even when the campaign is incomplete.
No economic winner follows from request time alone.

## Validation reservation

[validation-v1](../../splits/validation-v1.json) reserves 20 new issues excluding
dev-v1/dev-v2 IDs, normalized equivalents and Verified. Its membership was fixed
without patches or difficulty; labels and predictions are NOT_RUN. It is for
future versioned interventions, not this comparison. It remains same-repository
validation and cannot support repository/time generalization claims. Verified
remains reserved and untouched.
