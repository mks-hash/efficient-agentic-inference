"""Tiny local Parquet fixtures exercise population and snapshot invariants."""

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

from test_pipeline import MODIFIED, allowed

from efficient_agentic_inference.records import digest, encoded, read_jsonl
from efficient_agentic_inference.snapshot import build, freeze_splits


@unittest.skipUnless(
    importlib.util.find_spec("pyarrow"), "Install the data extra for Parquet tests"
)
class SnapshotContracts(unittest.TestCase):
    def sources(self, root):
        import pyarrow as pa
        import pyarrow.parquet as pq

        upstream = root / "upstream"
        upstream.mkdir()
        pq.write_table(
            pa.Table.from_pylist([{**allowed("dev-task"), "patch": MODIFIED}]),
            upstream / "dev.parquet",
        )
        pq.write_table(
            pa.Table.from_pylist([{**allowed("final-task"), "problem_statement": "other issue"}]),
            upstream / "verified.parquet",
        )
        sources = {
            "schema_version": "1.0.0",
            "sources": [
                {
                    "dataset": "synthetic/local",
                    "revision": "fixture",
                    "local_name": name,
                    "sha256": digest((upstream / name).read_bytes()),
                }
                for name in ("dev.parquet", "verified.parquet")
            ],
        }
        config = root / "sources.json"
        config.write_bytes(encoded(sources))
        return config, upstream

    def test_frozen_split_rebuild_and_final_disjointness(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            config, upstream = self.sources(root)
            freeze_splits(config, upstream, root / "s1", 1, "seed")
            freeze_splits(config, upstream, root / "s2", 1, "seed")
            self.assertEqual(
                (root / "s1/dev-v1.json").read_bytes(), (root / "s2/dev-v1.json").read_bytes()
            )
            dev = json.loads((root / "s1/dev-v1.json").read_text())
            final = json.loads((root / "s1/evaluation-v1.json").read_text())
            self.assertFalse(
                {r["instance_id"] for r in dev["instances"]} & set(final["instance_ids"])
            )

    def test_failed_checkout_keeps_selected_task_and_known_labels(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            config, upstream = self.sources(root)
            freeze_splits(config, upstream, root / "splits", 1, "seed")
            manifest = build(
                config,
                upstream,
                root / "splits/dev-v1.json",
                root / "snapshot",
                root / "missing-cache",
                True,
            )
            self.assertEqual(manifest["selected"], 1)
            self.assertEqual(manifest["prepared"], 0)
            self.assertEqual(manifest["labeled"], 1)
            inputs = read_jsonl(root / "snapshot/inference_inputs/tasks.jsonl")
            self.assertEqual(inputs[0]["preparation_status"], "failed_checkout")
            self.assertTrue(inputs[0]["failure_reason"])

    def test_upstream_checksum_change_blocks_rebuild(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            config, upstream = self.sources(root)
            (upstream / "dev.parquet").write_bytes(b"different dataset")
            with self.assertRaises(ValueError):
                freeze_splits(config, upstream, root / "split", 1, "seed")
