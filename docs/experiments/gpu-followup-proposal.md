# Accelerator follow-up proposal (not executed)

Local CPU smoke validates native API, parsing and resource accounting. A cloud
run is a separate execution treatment and needs an explicit spend/time limit and
run authorization before provisioning. No provider, current price or GPU result
is implied by this proposal.

## Preserve the experiment

Keep original model revision, Q4_K_M artifact SHA-256, system prompt, canonical
user rendering, context profile, population, greedy seed, 512 output tokens and
one attempt per task. Use the pinned llama.cpp source, recording a new CUDA build,
binary hash, driver/runtime versions, GPU identity and actual VRAM/context fit.

Use synthetic and old dev-v1 packets for GPU format/resource checks. Freeze GPU
execution parameters before dev-v2 generation. Different numerical kernels can
change greedy token choices; do not assume CPU/GPU prediction identity or transfer
CPU quality measurements to GPU. Evaluate every saved GPU result separately.

## Practical resource gate

An inference GPU with 16 GB VRAM is an initial capacity proposal, not a verified
fit. Model file size alone does not cover KV cache or working buffers. Confirm
16,384 context tokens plus 512 output reserve, no silent truncation, full model
offload and peak allocated/device memory. A large CPU-only VM is another option,
but its speed/cost benefit must be measured on that hardware.

## Paid-run boundary

Record hourly GPU/VM/storage rates with source and timestamp, billing granularity,
reservation wall time, setup/download/build, model loading, warmup, each attempted
request, evaluation and teardown. Record actual invoice/billable usage separately
from assumed rate scenarios. CPU request latency cannot be converted into GPU
cost. Include failed attempts and setup under explicit amortization assumptions.

Provision only after agreeing on provider/account, one chosen resource, spending
ceiling and hard runtime limit. Use a job that saves artifacts incrementally and
terminates compute at completion/limit; account for storage remaining afterward.
Keep data, cloned repositories, weights and full logs outside Git. Prepare a
source-free compact report with hashes and raw file-ranking outputs.
