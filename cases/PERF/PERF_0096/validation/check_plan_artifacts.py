#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path


ENGINES = ["pg", "mysql", "spark"]
EXPECTED_PLAN_FILES = [
    "runs/pg/plans/source.json",
    "runs/pg/plans/rewrite_pos_01.json",
    "runs/pg/plans/rewrite_neg_01.json",
    "runs/pg/plans/plan_check.json",
    "runs/mysql/plans/source.json",
    "runs/mysql/plans/rewrite_pos_01.json",
    "runs/mysql/plans/rewrite_neg_01.json",
    "runs/mysql/plans/plan_check.json",
    "runs/spark/plans/source.txt",
    "runs/spark/plans/rewrite_pos_01.txt",
    "runs/spark/plans/rewrite_neg_01.txt",
    "runs/spark/plans/plan_check.json",
]


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: check_plan_artifacts.py <output_plan_check_json>", file=sys.stderr)
        return 2

    case_dir = Path(__file__).resolve().parent.parent
    case_id = case_dir.name
    output_path = Path(sys.argv[1]).resolve()

    existing = []
    missing = []
    for rel_path in EXPECTED_PLAN_FILES:
        if (case_dir / rel_path).exists():
            existing.append(rel_path)
        else:
            missing.append(rel_path)

    status = "complete" if not missing else "incomplete"
    payload = {
        "case_id": case_id,
        "validation_model": "engine_local_plan_artifacts",
        "engines": ENGINES,
        "status": status,
        "draft_only": True,
        "expected_plan_files": EXPECTED_PLAN_FILES,
        "existing_plan_files": existing,
        "missing_plan_files": missing,
        "notes": [
            "Existing per-engine plan artifacts checked only.",
            "Plan-artifact presence checking only.",
            "No plan semantics review is claimed.",
            "Engine-local plan evidence model; not a cross-dialect source-reference plan claim.",
            "No registry validation, admission, common-core promotion, formal-review completion, or release-grade claim is implied.",
        ],
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return 0 if status == "complete" else 1


if __name__ == "__main__":
    raise SystemExit(main())
