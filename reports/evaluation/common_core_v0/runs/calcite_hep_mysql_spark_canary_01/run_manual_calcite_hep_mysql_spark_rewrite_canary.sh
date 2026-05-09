#!/usr/bin/env bash
set -euo pipefail

discover_repo_root() {
  local start_dir="$1"
  local current="$start_dir"
  while [[ "$current" != "/" ]]; do
    if [[ -d "$current/.git" ]] || \
       [[ -f "$current/reports/curation/common_core_v0_final_denominator.csv" ]]; then
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

RUN_ID="calcite_hep_mysql_spark_canary_01"
METHOD_ID="calcite_hep"
ROUTE_ID="calcite_hep_same_engine_rewrite"
CANARY_DENOMINATOR_ID="calcite_hep_mysql_spark_canary_01"
CLAIM_BOUNDARY="mysql_spark_rewrite_canary_only_not_execution_timing_speedup_or_leaderboard_evidence"

RUN_DIR="$REPO_ROOT/reports/evaluation/common_core_v0/runs/$RUN_ID"
MATRIX_PATH="$RUN_DIR/rewrite_command_matrix.csv"
RUN_RESULTS_PATH="$RUN_DIR/run_results.json"
RUN_EVENT_LONG_PATH="$RUN_DIR/run_event_long.csv"

CALCITE_CHECKOUT_ROOT="${CALCITE_CHECKOUT_ROOT:-$REPO_ROOT/datasets/raw/calcite/calcite}"
CALCITE_WRAPPER_SOURCE="$REPO_ROOT/tools/calcite_hep/CalciteHepRewriteSmoke.java"

mkdir -p "$RUN_DIR"

python - <<'PY' "$REPO_ROOT" "$MATRIX_PATH" "$RUN_RESULTS_PATH" "$RUN_EVENT_LONG_PATH" "$CALCITE_WRAPPER_SOURCE" "$CALCITE_CHECKOUT_ROOT" "$RUN_ID" "$METHOD_ID" "$ROUTE_ID" "$CANARY_DENOMINATOR_ID" "$CLAIM_BOUNDARY"
import csv
import json
import sys
from pathlib import Path

repo_root = Path(sys.argv[1])
matrix_path = Path(sys.argv[2])
run_results_path = Path(sys.argv[3])
run_event_long_path = Path(sys.argv[4])
wrapper_source = Path(sys.argv[5])
calcite_checkout_root = Path(sys.argv[6])
run_id = sys.argv[7]
method_id = sys.argv[8]
route_id = sys.argv[9]
canary_denominator_id = sys.argv[10]
claim_boundary = sys.argv[11]

rows = list(csv.DictReader(matrix_path.open("r", encoding="utf-8")))

event_fields = [
    "run_id",
    "row_key",
    "case_id",
    "pool",
    "engine",
    "method_id",
    "route_id",
    "canary_denominator_id",
    "row_status",
    "claim_boundary",
    "generated_sql_path",
    "log_path",
    "row_metadata_path",
    "failure_category",
    "blocker_reason",
]

missing = []
for row in rows:
    for key in ("source_sql_path", "schema_path", "witness_data_path"):
        p = repo_root / row[key]
        if not p.is_file():
            missing.append(f"{row['row_key']}:{key}:{row[key]}")

wrapper_text = wrapper_source.read_text(encoding="utf-8") if wrapper_source.is_file() else ""
wrapper_uses_postgresql = "PostgresqlSqlDialect" in wrapper_text
wrapper_has_mysql_renderer = "MysqlSqlDialect" in wrapper_text
wrapper_has_spark_renderer = "SparkSqlDialect" in wrapper_text

failure_category = ""
failure_reason = ""
if not wrapper_source.is_file():
    failure_category = "wrapper_source_missing"
    failure_reason = str(wrapper_source)
elif not calcite_checkout_root.is_dir():
    failure_category = "calcite_checkout_missing"
    failure_reason = str(calcite_checkout_root)
elif missing:
    failure_category = "missing_case_artifact"
    failure_reason = "; ".join(missing)
elif wrapper_uses_postgresql and not (wrapper_has_mysql_renderer or wrapper_has_spark_renderer):
    failure_category = "target_engine_dialect_not_implemented"
    failure_reason = (
        "Visible CalciteHepRewriteSmoke.java renders with PostgresqlSqlDialect and "
        "does not expose MysqlSqlDialect or SparkSqlDialect output routing"
    )

write_header = True
with run_event_long_path.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=event_fields)
    writer.writeheader()
    for row in rows:
        row_status = "preflight_blocked" if failure_category else "planned_canary_attempt"
        writer.writerow({
            "run_id": run_id,
            "row_key": row["row_key"],
            "case_id": row["case_id"],
            "pool": row["pool"],
            "engine": row["engine"],
            "method_id": method_id,
            "route_id": route_id,
            "canary_denominator_id": canary_denominator_id,
            "row_status": row_status,
            "claim_boundary": claim_boundary,
            "generated_sql_path": row["expected_generated_sql_path"],
            "log_path": row["expected_log_path"],
            "row_metadata_path": row["expected_row_metadata_path"],
            "failure_category": failure_category,
            "blocker_reason": failure_reason,
        })
        metadata = {
            "run_id": run_id,
            "method_id": method_id,
            "route_id": route_id,
            "canary_denominator_id": canary_denominator_id,
            "claim_boundary": claim_boundary,
            "case_id": row["case_id"],
            "pool": row["pool"],
            "engine": row["engine"],
            "source_sql_path": row["source_sql_path"],
            "schema_path": row["schema_path"],
            "witness_data_path": row["witness_data_path"],
            "witness_data_used_for_rewrite": False,
            "row_status": row_status,
            "failure_category": failure_category,
            "failure_reason": failure_reason,
            "wrapper_source": str(wrapper_source),
            "calcite_checkout_root": str(calcite_checkout_root),
            "wrapper_uses_postgresql_dialect": wrapper_uses_postgresql,
            "wrapper_has_mysql_renderer": wrapper_has_mysql_renderer,
            "wrapper_has_spark_renderer": wrapper_has_spark_renderer,
        }
        out = repo_root / row["expected_row_metadata_path"]
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8")

payload = {
    "run_id": run_id,
    "method_id": method_id,
    "route_id": route_id,
    "canary_denominator_id": canary_denominator_id,
    "claim_boundary": claim_boundary,
    "planned_rows": len(rows),
    "status": "preflight_failed" if failure_category else "preflight_passed_but_row_attempts_not_materialized_in_this_package",
    "status_counts": {
        "preflight_blocked": len(rows) if failure_category else 0,
        "planned_canary_attempt": 0 if failure_category else len(rows),
    },
    "failure_category": failure_category,
    "failure_reason": failure_reason,
    "wrapper_source": str(wrapper_source),
    "calcite_checkout_root": str(calcite_checkout_root),
    "wrapper_uses_postgresql_dialect": wrapper_uses_postgresql,
    "wrapper_has_mysql_renderer": wrapper_has_mysql_renderer,
    "wrapper_has_spark_renderer": wrapper_has_spark_renderer,
    "current_benchmark_metric_evidence": False,
    "notes": [
        "human-run only package",
        "rewrite-only canary",
        "no SQL execution",
        "no timing or speedup evidence",
        "does not overwrite existing Calcite HEP PG evidence",
    ],
}
run_results_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
PY

echo "wrote $RUN_RESULTS_PATH"
