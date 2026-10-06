# Local CPU execution

This is an unpriced capability/evaluation treatment. See ADR 0004 and the frozen
[dev-v2 protocol](untuned-dev-v2.md). Linux with Bubblewrap, a C++ compiler,
CMake and Python 3.11+ is required. Source-bearing run logs stay ignored.

## Acquire and build

Download the exact artifact URL in `configs/untuned-dev-v2.json` into `models/`.
Require the listed byte length and SHA-256; never substitute a moving model ref.
Keep failed/partial downloads outside final artifact filenames. Backend source
and build outputs belong in ignored `.develop/backends/`.

```bash
git clone https://github.com/ggml-org/llama.cpp .develop/backends/llama.cpp
git -C .develop/backends/llama.cpp checkout --detach 7049ff0cbeb1f5ead231de4522af6b75d8d773c0
cmake -S .develop/backends/llama.cpp -B .develop/backends/llama.cpp/build-cpu \
  -DCMAKE_BUILD_TYPE=Release -DBUILD_SHARED_LIBS=OFF -DGGML_CUDA=OFF \
  -DGGML_NATIVE=ON -DGGML_BLAS=OFF -DLLAMA_OPENSSL=OFF \
  -DLLAMA_BUILD_TESTS=OFF -DLLAMA_BUILD_SERVER=ON
cmake --build .develop/backends/llama.cpp/build-cpu --target llama-server --parallel 3
```

The local build used CMake 4.1.2 in an ignored tooling environment. Native CPU
flags make the binary hardware-specific; record the new checksum on another
machine. Binary equality is not required across different hardware/build tools.

## Freeze and run

Generate the unchanged context profile on dev-v1 first. The same command on
dev-v2 uses its previously frozen context packet. Use fresh paths everywhere.

```bash
tools/predict-isolated.sh data/local/snapshots/dev-v1-final-a/inference_inputs/tasks.jsonl \
  results/runs/cpu-smoke-context context
python3 tools/configure-cpu-run.py \
  --binary .develop/backends/llama.cpp/build-cpu/bin/llama-server \
  --build-dir .develop/backends/llama.cpp/build-cpu \
  --inputs results/runs/cpu-smoke-context/tasks.jsonl --campaign cpu-smoke-dev-v1 \
  --run-budget-s 3600 --task-timeout-s 600 --output .develop/cpu-smoke-config.json
tools/llama-isolated.sh results/runs/cpu-smoke-context/tasks.jsonl \
  .develop/cpu-smoke-config.json models/Qwen3-4B-Instruct-2507-Q4_K_M.gguf \
  .develop/backends/llama.cpp/build-cpu/bin/llama-server \
  configs/prompts/localization-v1.txt results/runs/cpu-smoke-dev-v1
uv run eai-evaluate --predictions results/runs/cpu-smoke-dev-v1/run/predictions \
  --gold data/local/snapshots/dev-v1-final-a/gold/labels.jsonl \
  --output results/runs/cpu-smoke-dev-v1-evaluation
```

The configuration helper records actual CMake cache/compiler and checks pinned,
clean backend source; the runner checks model, binary, prompt and input hashes.
Run a synthetic native-API probe before the smoke; mark its configuration with
`--synthetic`. Freeze dev-v2 deadlines only after measuring the old smoke, before
new model generation. Interrupted campaigns retain the full selected population
with explicit unattempted rows and cannot be described as completed baselines.

The namespace contains both the HTTP client and model server; loopback access
works inside it while external routes are absent. Artifacts include the namespace
probe, native template, raw messages/rendered prompts, token IDs, SSE traces,
errors, effective generation settings and checksums. These private records may
contain issue/source text. Compact public reports must omit source-bearing logs.

Request latency includes native rendering/tokenization, prefill, decoding and
validation; model load/warmup and context preparation are separate. Per-task server
CPU time and monetary cost remain null. Whole-server lifetime CPU time and peak
RSS are recorded separately. Interrupted received-token counts are lower bounds,
not a complete estimate of server work. Quantized CPU results cannot support
claims about GPU serving or unquantized model quality.
