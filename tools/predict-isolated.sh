#!/usr/bin/env bash
set -euo pipefail
if [ "$#" -ne 2 ]; then
  echo 'Usage: tools/predict-isolated.sh INPUTS_JSONL FRESH_OUTPUT_DIR' >&2
  exit 2
fi
project_root=$(cd "$(dirname "$0")/.." && pwd)
input_file=$(realpath "$1")
output_dir=$(realpath -m "$2")
if [ -e "$output_dir" ]; then
  echo 'Output exists; refusing to overwrite' >&2
  exit 2
fi
staging=$(mktemp -d)
trap 'rm -rf "$staging"' EXIT
mkdir -p "$staging/code/efficient_agentic_inference" "$staging/input" "$staging/output"
for module in __init__ inference predict records; do
  cp "$project_root/src/efficient_agentic_inference/$module.py" "$staging/code/efficient_agentic_inference/"
done
cp "$input_file" "$staging/input/tasks.jsonl"
host_netns=$(readlink /proc/self/ns/net)
cat > "$staging/probe.py" <<'PY'
import json, os, pathlib, socket
project_visible = pathlib.Path(os.environ['HIDDEN_PROJECT']).exists()
same_network = os.readlink('/proc/self/ns/net') == os.environ['HOST_NETNS']
sock = socket.socket(); sock.settimeout(0.2)
network_errno = sock.connect_ex(('198.51.100.1', 9)); sock.close()
route_count = len(pathlib.Path('/proc/net/route').read_text().splitlines()) - 1
assert not project_visible and not same_network and route_count == 0 and network_errno != 0
print(json.dumps(dict(project_visible=project_visible, separate_network_namespace=not same_network,
                     network_errno=network_errno, ipv4_routes=route_count)))
PY
# Probe and predict execute in the SAME namespace and mount view. The inference
# program does not import the probe; it receives no hidden-project metadata.
bwrap --unshare-all --die-with-parent --new-session --clearenv \
  --ro-bind /usr /usr --ro-bind /lib /lib --ro-bind /lib64 /lib64 \
  --proc /proc --dev /dev --tmpfs /tmp \
  --ro-bind "$staging/code" /code --ro-bind "$staging/input" /inputs \
  --ro-bind "$staging/probe.py" /probe.py --bind "$staging/output" /output \
  --setenv PYTHONPATH /code --setenv PYTHONDONTWRITEBYTECODE 1 \
  --setenv HIDDEN_PROJECT "$project_root" --setenv HOST_NETNS "$host_netns" --chdir /tmp \
  /usr/bin/sh -c '
    /usr/bin/python3 /probe.py > /output/isolation.json || exit 1
    unset HIDDEN_PROJECT HOST_NETNS
    exec /usr/bin/python3 -m efficient_agentic_inference.predict \
      --inputs /inputs/tasks.jsonl --output /output/run
  '
cp "$staging/output/isolation.json" "$staging/output/run/isolation.json"
/usr/bin/python3 - "$staging/output/run" <<'PY'
import hashlib, json, pathlib, sys
root = pathlib.Path(sys.argv[1])
path = root / 'checksums.json'
checksums = json.loads(path.read_text())
checksums['isolation.json'] = hashlib.sha256((root / 'isolation.json').read_bytes()).hexdigest()
path.write_text(json.dumps(checksums, sort_keys=True, indent=2) + '\n')
PY
mkdir -p "$(dirname "$output_dir")"
mv -T "$staging/output/run" "$output_dir"
