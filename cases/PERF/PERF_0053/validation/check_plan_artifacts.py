#!/usr/bin/env python3
import json
import sys
from pathlib import Path

CASE_ID = "PERF_0053"
EXPECTED_PLAN_FILES = [
    "runs/pg/plans/source.json",
    "runs/mysql/plans/rewrite_pos_01.json",
    "runs/mysql/plans/rewrite_neg_01.json",
    "runs/spark/plans/rewrite_pos_01.txt",
    "runs/spark/plans/rewrite_neg_01.txt",
]


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: check_plan_artifacts.py output.json", file=sys.stderr)
        return 2

    output_path = Path(sys.argv[1])
    case_root = output_path.parent.parent

    existing = []
    missing = []
    for rel_path in EXPECTED_PLAN_FILES:
        if (case_root / rel_path).exists():
            existing.append(rel_path)
        else:
            missing.append(rel_path)

    payload = {
        "case_id": CASE_ID,
        "status": "complete" if not missing else "incomplete",
        "draft_only": True,
        "expected_plan_files": EXPECTED_PLAN_FILES,
        "existing_plan_files": existing,
        "missing_plan_files": missing,
        "notes": [
            "Plan-artifact presence checking only.",
            "No plan semantics review is claimed.",
            "No admission, formal review completion, or release-grade claim is implied.",
        ],
    }

    output_path.write_text(json.dumps(payload, indent=2) + "\n")
    return 0 if not missing else 1


if __name__ == "__main__":
    raise SystemExit(main())
