#!/usr/bin/env bash
set -euo pipefail

discover_repo_root() {
  local start_dir="$1"
  local current="$start_dir"
  while [[ "$current" != "/" ]]; do
    if [[ -d "$current/.git" ]] || [[ -f "$current/reports/curation/common_core_v0_final_denominator.csv" ]]; then
      printf '%s\n' "$current"
      return 0
    fi
    current="$(dirname "$current")"
  done
  return 1
}

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(discover_repo_root "$SCRIPT_DIR")"
if [[ -z "${REPO_ROOT:-}" ]]; then
  echo "unable to discover repo root" >&2
  exit 1
fi

if [[ "$(pwd)" != "$REPO_ROOT" ]]; then
  echo "run from repo root: $REPO_ROOT" >&2
  exit 1
fi

RUN_ID="calcite_hep_120_recovery_autopilot_01"
METHOD_ID="calcite_hep"
ROUTE_ID="calcite_hep_same_engine_rewrite"
DENOMINATOR_ID="common_core_v0_40_same_engine_120"
CLAIM_BOUNDARY="calcite_hep_120_recovery_autopilot_only_not_timing_speedup_or_leaderboard_evidence"

RUN_DIR="$REPO_ROOT/reports/evaluation/common_core_v0/runs/$RUN_ID"
MATRIX_PATH="$RUN_DIR/recovery_command_matrix.csv"
RUN_RESULTS_PATH="$RUN_DIR/run_results.json"
RUN_EVENT_LONG_PATH="$RUN_DIR/run_event_long.csv"

mkdir -p "$RUN_DIR"

echo "Human-run only."
echo "Codex must not execute this script."
echo "This package produces recovery-autopilot validity evidence only."
echo "No timing."
echo "No speedup."
echo "No leaderboard."
echo "No full 120-row comparable claim."

python - <<'PY' "$MATRIX_PATH" "$RUN_RESULTS_PATH" "$RUN_EVENT_LONG_PATH" "$RUN_ID" "$METHOD_ID" "$ROUTE_ID" "$DENOMINATOR_ID" "$CLAIM_BOUNDARY"
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

matrix_path = Path(sys.argv[1])
run_results_path = Path(sys.argv[2])
run_event_long_path = Path(sys.argv[3])
run_id = sys.argv[4]
method_id = sys.argv[5]
route_id = sys.argv[6]
denominator_id = sys.argv[7]
claim_boundary = sys.argv[8]

with matrix_path.open(newline="", encoding="utf-8") as handle:
    rows = list(csv.DictReader(handle))

event_fieldnames = [
    "run_id",
    "row_key",
    "case_id",
    "pool",
    "engine",
    "method_id",
    "route_id",
    "denominator_id",
    "previous_status",
    "recoverability_bucket",
    "planned_action",
    "execution_status",
    "consistency_status",
    "recovered_exact",
    "failure_category",
    "blocker_reason",
    "claim_boundary",
]

with run_event_long_path.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=event_fieldnames)
    writer.writeheader()
    for row in rows:
        writer.writerow({
            "run_id": run_id,
            "row_key": row.get("row_key", ""),
            "case_id": row.get("case_id", ""),
            "pool": row.get("pool", ""),
            "engine": row.get("engine", ""),
            "method_id": method_id,
            "route_id": route_id,
            "denominator_id": denominator_id,
            "previous_status": row.get("previous_status", ""),
            "recoverability_bucket": row.get("recoverability_bucket", ""),
            "planned_action": row.get("planned_action", ""),
            "execution_status": "not_planned_no_safe_candidate",
            "consistency_status": "not_applicable",
            "recovered_exact": "false",
            "failure_category": "no_safe_retained_evidence_candidate",
            "blocker_reason": "remaining_rows_are_semantic_output_shape_or_methodology_boundary",
            "claim_boundary": claim_boundary,
        })

payload = {
    "run_id": run_id,
    "method_id": method_id,
    "route_id": route_id,
    "denominator_id": denominator_id,
    "previous_fail_closed_exact_ledger": "90/120",
    "planned_rows": len(rows),
    "recovered_exact_count": 0,
    "new_fail_closed_exact_ledger": "90/120",
    "maximum_possible_ledger_after_this_autopilot": "90/120",
    "current_benchmark_metric_evidence": False,
    "timing_denominator_id": "NA_not_computed",
    "leaderboard_comparable": "no",
    "claim_boundary": claim_boundary,
    "autopilot_decision": "frontier_closed_no_safe_rows",
    "blocked_row_classes": [
        "semantic_or_output_shape_mismatch",
        "methodology_boundary_do_not_recover",
    ],
}
run_results_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
PY
