# CUDA execution and evidence gate

The runner supports a separately frozen CUDA request configuration. Software
checks verify device selection, unknown utilization semantics and rejection of
missing/partial offload. The pinned L4 treatment passed actual resource-fit,
native API and physical-isolation checks; its frozen 60-task development result
is [reported separately](../../results/reports/untuned-dev-v2-l4/README.md).
This validates that exact execution treatment. Paid execution requires an explicit
budget and authorization.

Use the same pinned Qwen3-4B-Instruct-2507 Q4_K_M artifact, prompt/context and
llama.cpp source. Build on the chosen GPU host with the CPU build flags from the
runbook, except `-DGGML_CUDA=ON -DCMAKE_CUDA_ARCHITECTURES=native`. Record exact
CUDA compiler/runtime, driver, GPU, CMake cache, compiler flags and binary checksum.
Use a clean backend source and the actual build directory when freezing config.

`tools/configure-cpu-run.py --device cuda` freezes CUDA execution without reading
labels. The historical filename is retained for the existing CPU commands. A
transported code archive can provide `--code-identity-json` with its original
commit/tree/archive hashes; never invent a Git revision on the remote machine.
The inference manifest also hashes each of its four actually mounted modules.

`tools/llama-isolated.sh` exposes only GPU 0, its driver/UVM device nodes, system
runtime, read-only hardware sysfs, inputs/config/prompt/model/binary and fresh
output. Gold, evaluator, Git and host network remain absent. Load the UVM kernel
module on the dedicated host before the sandbox; missing device nodes abort the
run. The client and backend share the private network namespace for loopback.

The CUDA request asks for all layers offloaded. Startup must confirm a nonzero
complete `offloaded X/X layers to GPU` message; partial/CPU fallback aborts before
research generation. The pinned backend maps library INFO to trace verbosity;
`--log-verbosity 4` is required to retain this evidence. A missing log remains a
failed gate, never implicit proof of GPU execution. Native template/token provenance, no truncation/repair,
512 output tokens, strict JSON, one attempt and failed-task accounting are shared
with the CPU treatment. GPU utilization seconds remain null; record reservation
wall time/billing separately rather than equating it with active GPU compute.

First run synthetic input and a preregistered old dev-v1 resource subset. Then
freeze the actual GPU campaign config before dev-v2 outputs. Keep all 60 tasks,
raw streams and failures. Different kernels can change greedy outputs; evaluate
GPU quality independently. A timeout or incomplete artifact export must not be
reported as a completed baseline.

## Reproduce the measured treatment

Use an immutable run-specific checkout/archive with Python 3.11+, CUDA 12.9,
CMake 4.1.2 and Bubblewrap. The observed dedicated host was Ubuntu 24.04,
`g2-standard-4` / L4 23,034 MiB / driver 580.178.04. Keep the same pinned
model/source URLs and verify artifact bytes/SHA-256. This procedure does not
provision cloud resources.

Place the execution workspace under a traversable path such as `/opt/eai-run`
on a dedicated VM. Running Bubblewrap through sudo from a protected home can
fail its source binds after user-namespace capability changes. Keep the host-side
workspace separate from model mounts; never expose the full project to fix access.

Build with the CPU runbook's flags plus `-DGGML_CUDA=ON`,
`-DCMAKE_CUDA_ARCHITECTURES=native`, and the exact recorded CUDA compiler.
On the dedicated host, load `nvidia_uvm` before running the wrapper. After
synthetic and declared old-resource gates, freeze the config without labels:

```bash
python3 tools/configure-cpu-run.py \
  --binary .develop/backends/llama.cpp/build-gpu/bin/llama-server \
  --build-dir .develop/backends/llama.cpp/build-gpu --device cuda \
  --inputs results/runs/dev-v2-context-copy/tasks.jsonl \
  --campaign gpu-dev-v2-untuned-copy --run-budget-s 3600 --task-timeout-s 120 \
  --output .develop/gpu-dev-v2-untuned-copy-config.json
sudo tools/llama-isolated.sh results/runs/dev-v2-context-copy/tasks.jsonl \
  .develop/gpu-dev-v2-untuned-copy-config.json \
  models/Qwen3-4B-Instruct-2507-Q4_K_M.gguf \
  .develop/backends/llama.cpp/build-gpu/bin/llama-server \
  configs/prompts/localization-v1.txt results/runs/gpu-dev-v2-untuned-copy
```

For a transported minimal archive, use `--code-identity-json` with its real clean
revision and archive checksum instead of fabricating Git metadata. Acquire/rebuild
context inputs before stripping the evaluator/gold/full checkout from the model VM.
The measured input checksum is retained in the report. Evaluate saved predictions
on a separate host/environment with the frozen gold, after collection and checksum
verification. Native rendering/tokenization should match; binary checksums and GPU
outputs need not match across changed compilers/hardware. Report changed execution
parameters as a separate treatment. All failures remain in evaluation.
