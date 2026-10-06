#!/usr/bin/env python3
"""Freeze a llama.cpp CPU/CUDA configuration before inference; no labels are read."""

import argparse
import hashlib
import json
import platform
import subprocess
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--binary", type=Path, required=True)
parser.add_argument("--build-dir", type=Path, required=True)
parser.add_argument("--inputs", type=Path, required=True)
parser.add_argument("--campaign", required=True)
parser.add_argument("--run-budget-s", type=int, default=3600)
parser.add_argument("--task-timeout-s", type=int, default=600)
parser.add_argument("--synthetic", action="store_true")
parser.add_argument("--device", choices=("cpu", "cuda"), default="cpu")
parser.add_argument("--code-identity-json", type=Path)
parser.add_argument("--output", type=Path, required=True)
args = parser.parse_args()
if args.run_budget_s <= 0 or args.task_timeout_s <= 0:
    parser.error("Budgets must be positive")
config = json.loads(Path("configs/untuned-dev-v2.json").read_text())
config["backend"]["binary_sha256"] = hashlib.sha256(args.binary.read_bytes()).hexdigest()
config["backend"]["binary_identity_status"] = "PASS"
if args.binary.resolve() != (args.build_dir / "bin/llama-server").resolve():
    parser.error("Binary must belong to the recorded build directory")
cache_path = args.build_dir / "CMakeCache.txt"
cache = dict(
    (line.split(":", 1)[0], line.split("=", 1)[1])
    for line in cache_path.read_text().splitlines()
    if not line.startswith(("//", "#")) and ":" in line and "=" in line
)
source = Path(cache["CMAKE_HOME_DIRECTORY"])
backend_revision = subprocess.check_output(
    ["git", "-C", str(source), "rev-parse", "HEAD"], text=True
).strip()
if backend_revision != config["backend"]["revision"]:
    parser.error("Backend source revision differs from pinned revision")
if subprocess.check_output(["git", "-C", str(source), "status", "--porcelain"], text=True):
    parser.error("Backend source must be clean")
if cache["GGML_CUDA"] != ("ON" if args.device == "cuda" else "OFF"):
    parser.error("CUDA build flag must match requested execution device")
config["backend"]["build"] = {
    "cmake": ".".join(cache[f"CMAKE_CACHE_{part}_VERSION"] for part in ("MAJOR", "MINOR", "PATCH")),
    "compiler": subprocess.check_output(
        [cache["CMAKE_CXX_COMPILER"], "--version"], text=True
    ).splitlines()[0],
    "cache_sha256": hashlib.sha256(cache_path.read_bytes()).hexdigest(),
    "flags": {
        key: cache[key]
        for key in (
            "CMAKE_BUILD_TYPE",
            "BUILD_SHARED_LIBS",
            "GGML_CUDA",
            "GGML_NATIVE",
            "GGML_BLAS",
            "LLAMA_OPENSSL",
            "LLAMA_BUILD_TESTS",
            "LLAMA_BUILD_SERVER",
        )
    },
}
if args.device == "cuda":
    config["backend"]["build"]["cuda_architectures"] = cache["CMAKE_CUDA_ARCHITECTURES"]
    config["backend"]["build"]["cuda_compiler_version"] = subprocess.check_output(
        [cache["CMAKE_CUDA_COMPILER"], "--version"], text=True
    )
config["execution"] = {
    "device": args.device,
    "context_tokens": 16384,
    "threads": 4,
    "startup_timeout_s": 180,
    "per_task_timeout_s": args.task_timeout_s,
    "run_budget_s": args.run_budget_s,
    "synthetic": args.synthetic,
}
config["campaign"] = args.campaign
config["input_identity"] = {"sha256": hashlib.sha256(args.inputs.read_bytes()).hexdigest()}
config["code_identity"] = (
    json.loads(args.code_identity_json.read_text())
    if args.code_identity_json
    else {
        "revision": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "dirty": bool(subprocess.check_output(["git", "status", "--porcelain"], text=True)),
    }
)
config["hardware"] = {
    "cpu": subprocess.check_output(["lscpu"], text=True),
    "ram": Path("/proc/meminfo").read_text().splitlines()[0],
    "kernel": platform.release(),
    "gpu_layers": 0 if args.device == "cpu" else 999,
}
ids = [
    json.loads(line)["instance"]["instance_id"]
    for line in args.inputs.read_text().splitlines()
    if line.strip()
]
config["population"] = {
    "role": "synthetic API probe" if args.synthetic else args.campaign,
    "selected": len(ids),
    "instance_ids_sha256": hashlib.sha256(json.dumps(sorted(ids)).encode()).hexdigest(),
}
config["execution_status"] = "FROZEN_NOT_RUN"
config["status"] = "Frozen local execution configuration; evidence gates require run artifacts"
with args.output.open("x") as output:
    json.dump(config, output, indent=2, sort_keys=True)
    output.write("\n")
print(json.dumps({"config_sha256": hashlib.sha256(args.output.read_bytes()).hexdigest()}))
