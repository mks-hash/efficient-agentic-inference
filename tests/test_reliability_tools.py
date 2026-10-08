"""Synthetic artifact fixtures exercise CLI checks; headers simulate a research run."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from efficient_agentic_inference.records import digest, encoded, jsonl, write_artifacts

ROOT = Path(__file__).resolve().parents[1]


class ReliabilityToolContracts(unittest.TestCase):
    def artifacts(self, runs):
        campaign = json.loads((ROOT / "configs/reliability-validation-v1.json").read_text())
        split = json.loads((ROOT / campaign["population"]["split"]).read_text())
        for arm, config_path in campaign["arms"].items():
            config = json.loads((ROOT / config_path).read_text())
            improved = arm.endswith("-constrained")
            predictions, metrics = [], []
            for task in split["instances"]:
                disposition = "valid" if improved else "invalid_output"
                predictions.append(
                    {
                        "instance_id": task["instance_id"],
                        "candidate_paths": ["src/fixture.py"],
                        "candidate_sha256": "a" * 64,
                        "disposition": disposition,
                    }
                )
                metrics.append(
                    {
                        "instance_id": task["instance_id"],
                        "disposition": disposition,
                        "all_files": {
                            "gold_file_count": 1,
                            "candidate_recall_ceiling": 1.0,
                            "recall_at_k": {"5": float(improved)},
                            "strict_success_at_k": {"5": improved},
                        },
                    }
                )
            manifest = {key: config[key] for key in ("model", "artifact", "prompt", "decoding")}
            manifest.update(synthetic=False, inputs_sha256="b" * 64)
            if "output_constraint" in config:
                manifest["output_constraint"] = config["output_constraint"]
            data = jsonl(predictions)
            write_artifacts(
                runs / arm / "predictions",
                {
                    "predictions.jsonl": data,
                    "manifest.json": encoded(manifest),
                    "predictions.sha256": (digest(data) + "\n").encode(),
                },
            )
            write_artifacts(
                runs / arm / "evaluation",
                {
                    "metrics.jsonl": jsonl(metrics),
                    "summary.json": encoded(
                        {
                            "predictions_sha256": digest(data),
                            "gold_sha256": "c" * 64,
                            "synthetic": False,
                        }
                    ),
                },
            )

    def run_tool(self, runs, output):
        return subprocess.run(
            [
                sys.executable,
                "tools/analyze-reliability.py",
                "--runs",
                str(runs),
                "--output",
                str(output),
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_valid_pairing_and_immutable_output(self):
        with tempfile.TemporaryDirectory() as temporary:
            runs, output = (Path(temporary) / name for name in ("runs", "comparison"))
            self.artifacts(runs)
            result = self.run_tool(runs, output)
            self.assertEqual(result.returncode, 0, result.stderr)
            record = json.loads((output / "comparison.json").read_text())
            self.assertTrue(record["contrasts"]["S"]["numerical_signal_rule_pass"])
            self.assertEqual(record["contrasts"]["S"]["selected"], 20)
            self.assertEqual(record["contrasts"]["S"]["repository_blocks"], 5)
            self.assertEqual(record["technical_gates"], "NOT_ASSESSED_BY_METRICS")
            original = (output / "comparison.json").read_bytes()
            self.assertNotEqual(self.run_tool(runs, output).returncode, 0)
            self.assertEqual((output / "comparison.json").read_bytes(), original)

    def test_tampering_and_mismatched_gold_cannot_be_ignored(self):
        for tamper in (True, False):
            with tempfile.TemporaryDirectory() as temporary:
                runs, output = (Path(temporary) / name for name in ("runs", "comparison"))
                self.artifacts(runs)
                folder = runs / "G-free" / "evaluation"
                summary = json.loads((folder / "summary.json").read_text())
                summary["gold_sha256"] = "d" * 64
                (folder / "summary.json").write_bytes(encoded(summary))
                if not tamper:
                    checksums = json.loads((folder / "checksums.json").read_text())
                    checksums["summary.json"] = digest((folder / "summary.json").read_bytes())
                    (folder / "checksums.json").write_bytes(encoded(checksums))
                self.assertNotEqual(self.run_tool(runs, output).returncode, 0)
                self.assertFalse(output.exists())
