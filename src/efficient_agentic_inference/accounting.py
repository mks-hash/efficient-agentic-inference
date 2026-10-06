"""Post-evaluation cost accounting; never supplies inference inputs or invented rates."""

from __future__ import annotations

import argparse
import json
import math
from decimal import Decimal
from pathlib import Path

import jsonschema

from .records import digest, encoded, write_artifacts

COMPONENTS = {"compute", "storage", "external_ip", "network", "external_preparation", "other"}


def cost_summary(ledger: dict, evaluation: dict, schema: dict) -> dict:
    jsonschema.validate(ledger, schema)
    if evaluation.get("synthetic") is not ledger["synthetic"]:
        raise ValueError("Synthetic and measured evidence must not be mixed")
    components = ledger["components"]
    names = [item["name"] for item in components]
    if len(names) != len(set(names)) or set(names) != COMPONENTS:
        raise ValueError("Require each accounting component exactly once")
    selected = evaluation["selected"]
    if type(selected) is not int or selected < 1 or selected != ledger["selected"]:
        raise ValueError("Accounting and evaluation populations must match")
    quality = evaluation["all_files"]
    successes, unknown = quality["strict_successes_at_5"], quality["unknown_label_tasks"]
    if any(type(v) is not int or v < 0 or v > selected for v in (successes, unknown)):
        raise ValueError("Invalid evaluation counts")
    if successes + unknown > selected:
        raise ValueError("Successes cannot include unknown-label tasks")
    results = {}
    for kind in ("actual", "scenario"):
        values = [item[f"{kind}_usd"] for item in components]
        for value in values:
            if value is not None and (type(value) not in (float, int) or not math.isfinite(value)):
                raise ValueError("Costs must be finite numbers or unknown")
        total = None if any(v is None for v in values) else sum(Decimal(str(v)) for v in values)
        status = (
            "UNKNOWN_COST"
            if total is None
            else "UNKNOWN_LABELS"
            if unknown
            else "UNDEFINED_ZERO_SUCCESSES"
            if successes == 0
            else "DEFINED"
        )
        results[kind] = {
            "total_usd": None if total is None else float(total),
            "cost_per_success_usd": float(total / successes) if status == "DEFINED" else None,
            "cps_status": status,
            "unknown_components": [
                item["name"] for item in components if item[f"{kind}_usd"] is None
            ],
        }
    return {
        "schema_version": "1.0.0",
        "synthetic": ledger["synthetic"],
        "boundary": ledger["boundary"],
        "allocation_policy": ledger["allocation_policy"],
        "treatment": ledger["treatment"],
        "currency": "USD",
        "selected": selected,
        "known_strict_successes_at_5": successes,
        "unknown_label_tasks": unknown,
        "failed_or_unsuccessful_tasks": selected - successes - unknown,
        "success_denominator_status": "UNKNOWN"
        if unknown
        else "ZERO"
        if successes == 0
        else "KNOWN",
        "actual": results["actual"],
        "scenario": results["scenario"],
        "scope": "File localization only; scenario values are assumptions, not measured savings",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ledger", type=Path, required=True)
    parser.add_argument("--evaluation", type=Path, required=True)
    parser.add_argument(
        "--schema", type=Path, default=Path("schemas/accounting/v1/ledger.schema.json")
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        ledger, evaluation, schema = (
            json.loads(path.read_text()) for path in (args.ledger, args.evaluation, args.schema)
        )
        result = cost_summary(ledger, evaluation, schema)
        result["input_sha256"] = {
            name: digest(path.read_bytes())
            for name, path in (
                ("ledger", args.ledger),
                ("evaluation", args.evaluation),
                ("schema", args.schema),
            )
        }
        write_artifacts(
            args.output,
            {
                "summary.json": encoded(result),
                "ledger.json": args.ledger.read_bytes(),
                "evaluation-summary.json": args.evaluation.read_bytes(),
                "ledger-schema.json": args.schema.read_bytes(),
            },
        )
        print(json.dumps(result, indent=2))
    except (ValueError, KeyError, OSError, jsonschema.ValidationError) as exc:
        parser.exit(2, f"error: {exc}\n")


if __name__ == "__main__":
    main()
