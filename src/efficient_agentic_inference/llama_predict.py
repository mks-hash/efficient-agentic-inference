"""Isolated llama.cpp inference with native rendering and streamed, gold-free evidence."""

from __future__ import annotations

import argparse
import hashlib
import http.client
import json
import platform
import re
import resource
import subprocess
import time
from pathlib import Path

from .inference import PreparedInference, prediction_error
from .records import digest, encoded, jsonl, read_jsonl, write_artifacts

HOST, PORT = "127.0.0.1", 8080


def gpu_seconds(config: dict) -> int | None:
    return 0 if config["execution"].get("device", "cpu") == "cpu" else None


def gpu_layers(config: dict) -> str:
    device = config["execution"].get("device", "cpu")
    if device not in {"cpu", "cuda"}:
        raise ValueError("unsupported_execution_device")
    return "0" if device == "cpu" else "999"


def require_full_offload(log: str) -> None:
    matches = re.findall(r"offloaded (\d+)/(\d+) layers to GPU", log)
    if not matches or any(int(done) == 0 or done != total for done, total in matches):
        raise ValueError("full_gpu_offload_not_confirmed")


def file_digest(path: Path) -> str:
    with path.open("rb") as source:
        return hashlib.file_digest(source, "sha256").hexdigest()


def remaining(deadline: float) -> float:
    seconds = deadline - time.monotonic()
    if seconds <= 0:
        raise TimeoutError("task_deadline_exceeded")
    return seconds


def request(endpoint: str, payload: dict | None, deadline: float):
    connection = http.client.HTTPConnection(HOST, PORT, timeout=remaining(deadline))
    connection.connect()
    sock = connection.sock
    connection.request(
        "GET" if payload is None else "POST",
        endpoint,
        body=None if payload is None else json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
    )
    sock.settimeout(remaining(deadline))
    response = connection.getresponse()
    return connection, sock, response


def post(endpoint: str, payload: dict | None, deadline: float) -> dict:
    connection, sock, response = request(endpoint, payload, deadline)
    try:
        sock.settimeout(remaining(deadline))
        raw = response.read().decode()
        if response.status != 200:
            raise RuntimeError(f"backend_http_{response.status}: {raw}")
        return json.loads(raw)
    finally:
        connection.close()


def token_ids(value: object) -> bool:
    return isinstance(value, list) and all(type(i) is int and i >= 0 for i in value)


def consume_event(event: dict, evidence: dict) -> None:
    if not isinstance(event, dict):
        raise ValueError("stream_event_must_be_an_object")
    if "error" in event:
        raise RuntimeError(f"backend_error: {event['error']}")
    if event.get("stop") is True:
        evidence["final_response"] = event
        return
    if "prompt_progress" in event:
        evidence["prompt_progress"] = event["prompt_progress"]
        return
    tokens = event.get("tokens", [])
    if not token_ids(tokens):
        raise ValueError("invalid_generated_token_ids")
    evidence["output_token_ids"].extend(tokens)
    content = event.get("content", "")
    if not isinstance(content, str):
        raise ValueError("invalid_stream_content")
    evidence["raw_output"] += content


def stream(payload: dict, deadline: float, evidence: dict, trace: Path) -> None:
    connection, sock, response = request("/completion", payload, deadline)
    try:
        if response.status != 200:
            sock.settimeout(remaining(deadline))
            body = response.read().decode()
            evidence["http_error_body"] = body
            raise RuntimeError(f"backend_http_{response.status}: {body}")
        with trace.open("wb") as saved:
            while True:
                sock.settimeout(remaining(deadline))
                line = response.readline()
                if not line:
                    break
                saved.write(line)
                saved.flush()
                if line.startswith(b"data: "):
                    event = json.loads(line[6:])
                    consume_event(event, evidence)
                    if event.get("stop") is True:
                        break
        if evidence["final_response"] is None:
            raise RuntimeError("stream_ended_without_final_response")
    finally:
        response.close()
        connection.close()


def classify(evidence: dict, candidates: set[str], config: dict) -> list[str]:
    final = evidence["final_response"]
    if final is None:
        raise ValueError("missing_final_response")
    if final.get("truncated"):
        raise ValueError("context_truncated")
    if final.get("stop_type") != "eos":
        raise ValueError(f"completion_stop_{final.get('stop_type')}")
    if final.get("tokens_evaluated") != len(evidence["input_token_ids"]):
        raise ValueError("input_token_provenance_mismatch")
    if final.get("tokens_predicted") != len(evidence["output_token_ids"]):
        raise ValueError("output_token_provenance_mismatch")
    settings = final.get("generation_settings", {})
    if not isinstance(settings, dict):
        raise ValueError("invalid_generation_settings")
    for name, expected in {
        "seed": 0,
        "temperature": 0,
        "n_predict": config["decoding"]["max_output_tokens"],
    }.items():
        if settings.get(name) != expected:
            raise ValueError(f"effective_decoding_mismatch_{name}")
    ranked = json.loads(evidence["raw_output"])
    error = prediction_error(ranked, candidates)
    if error:
        raise ValueError(error)
    if len(ranked) > 10:
        raise ValueError("more_than_ten_predictions")
    return ranked


def infer(prepared: PreparedInference, config: dict, system: str, folder: Path, deadline: float):
    task = prepared.instance
    evidence = {
        "instance_id": task.instance_id,
        "rendered_prompt": None,
        "input_token_ids": None,
        "output_token_ids": [],
        "raw_output": "",
        "final_response": None,
    }
    ranked, reason, disposition = [], prepared.failure_reason, "preparation_failed"
    start = time.monotonic()
    client_cpu = time.process_time()
    if prepared.preparation_status == "prepared":
        disposition = "runtime_error"
        try:
            user = encoded(
                {
                    "issue": task.issue,
                    "candidates": [{"path": c.path, "text": c.text} for c in task.candidates],
                }
            ).decode()
            evidence["messages"] = [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ]
            evidence["rendered_prompt"] = post(
                "/apply-template", {"messages": evidence["messages"]}, deadline
            )["prompt"]
            ids = post(
                "/tokenize",
                {
                    "content": evidence["rendered_prompt"],
                    "add_special": False,
                    "parse_special": True,
                },
                deadline,
            )["tokens"]
            if not token_ids(ids) or not ids:
                raise ValueError("invalid_input_token_ids")
            evidence["input_token_ids"] = ids
            if (
                len(ids) + config["decoding"]["max_output_tokens"]
                > config["execution"]["context_tokens"]
            ):
                raise ValueError("context_overflow_before_generation")
            payload = {
                "prompt": ids,
                "n_predict": config["decoding"]["max_output_tokens"],
                "temperature": 0,
                "seed": 0,
                "cache_prompt": False,
                "stream": True,
                "return_tokens": True,
                "return_progress": True,
                "sse_ping_interval": 5,
                "samplers": ["temperature"],
                "repeat_penalty": 1,
                "frequency_penalty": 0,
                "presence_penalty": 0,
            }
            evidence["request"] = payload
            stream(payload, deadline, evidence, folder / "stream.sse")
            disposition = "invalid_output"
            ranked = classify(evidence, {c.path for c in task.candidates}, config)
            disposition, reason = "valid", None
        except (
            ValueError,
            KeyError,
            TypeError,
            OSError,
            RuntimeError,
            http.client.HTTPException,
        ) as exc:
            ranked = []
            reason = f"{type(exc).__name__}: {exc}"
    wall_ms = (time.monotonic() - start) * 1000
    evidence["client_cpu_ms"] = (time.process_time() - client_cpu) * 1000
    evidence["disposition"], evidence["failure_reason"] = disposition, reason
    (folder / "evidence.json").write_bytes(encoded(evidence))
    return {
        "schema_version": "2.0.0",
        "instance_id": task.instance_id,
        "ranked_files": ranked,
        "raw_output": evidence["raw_output"],
        "disposition": disposition,
        "failure_reason": reason,
        "candidate_paths": [c.path for c in task.candidates],
        "candidate_sha256": prepared.candidate_sha256,
        "measurements": {
            "wall_ms": wall_ms if prepared.preparation_status == "prepared" else None,
            "cpu_ms": None,
            "input_tokens": len(evidence["input_token_ids"])
            if evidence["input_token_ids"] is not None
            else None,
            "output_tokens": len(evidence["output_token_ids"]) if evidence.get("request") else None,
            "gpu_seconds": gpu_seconds(config),
            "monetary_usd": None,
        },
    }


def run(
    inputs: Path, config_path: Path, model: Path, binary: Path, prompt: Path, output: Path
) -> dict:
    config = json.loads(config_path.read_text())
    layers = gpu_layers(config)
    if config["decoding"] != {
        "attempts": 1,
        "max_output_tokens": 512,
        "repair": False,
        "retries": 0,
        "seed": 0,
        "temperature": 0,
    }:
        raise ValueError("unsupported_decoding_contract")
    if config.get("input_identity", {}).get("sha256") not in (None, digest(inputs.read_bytes())):
        raise ValueError("input_checksum_mismatch")
    if file_digest(model) != config["artifact"]["sha256"]:
        raise ValueError("model_checksum_mismatch")
    if file_digest(binary) != config["backend"]["binary_sha256"]:
        raise ValueError("backend_binary_checksum_mismatch")
    if digest(prompt.read_bytes()) != config["prompt"]["sha256"]:
        raise ValueError("prompt_checksum_mismatch")
    instances = [PreparedInference.from_record(r) for r in read_jsonl(inputs)]
    ids = [r.instance.instance_id for r in instances]
    if not ids or len(set(ids)) != len(ids):
        raise ValueError("instance_ids_must_be_unique_and_nonempty")
    output.mkdir(parents=True, exist_ok=False)
    (output / "attempts").mkdir()
    (output / "execution-config.json").write_bytes(encoded(config))
    if layers != "0":
        metadata = subprocess.check_output(
            [
                "nvidia-smi",
                "--query-gpu=index,name,memory.total,driver_version",
                "--format=csv,noheader,nounits",
            ],
            timeout=15,
        )
        (output / "gpu-metadata.csv").write_bytes(metadata)
    command = [
        str(binary),
        "--model",
        str(model),
        "--host",
        HOST,
        "--port",
        str(PORT),
        "--log-verbosity",
        "4",
        "--ctx-size",
        str(config["execution"]["context_tokens"]),
        "--parallel",
        "1",
        "--threads",
        str(config["execution"]["threads"]),
        "--threads-batch",
        str(config["execution"]["threads"]),
        "--n-gpu-layers",
        layers,
        "--no-context-shift",
        "--cache-ram",
        "0",
        "--batch-size",
        "512",
        "--ubatch-size",
        "128",
        "--jinja",
    ]
    started = time.monotonic()
    usage_before = resource.getrusage(resource.RUSAGE_CHILDREN)
    predictions = []
    with (output / "server.log").open("wb") as log:
        server = subprocess.Popen(command, stdout=log, stderr=log)
        try:
            deadline = started + config["execution"]["startup_timeout_s"]
            while True:
                if server.poll() is not None:
                    raise RuntimeError(f"backend_startup_exit_{server.returncode}")
                try:
                    health = post("/health", None, min(deadline, time.monotonic() + 1))
                    if health.get("status") == "ok":
                        break
                except (OSError, RuntimeError, http.client.HTTPException):
                    remaining(deadline)
                    time.sleep(0.25)
            load_ms = (time.monotonic() - started) * 1000
            if layers != "0":
                require_full_offload((output / "server.log").read_text())
            props = post("/props", None, time.monotonic() + 10)
            (output / "backend-props.json").write_bytes(encoded(props))
            if props.get("model_path") != str(model):
                raise ValueError("loaded_model_path_mismatch")
            if (
                props.get("default_generation_settings", {}).get("n_ctx")
                != config["execution"]["context_tokens"]
            ):
                raise ValueError("effective_context_capacity_mismatch")
            if props.get("total_slots") != 1:
                raise ValueError("effective_slot_count_mismatch")
            template = props.get("chat_template")
            if not isinstance(template, str) or not template:
                raise ValueError("missing_native_chat_template")
            (output / "chat-template.txt").write_text(template)
            run_deadline = time.monotonic() + config["execution"]["run_budget_s"]
            for index, prepared in enumerate(instances):
                folder = output / "attempts" / f"{index:03d}"
                folder.mkdir()
                if time.monotonic() >= run_deadline:
                    prediction = {
                        "schema_version": "2.0.0",
                        "instance_id": prepared.instance.instance_id,
                        "ranked_files": [],
                        "raw_output": None,
                        "disposition": "runtime_error",
                        "failure_reason": "run_budget_exhausted_not_attempted",
                        "candidate_paths": [c.path for c in prepared.instance.candidates],
                        "candidate_sha256": prepared.candidate_sha256,
                        "measurements": {
                            "wall_ms": 0,
                            "cpu_ms": None,
                            "input_tokens": 0,
                            "output_tokens": 0,
                            "gpu_seconds": gpu_seconds(config),
                            "monetary_usd": None,
                        },
                    }
                else:
                    prediction = infer(
                        prepared,
                        config,
                        prompt.read_text(),
                        folder,
                        min(
                            run_deadline,
                            time.monotonic() + config["execution"]["per_task_timeout_s"],
                        ),
                    )
                predictions.append(prediction)
                (folder / "prediction.json").write_bytes(encoded(prediction))
                print(
                    json.dumps(
                        {
                            "completed": index + 1,
                            "selected": len(instances),
                            "instance_id": prepared.instance.instance_id,
                            "disposition": prediction["disposition"],
                            "reason": prediction["failure_reason"],
                            "wall_ms": prediction["measurements"]["wall_ms"],
                        }
                    ),
                    flush=True,
                )
        finally:
            server.terminate()
            try:
                server.wait(timeout=10)
            except subprocess.TimeoutExpired:
                server.kill()
                server.wait()
    usage = resource.getrusage(resource.RUSAGE_CHILDREN)
    phases = {
        "backend_load_warmup_ms": load_ms,
        "backend_lifetime_wall_ms": (time.monotonic() - started) * 1000,
        "backend_cpu_seconds": usage.ru_utime
        + usage.ru_stime
        - usage_before.ru_utime
        - usage_before.ru_stime,
        "backend_peak_rss_kib": usage.ru_maxrss,
        "gpu_seconds": gpu_seconds(config),
        "monetary_usd": None,
        "command": command,
        "child_exit_code": server.returncode,
    }
    (output / "phases.json").write_bytes(encoded(phases))
    manifest = {
        "schema_version": "2.0.0",
        "program": "llama-predict-" + config["execution"].get("device", "cpu"),
        "synthetic": config["execution"]["synthetic"],
        "inputs_sha256": digest(inputs.read_bytes()),
        "execution_config_sha256": digest(config_path.read_bytes()),
        "model": config["model"],
        "artifact": config["artifact"],
        "backend": config["backend"],
        "code_identity": config.get("code_identity"),
        "hardware": config.get("hardware"),
        "chat_template_sha256": digest(template.encode()),
        "prompt": config["prompt"],
        "decoding": config["decoding"],
        "execution": config["execution"],
        "python": platform.python_version(),
        "platform": platform.platform(),
        "runtime_sources": {
            name: digest((Path(__file__).parent / name).read_bytes())
            for name in ("__init__.py", "inference.py", "records.py", "llama_predict.py")
        },
        "measurement_boundary": (
            "request rendering/tokenization/prefill/decode/validation; excludes model load "
            "and context preparation; cpu_ms unknown per task, total backend CPU separately "
            "measured; interrupted output token counts are received-token lower bounds"
        ),
        "cost_reason": "No price/invoice joined; no general latency/economics claim",
    }
    write_artifacts(
        output / "predictions",
        {
            "manifest.json": encoded(manifest),
            "predictions.jsonl": jsonl(predictions),
            "predictions.sha256": (digest(jsonl(predictions)) + "\n").encode(),
        },
    )
    (output / "SHA256SUMS").write_text(
        "".join(
            f"{file_digest(path)}  {path.relative_to(output).as_posix()}\n"
            for path in sorted(output.rglob("*"))
            if path.is_file()
        )
    )
    return {
        "selected": len(predictions),
        "valid": sum(p["disposition"] == "valid" for p in predictions),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("inputs", "config", "model", "binary", "prompt", "output"):
        parser.add_argument(f"--{name}", type=Path, required=True)
    args = vars(parser.parse_args())
    args["config_path"] = args.pop("config")
    try:
        print(json.dumps(run(**args)))
    except (ValueError, OSError, RuntimeError) as exc:
        parser.exit(2, f"error: {exc}\n")


if __name__ == "__main__":
    main()
