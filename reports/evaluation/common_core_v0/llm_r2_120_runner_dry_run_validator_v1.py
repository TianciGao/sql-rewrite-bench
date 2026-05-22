#!/usr/bin/env python3
import argparse
import csv
import json
import sys
from pathlib import Path


REQUIRED_DEPENDENCIES = {
    "runner",
    "logical_plan_substrate",
    "output_sql_extraction",
    "input_format_contract",
    "per_engine_sql_dialect_support",
    "generated_sql_retention_path",
    "checker_handoff",
    "timing_policy",
    "failure_bucket_policy",
    "reproducibility_contract",
}


def read_csv_rows(path: Path):
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def fail(result, message):
    result["ok"] = False
    result["errors"].append(message)


def main():
    parser = argparse.ArgumentParser(
        description="Static dry-run validator for LLM-R2 runner recovery inputs."
    )
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--candidate-matrix", required=True)
    parser.add_argument("--run-plan", required=True)
    parser.add_argument("--recovery-inventory", required=True)
    args = parser.parse_args()

    result = {
        "ok": True,
        "method_id": "llm_r2",
        "checks": {},
        "errors": [],
    }

    manifest_path = Path(args.manifest)
    candidate_path = Path(args.candidate_matrix)
    run_plan_path = Path(args.run_plan)
    inventory_path = Path(args.recovery_inventory)

    for name, path in {
        "manifest": manifest_path,
        "candidate_matrix": candidate_path,
        "run_plan": run_plan_path,
        "recovery_inventory": inventory_path,
    }.items():
        if not path.exists():
            fail(result, f"missing required file: {name} -> {path}")

    if not result["ok"]:
        print(json.dumps(result, indent=2, sort_keys=True))
        return 1

    manifest_rows = read_csv_rows(manifest_path)
    candidate_rows = read_csv_rows(candidate_path)
    run_plan = json.loads(run_plan_path.read_text())
    inventory = json.loads(inventory_path.read_text())

    result["checks"]["manifest_rows"] = len(manifest_rows)
    result["checks"]["candidate_rows"] = len(candidate_rows)
    result["checks"]["run_plan_planned_rows"] = run_plan.get("planned_rows")
    result["checks"]["run_plan_method_id"] = run_plan.get("method_id")
    result["checks"]["inventory_method_id"] = inventory.get("method_id")

    if len(manifest_rows) != 120:
        fail(result, f"manifest data rows must equal 120, got {len(manifest_rows)}")
    if len(candidate_rows) != 120:
        fail(
            result, f"candidate matrix data rows must equal 120, got {len(candidate_rows)}"
        )

    bad_candidate_method_ids = sorted(
        {row.get("method_id") for row in candidate_rows if row.get("method_id") != "llm_r2"}
    )
    if bad_candidate_method_ids:
        fail(
            result,
            "candidate matrix contains non-llm_r2 method_id values: "
            + ",".join(bad_candidate_method_ids),
        )

    if run_plan.get("planned_rows") != 120:
        fail(
            result,
            f"run plan planned_rows must equal 120, got {run_plan.get('planned_rows')}",
        )
    if run_plan.get("method_id") != "llm_r2":
        fail(result, f"run plan method_id must equal llm_r2, got {run_plan.get('method_id')}")

    if inventory.get("method_id") != "llm_r2":
        fail(
            result,
            f"recovery inventory method_id must equal llm_r2, got {inventory.get('method_id')}",
        )

    deps = inventory.get("required_dependencies", [])
    dep_names = {d.get("dependency") for d in deps if isinstance(d, dict)}
    result["checks"]["inventory_dependency_keys"] = sorted(dep_names)
    missing = sorted(REQUIRED_DEPENDENCIES - dep_names)
    if missing:
        fail(result, "recovery inventory missing dependency keys: " + ",".join(missing))

    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
