# CUDA execution gate — prepared, not model-validated

The runner supports a separately frozen CUDA request configuration. Software
checks verify device selection, unknown utilization semantics and rejection of
missing/partial offload. No actual GPU resource fit, output or latency gate has
passed yet. Paid execution requires an explicit budget and authorization.

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
