"""Previously exposed development data cannot enter a new research population."""

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

import test_snapshot
from test_pipeline import allowed

from efficient_agentic_inference.records import encoded
from efficient_agentic_inference.snapshot import issue_fingerprint, select


class DevelopmentSelection(unittest.TestCase):
    def test_previous_ids_and_equivalent_issues_excluded_before_selection(self):
        seen = allowed("seen")
        equivalent = {**seen, "instance_id": "renamed-issue"}
        fresh = {**allowed("fresh"), "problem_statement": "a different issue"}
        chosen, exclusions = select(
            [seen, equivalent, fresh],
            [],
            1,
            "seed",
            frozenset({"seen"}),
            frozenset({issue_fingerprint(seen)}),
        )
        self.assertEqual([r["instance_id"] for r in chosen], ["fresh"])
        self.assertEqual(len(exclusions), 2)
        self.assertTrue(all(r["reason"] == "previous_development_exposure" for r in exclusions))

    def test_exclusions_do_not_resample_when_population_exhausted(self):
        with self.assertRaises(ValueError):
            select([allowed("seen")], [], 1, "seed", frozenset({"seen"}))


@unittest.skipUnless(importlib.util.find_spec("pyarrow"), "Install the data extra")
class DevelopmentFreeze(unittest.TestCase):
    sources = test_snapshot.SnapshotContracts.sources

    def test_named_population_preserves_sources_and_exclusion_identity(self):
        from efficient_agentic_inference.records import digest
        from efficient_agentic_inference.snapshot import freeze_splits

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            config, upstream = self.sources(root)
            freeze_splits(config, upstream, root / "original", 1, "seed")
            original = root / "original/dev-v1.json"
            record = json.loads(original.read_text())
            record["name"] = "previous-dev"
            record["instances"] = [
                {
                    "instance_id": "previous-task",
                    "repo": "fixture/repo",
                    "base_commit": "a" * 40,
                    "issue_sha256": "0" * 64,
                }
            ]
            original.write_bytes(encoded(record))
            freeze_splits(config, upstream, root / "new", 1, "seed", "dev-v2", [original])
            new = json.loads((root / "new/dev-v2.json").read_text())
            self.assertEqual(new["name"], "dev-v2")
            self.assertEqual(
                new["excluded_development_splits"],
                [{"name": "previous-dev", "sha256": digest(original.read_bytes())}],
            )
            self.assertEqual(new["sources"], record["sources"])

    def test_mismatched_excluded_source_is_rejected(self):
        from efficient_agentic_inference.snapshot import freeze_splits

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            config, upstream = self.sources(root)
            excluded = root / "excluded.json"
            excluded.write_bytes(encoded({"sources": {"wrong": "revision"}}))
            with self.assertRaises(ValueError):
                freeze_splits(config, upstream, root / "new", 1, "seed", "dev-v2", [excluded])
