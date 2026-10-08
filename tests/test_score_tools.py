"""Independent simulated artifact checks, not research or native model evidence."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from efficient_agentic_inference.records import digest, encoded, jsonl, write_artifacts

ROOT = Path(__file__).resolve().parents[1]


class ScoreToolContracts(unittest.TestCase):
    def artifacts(self, root):
        campaign = json.loads((ROOT / "configs/score-ranking-validation-v2.json").read_text())
        split = json.loads((ROOT / campaign["population"]["split"]).read_text())
        for arm, config_path in campaign["arms"].items():
            config = json.loads((ROOT / config_path).read_text())
            scoring = arm.endswith("-scores")
            predictions, metrics = [], []
            for task in split["instances"]:
                predictions.append(
                    {
                        "instance_id": task["instance_id"],
                        "candidate_paths": ["a.py", "b.py", "c.py"],
                        "candidate_sha256": "a" * 64,
                        "disposition": "valid",
                        "ranked_files": ["b.py", "c.py"] if scoring else ["a.py"],
                        "raw_output": "[0,75,75]" if scoring else '["a.py"]',
                    }
                )
                metrics.append(
                    {
                        "instance_id": task["instance_id"],
                        "disposition": "valid",
                        "all_files": {
                            "gold_file_count": 1,
                            "candidate_recall_ceiling": 1.0,
                            "recall_at_k": {"5": float(scoring)},
                            "strict_success_at_k": {"5": scoring},
                        },
                    }
                )
            manifest = {
                key: config[key]
                for key in ("model", "artifact", "prompt", "decoding", "output_constraint")
            }
            manifest.update(synthetic=False, inputs_sha256="b" * 64)
            if scoring:
                manifest["score_mapping"] = campaign["score_mapping"]
            data = jsonl(predictions)
            write_artifacts(
                root / arm / "predictions",
                {
                    "predictions.jsonl": data,
                    "manifest.json": encoded(manifest),
                },
            )
            write_artifacts(
                root / arm / "evaluation",
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
                "tools/analyze-score-ranking.py",
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

    def test_new_recipe_names_and_ties_do_not_change_the_primary_role(self):
        with tempfile.TemporaryDirectory() as temporary:
            runs, output = (Path(temporary) / name for name in ("runs", "comparison"))
            self.artifacts(runs)
            result = self.run_tool(runs, output)
            self.assertEqual(result.returncode, 0, result.stderr)
            record = json.loads((output / "comparison.json").read_text())
            self.assertEqual(record["contract"], "score-ranking-validation-v2")
            self.assertTrue(record["contrasts"]["S"]["numerical_signal_rule_pass"])
            self.assertEqual(record["contrasts"]["S"]["contrast"], ["S-scores", "S-paths"])
            self.assertEqual(record["contrasts"]["G"]["role"], "secondary_exploratory")
            self.assertEqual(record["contrasts"]["S"]["repository_blocks"], 4)
            self.assertEqual(record["score_diagnostics"]["S-scores"]["zero_entries"], 30)
            self.assertEqual(record["score_diagnostics"]["S-scores"]["positive_tie_vectors"], 30)
            self.assertEqual(record["technical_gates"], "NOT_ASSESSED_BY_METRICS")
            original = (output / "comparison.json").read_bytes()
            self.assertNotEqual(self.run_tool(runs, output).returncode, 0)
            self.assertEqual((output / "comparison.json").read_bytes(), original)

    def test_rechecks_mapping_and_gold_even_with_updated_transport_hashes(self):
        for target in ("mapping", "gold"):
            with tempfile.TemporaryDirectory() as temporary:
                runs, output = (Path(temporary) / name for name in ("runs", "comparison"))
                self.artifacts(runs)
                folder = runs / "G-scores" / "predictions"
                if target == "mapping":
                    records = [
                        json.loads(line)
                        for line in (folder / "predictions.jsonl").read_text().splitlines()
                    ]
                    records[0]["ranked_files"] = ["c.py", "b.py"]
                    (folder / "predictions.jsonl").write_bytes(jsonl(records))
                evaluation = runs / "G-scores" / "evaluation"
                summary = json.loads((evaluation / "summary.json").read_text())
                summary["predictions_sha256"] = digest((folder / "predictions.jsonl").read_bytes())
                if target == "gold":
                    summary["gold_sha256"] = "d" * 64
                (evaluation / "summary.json").write_bytes(encoded(summary))
                for directory in (folder, evaluation):
                    checksums = json.loads((directory / "checksums.json").read_text())
                    (directory / "checksums.json").write_bytes(
                        encoded(
                            {name: digest((directory / name).read_bytes()) for name in checksums}
                        )
                    )
                self.assertNotEqual(self.run_tool(runs, output).returncode, 0)
                self.assertFalse(output.exists())
