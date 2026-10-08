# Matched 4B / 14B development comparison

Frozen dev-v2: **60 issues / 6 repositories**, identical bounded evidence and
one greedy attempt per model. This compares two fresh runs; the released 4B
result is a historical reference. No training, repair, retries or fallback.

| Treatment | Recall@5 | Strict@5 | Ceiling | Valid / invalid | p50 / p95 request |
| --- | ---: | ---: | ---: | ---: | ---: |
| Fresh Qwen3-4B-Instruct-2507 Q4_K_M | 0.656926 | 33/60 | 0.783487 | 52 / 8 | 3.221s / 4.249s |
| Qwen3-14B Q4_K_M, non-thinking | 0.609120 | 30/60 | 0.783487 | 49 / 11 | 11.545s / 13.376s |

Failures remain in all denominators. Candidate paths/hashes are identical and
all labels known. The primary G minus S recall gain is
**-0.047806**, repository-block 95% interval
**[-0.079036, -0.028107]** (5,000 resamples, seed 20261006, nearest-rank).
The preregistered material-gap rule (gain ≥0.05, G strict noninferior, interval
lower bound >0) is **FAIL**. This candidate/configuration does not justify an
adaptation pilot under ADR 0006. It does not establish model equivalence, SS-H1
or a general small-model advantage. Different post-training and conversion
histories preclude attributing the outcome to parameter count alone.

The fresh small run reproduced all 60 historical ranked-path/disposition/failure
records; see [replication](small-historical-replication.json). Both models
completed all 60 attempts at EOS without context truncation. S had eight
unknown-path invalid answers; G had nine unknown-path and two duplicate-path
answers. Its request median was 3.58× the small median on this single serial batch.

[Supplemental diagnostics](supplemental-diagnostics.json) are **post hoc** and
do not alter the primary criterion. The six tasks valid for S but invalid for G
contribute −0.07778 to the all-task recall difference, offset by +0.02580 on the
46 both-valid tasks and +0.00417 on three S-invalid/G-valid tasks. The five
both-invalid tasks contribute zero. Conditional both-valid performance does not
establish a causal ranking advantage. The bounded top-5 oracle is Recall@5
0.78133 and strict 39/60; it is evaluator-only information, never model input.

## Execution and evidence

Minimal clean code archive `f0a654ca81a8a7a17151ea37e3ec3855377ac728`;
pinned backend and model hashes, native tokenizer/template, full GPU offload and
physical gold/network isolation passed. Both configurations froze after synthetic
and old dev-v1 resource probes, before the first new dev-v2 generation.
Resource probes establish execution behavior only and are excluded from quality.

One g2-standard-4/L4 ran in us-east4-c after capacity errors elsewhere. The host
is shared by both serial arms (S then G); historical-host and cache/order
differences limit replication and latency claims. The new VM and boot disk are
confirmed absent. The wall boundary from provider start to confirmed absence was
51.55 minutes. Runtime raw outputs and all technical attempts
are retained in the ignored checksum-verified archive. Public predictions redact
raw output; fresh evaluation confirms identical per-task metrics. See
[provenance](provenance.json), [gates](evidence-gates.json),
[paired analysis](paired-comparison.json), [cleanup](cleanup-summary.json) and
[phase/scenario record](accounting/session-scenario.json).

## Cost and interpretation

**Actual full-system cost per successful task remains unknown.** Recorded phase
times and list-rate compute/storage/IP components are deployment scenarios, not
invoices. Network, external preparation and other charges remain null, so neither
complete scenario CPS nor actual CPS is reported. The inclusive session's
compute-only list-rate scenario is USD 0.6053; it includes
setup, probes, failures, idle allocation and collection. Independent cold batch
scenarios replay common preparation once per treatment and exclude explicit
research probes; they are not additive parts of the shared session invoice.
They use observed post-probe load/request timings; an independent clean-cache
cold start was not measured. The list-rate review uses the actual us-east4 region:
[compute](https://cloud.google.com/products/compute/pricing/accelerator-optimized),
[disk](https://cloud.google.com/compute/disks-image-pricing) and
[IP](https://cloud.google.com/vpc/network-pricing). Account credits/taxes have not
been joined. See [rate provenance](accounting/rate-review.json).

Only six exposed development repositories are covered. Same-repository
validation-v1 and SWE-bench Verified remain untouched. Different post-training
generations and GGUF conversions prevent attributing the outcome to parameter
count alone. Greedy non-thinking is a controlled treatment, not an optimal
configuration claim. No generalization, issue-repair, specialization or economic
substitution claim follows from this comparison.

## Re-evaluation

Rebuild labels from the pinned snapshot under the [reproduction guide](../../../docs/reproducibility.md)
and [frozen protocol](../../../docs/experiments/generalist-dev-v2.md). The expected
gold SHA-256 is recorded in provenance. With a fresh output directory:

```bash
uv run eai-evaluate \
  --predictions results/reports/generalist-dev-v2-l4/small-replication-dev-v2/predictions \
  --gold /path/to/frozen/dev-v2/gold/labels.jsonl --output /path/to/fresh/small-evaluation
uv run eai-evaluate \
  --predictions results/reports/generalist-dev-v2-l4/generalist-dev-v2/predictions \
  --gold /path/to/frozen/dev-v2/gold/labels.jsonl --output /path/to/fresh/generalist-evaluation
```

The primary paired analysis uses `comparison.paired_comparison` on the two
`metrics.jsonl` outputs and repository membership from `splits/dev-v2.json`.
Accounting can be recalculated with `python -m efficient_agentic_inference.accounting`,
using each arm's ledger and evaluation summary. Unknown components remain null.
These are evaluation commands; no gold is provided to inference.
