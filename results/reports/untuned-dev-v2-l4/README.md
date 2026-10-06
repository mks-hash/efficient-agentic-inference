# Untuned Qwen3-4B — SWE-bench dev-v2 localization

Date: 2026-10-06. **60 tasks / 6 repositories; one attempt per task.**
Qwen3-4B-Instruct-2507, Q4_K_M, pinned llama.cpp CUDA backend on NVIDIA L4.
No training, output repair, retries or fallback.

## Result

| Treatment | Recall@5 | Strict Success@5 | Candidate ceiling |
| --- | ---: | ---: | ---: |
| Lexical, full corpus | 0.552265 | 25/60 | 0.985450 |
| Lexical, matched context | 0.228326 | 8/60 | 0.783487 |
| Untuned Qwen3-4B Q4_K_M, matched context | **0.656926** | **33/60** | 0.783487 |

All 60 attempts completed: **52 valid / 8 invalid**. Every invalid output contains
an unknown candidate path and receives zero recall/MRR and failed strict success;
no failed instance was dropped. There are no timeouts, input overflows,
truncated inputs, output-budget exhaustion or unknown labels. All-file and
implementation-only metrics are retained in the [evaluation](evaluation/summary.json).
Strict success is reference file-set coverage, not successful issue repair.

The preregistered development rule **passes** against the matched evidence control:
Recall@5 gain **0.428600**, strict 33 versus 8, paired repository-block bootstrap
95% interval **[0.315904, 0.559686]** (5,000 resamples; seed 20261006; nearest-rank).
This establishes a useful development signal for this untuned model under the
frozen packet contract. It does not establish specialization or agent economics.

Against full-corpus lexical, the observed gain is **0.104661**. A supplementary,
post-run interval using the same block-bootstrap method is **[-0.001196, 0.216399]**,
which includes zero. Treat the full-reference advantage as uncertain. The full
reference also has a different candidate set and source representation.

The population is exposed development data from six known repositories. Verified
remains reserved; no repository/time held-out or pretraining contamination audit
has been performed. Dataset/prompt membership and thresholds stay frozen after
this run. Further prompt/retrieval work requires a separate versioned treatment
and declared validation population.

## Input and execution

The exact `bm25-top20-prefix1200-v1` packet is shared with matched lexical: at most
20 BM25-selected paths, first 1,200 Unicode characters/file, path-sorted, full issue,
no retrieval scores. Input SHA-256:
`880c534924526231362229bb84dd606e3ef35ab9f75f579152f65d7c9b3eb287`.
Every candidate list/content hash matches the saved lexical control.

Inference code: clean `f67e4993aa93c5c05e13e28b0bb4b0bf0ea8dc53`; backend:
`7049ff0cbeb1f5ead231de4522af6b75d8d773c0`. Model and quantized revisions,
artifact/binary checksums, native template identity, compiler/build flags and
actual hardware are in the [manifest](predictions/manifest.json) and
[provenance](provenance.json). Context 16,384; output reserve 512; temperature 0;
seed 0; one slot; four CPU threads; request deadline 120 seconds.

Actual Bubblewrap probes verify hidden project/evaluator, a separate network
namespace, zero external IPv4 routes and failed external connection. Gold,
upstream benchmark/evaluator, full source repositories and Git are not mounted.
Only minimal inference modules, permitted packet/config/prompt/model/binary and
fresh output are visible. Inference received no benchmark gold, even outside the
sandbox on the dedicated VM. Evaluation ran locally after predictions completed.
Startup confirms **37/37 model layers offloaded to GPU**; CPU fallback is rejected.

A synthetic GPU API probe matched two prior CPU probes exactly in rendered input,
input/output token IDs and raw output (192 input / 7 output tokens). Three old
dev-v1 resource tasks then completed in 2.78–3.30 seconds each. These probes are
software/resource evidence only. The new 60-task config was frozen afterward.
All 60 native final responses have matching token counters, EOS completion,
no truncation, the greedy sampler and no grammar/adapters.

## Measurements and cost boundary

- Request wall p50 **3.205 s**, p95 **4.215 s**; all 60 attempts included.
- Sum of request wall time **196.445 s**; model load/warmup **2.009 s**;
  complete backend lifetime **199.127 s**.
- Observed native input tokens **477,333**; generated tokens **2,190**, including
  invalid answers and native EOS accounting.
- Whole-backend CPU **198.737 CPU-seconds**; peak child RSS **2,759,260 KiB**.
  Per-task server CPU and active GPU-seconds are unknown.

Request latency covers native rendering/tokenization, prefill, decoding and
validation. It excludes acquisition/context construction, model/binary verification,
load/warmup, evaluation and artifact transfer. Lexical timings cover ranking and
validation on a different CPU; these are not matched total-deployment latencies
or a concurrency/serving benchmark. CUDA device buffers are not peak GPU utilization.

The single authorized cloud session stayed within its three-hour allocation cap:
start to confirmed VM/disk absence **46.19 minutes**, including build, downloads,
failed starts, probes, inference and collection. The on-demand compute-only
list-rate scenario is **USD 0.5441**, using USD 0.706832276/hour; disk, IP, network,
tax and account-specific adjustments are excluded. This is a wall-time accounting
bound and price scenario, not an invoice. **Total measured system monetary cost
and cost per successful localization remain null.** See [cloud-session.json](cloud-session.json)
and [pricing sources](../../../docs/experiments/cloud-options-2026-10-06.md).
The new VM and its auto-delete disk are confirmed absent.

## Retained failures and evidence

Two GPU technical starts failed before generation: protected home traversal and
suppressed full-offload logging. The workspace moved to `/opt`; explicit trace
logging was committed before any GPU generation. Both failures/logs are retained.
Model inputs, decoding and benchmark grading were unchanged. Five of eight
invalid model outputs are from sqlfluff; see [per-repository results](per-repository.json).
No failure was repaired or rerun.

The prior CPU dev-v1 smoke was incomplete at its one-hour limit: 9/12 started,
7 valid, 1 invalid, 1 timeout, 3 unattempted; all 12 remain in evaluation. Its
Recall@5 0.375 and strict 4/12 concern exposed resource-check data, not this
new baseline. Completed-response p50 410.780 s projected roughly 6.85 hours for
60 CPU requests; CPU dev-v2 is **NOT_RUN**. An active shell launcher edit caused
post-inference collection to fail; internal hashes/frozen ce08620 modules verified,
and the outer manifest was recovered once without altering or repeating inference.
See [CPU records](cpu-smoke/resource-summary.json) and
[collection failure](cpu-smoke/post-run-collection.json).

- [Protocol](../../../docs/experiments/untuned-dev-v2.md), [ADR 0005](../../../decisions/0005-bounded-l4-untuned-baseline.md)
- [CUDA reproduction](../../../docs/experiments/cuda-execution.md), [population](../../../splits/dev-v2.json)
- [Predictions](predictions/predictions.jsonl), [quality metrics](evaluation/metrics.jsonl)
- [Primary paired comparison](paired-comparison.json), [full-reference analysis](full-reference-comparison.json)
- [Native evidence hashes/counters](native-evidence.jsonl), [all-attempt audit](native-all-attempts-audit.json)
- [Resource summary](resource-summary.json), [phases](phases.json), [evidence gates](evidence-gates.json)
- [Technical failures](technical-failures.json), [checksums](SHA256SUMS)

This compact bundle contains path-only predictions, metrics, configs, hashes and
measurement evidence. Issue/source-bearing rendered prompts, exact token arrays,
SSE traces and complete failed/setup logs remain in the ignored local archive;
its SHA-256 is retained in provenance. Reconstruct permitted inputs from the pinned
snapshot/context protocol. Saved configs retain their historical freeze-time
NOT_RUN states; current evidence statuses are recorded separately.

The next comparison is a stronger generalist on the same evidence and explicit
system cost accounting. This positive untuned finding alone does not justify LoRA.
