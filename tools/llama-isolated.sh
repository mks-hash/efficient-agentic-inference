#!/usr/bin/env bash
set -euo pipefail
if [ "$#" -ne 6 ]; then
  echo 'Usage: llama-isolated.sh INPUT CONFIG MODEL BINARY PROMPT FRESH_OUTPUT' >&2
  exit 2
fi
project_root=$(cd "$(dirname "$0")/.." && pwd)
input_file=$(realpath "$1")
config_file=$(realpath "$2")
model_file=$(realpath "$3")
binary_file=$(realpath "$4")
prompt_file=$(realpath "$5")
output_dir=$(realpath -m "$6")
if [ -e "$output_dir" ]; then
  echo 'Output exists; refusing to overwrite' >&2
  exit 2
fi
mkdir -p "$output_dir"
staging=$(mktemp -d)
trap 'rm -rf "$staging"' EXIT
mkdir -p "$staging/code/efficient_agentic_inference" "$staging/input" "$staging/config"
for module in __init__ inference llama_predict records; do
  cp "$project_root/src/efficient_agentic_inference/$module.py" "$staging/code/efficient_agentic_inference/"
done
cp "$input_file" "$staging/input/tasks.jsonl"
cp "$config_file" "$staging/config/config.json"
cp "$prompt_file" "$staging/config/system.txt"
device=$(/usr/bin/python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["execution"].get("device", "cpu"))' "$config_file")
device_mounts=()
case "$device" in
  cpu) ;;
  cuda)
    device_mounts+=(--ro-bind /sys /sys --ro-bind /etc/ld.so.cache /etc/ld.so.cache)
    for node in /dev/nvidia0 /dev/nvidiactl /dev/nvidia-uvm; do
      if [ ! -e "$node" ]; then echo "Required GPU device absent: $node" >&2; exit 2; fi
      device_mounts+=(--dev-bind "$node" "$node")
    done
    ;;
  *) echo 'Unsupported execution device' >&2; exit 2 ;;
esac
host_netns=$(readlink /proc/self/ns/net)
cat > "$staging/probe.py" <<'PY'
import json, os, pathlib, socket
project_visible = pathlib.Path(os.environ['HIDDEN_PROJECT']).exists()
same_network = os.readlink('/proc/self/ns/net') == os.environ['HOST_NETNS']
sock = socket.socket(); sock.settimeout(0.2)
network_errno = sock.connect_ex(('198.51.100.1', 9)); sock.close()
route_count = len(pathlib.Path('/proc/net/route').read_text().splitlines()) - 1
assert not project_visible and not same_network and route_count == 0 and network_errno != 0
assert not pathlib.Path('/code/efficient_agentic_inference/evaluation.py').exists()
print(json.dumps(dict(project_visible=project_visible, separate_network_namespace=not same_network,
                     evaluator_visible=False, network_errno=network_errno, ipv4_routes=route_count)))
PY
# Client and model server share this isolated namespace; no evaluator, gold,
# repository checkout, Git metadata or host network is mounted.
bwrap --unshare-all --die-with-parent --new-session --clearenv \
  --ro-bind /usr /usr --ro-bind /lib /lib --ro-bind /lib64 /lib64 \
  --proc /proc --dev /dev --tmpfs /tmp \
  "${device_mounts[@]}" \
  --ro-bind "$staging/code" /code --ro-bind "$staging/input" /inputs \
  --ro-bind "$staging/config" /config --ro-bind "$model_file" /model/model.gguf \
  --ro-bind "$binary_file" /backend/llama-server \
  --ro-bind "$staging/probe.py" /probe.py --bind "$output_dir" /output \
  --setenv PYTHONPATH /code --setenv PYTHONDONTWRITEBYTECODE 1 \
  --setenv CUDA_CACHE_PATH /tmp/cuda-cache \
  --setenv HIDDEN_PROJECT "$project_root" --setenv HOST_NETNS "$host_netns" --chdir /tmp \
  /usr/bin/sh -c '
    /usr/bin/python3 /probe.py > /output/isolation.json || exit 1
    unset HIDDEN_PROJECT HOST_NETNS
    exec /usr/bin/python3 -m efficient_agentic_inference.llama_predict \
      --inputs /inputs/tasks.jsonl --config /config/config.json --model /model/model.gguf \
      --binary /backend/llama-server --prompt /config/system.txt --output /output/run
  '
/usr/bin/python3 - "$output_dir" <<'PY'
import hashlib, pathlib, sys
root = pathlib.Path(sys.argv[1])
(root / 'SHA256SUMS').write_text(''.join(
    f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(root).as_posix()}\n'
    for p in sorted(root.rglob('*')) if p.is_file() and p != root / 'SHA256SUMS'
))
PY
