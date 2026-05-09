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

RUN_ID="calcite_hep_120_recovery_round3b_mysql_setup_canary_02_01"
METHOD_ID="calcite_hep"
ROUTE_ID="calcite_hep_same_engine_rewrite"
DENOMINATOR_ID="common_core_v0_40_same_engine_120"
CLAIM_BOUNDARY="calcite_hep_120_recovery_round3b_mysql_setup_canary_only_not_timing_speedup_or_leaderboard_evidence"

RUN_DIR="$REPO_ROOT/reports/evaluation/common_core_v0/runs/$RUN_ID"
MATRIX_PATH="$RUN_DIR/recovery_command_matrix.csv"
RUN_RESULTS_PATH="$RUN_DIR/run_results.json"
RUN_EVENT_LONG_PATH="$RUN_DIR/run_event_long.csv"

mkdir -p "$RUN_DIR"

echo "Human-run only."
echo "Codex must not execute this script."
echo "This package produces recovery-canary validity evidence only."
echo "No timing."
echo "No speedup."
echo "No leaderboard."
echo "No full 120-row comparable claim."

source "$REPO_ROOT/scripts/env_mysql.sh"

python - <<'PY' "$REPO_ROOT" "$MATRIX_PATH" "$RUN_RESULTS_PATH" "$RUN_EVENT_LONG_PATH" "$RUN_ID" "$METHOD_ID" "$ROUTE_ID" "$DENOMINATOR_ID" "$CLAIM_BOUNDARY"
from __future__ import annotations

import csv
import json
import os
import re
import shutil
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

REPO_ROOT = Path(sys.argv[1])
MATRIX_PATH = Path(sys.argv[2])
RUN_RESULTS_PATH = Path(sys.argv[3])
RUN_EVENT_LONG_PATH = Path(sys.argv[4])
RUN_ID = sys.argv[5]
METHOD_ID = sys.argv[6]
ROUTE_ID = sys.argv[7]
DENOMINATOR_ID = sys.argv[8]
CLAIM_BOUNDARY = sys.argv[9]

PREVIOUS_LEDGER_NUM = 84
PREVIOUS_LEDGER_DEN = 120
MAX_LEDGER_AFTER = 86


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def normalize_query_text(text: str) -> str:
    return text.strip().rstrip(";").strip()


def compare_tsv_outputs(source_path: Path, generated_path: Path) -> dict[str, Any]:
    source_text = source_path.read_text(encoding="utf-8")
    generated_text = generated_path.read_text(encoding="utf-8")
    exact_match = source_text == generated_text
    return {
        "exact_match": exact_match,
        "consistency_status": "match_exact" if exact_match else "mismatch",
    }


def mysql_args() -> list[str]:
    args = ["mysql"]
    if os.environ.get("MYSQL_HOST"):
        args.extend(["--host", os.environ["MYSQL_HOST"]])
    if os.environ.get("MYSQL_PORT"):
        args.extend(["--port", os.environ["MYSQL_PORT"]])
    if os.environ.get("MYSQL_USER"):
        args.extend(["--user", os.environ["MYSQL_USER"]])
    if os.environ.get("MYSQL_PASSWORD"):
        args.append(f"--password={os.environ['MYSQL_PASSWORD']}")
    return args


def extract_table_names(ddl_text: str) -> list[str]:
    pattern = re.compile(
        r"CREATE\\s+TABLE\\s+(?:IF\\s+NOT\\s+EXISTS\\s+)?(?:`([^`]+)`|\\\"([^\\\"]+)\\\"|([A-Za-z_][A-Za-z0-9_]*))",
        re.IGNORECASE,
    )
    table_names: list[str] = []
    for match in pattern.finditer(ddl_text):
        table_name = match.group(1) or match.group(2) or match.group(3)
        if table_name and table_name not in table_names:
            table_names.append(table_name)
    return table_names


def read_rows() -> list[dict[str, str]]:
    with MATRIX_PATH.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def copy_inputs(workspace: Path, row: dict[str, str]) -> dict[str, Path]:
    workspace.mkdir(parents=True, exist_ok=True)
    copied = {
        "schema": workspace / "ddl_mysql.sql",
        "witness": workspace / "mysql_witness_data.sql",
        "source": workspace / "source.sql",
        "generated": workspace / "generated.sql",
    }
    shutil.copyfile(REPO_ROOT / row["schema_path"], copied["schema"])
    shutil.copyfile(REPO_ROOT / row["witness_data_path"], copied["witness"])
    shutil.copyfile(REPO_ROOT / row["source_sql_path"], copied["source"])
    shutil.copyfile(REPO_ROOT / row["retained_generated_sql_path"], copied["generated"])
    return copied


def run_mysql_execution(row: dict[str, str]) -> dict[str, Any]:
    workspace = (REPO_ROOT / row["expected_result_check_path"]).parent
    copied = copy_inputs(workspace, row)
    source_out = REPO_ROOT / row["expected_source_tsv_path"]
    generated_out = REPO_ROOT / row["expected_generated_tsv_path"]
    result_check = REPO_ROOT / row["expected_result_check_path"]
    source_stdout = REPO_ROOT / row["expected_source_stdout_log"]
    source_stderr = REPO_ROOT / row["expected_source_stderr_log"]
    generated_stdout = REPO_ROOT / row["expected_generated_stdout_log"]
    generated_stderr = REPO_ROOT / row["expected_generated_stderr_log"]
    row_metadata_path = REPO_ROOT / row["expected_row_metadata_path"]

    for path in [source_out.parent, source_stdout.parent, generated_stdout.parent, row_metadata_path.parent]:
        path.mkdir(parents=True, exist_ok=True)

    db_name = os.environ.get("MYSQL_DATABASE", "")
    if not db_name:
        payload = {
            "execution_status": "setup_failed",
            "exact_match": False,
            "consistency_status": "not_applicable",
            "failure_category": "missing_mysql_database_env",
            "blocker_reason": "MYSQL_DATABASE is not set",
        }
        write_json(result_check, payload)
        write_json(row_metadata_path, {"row_key": row["row_key"], **payload})
        return payload

    ddl_text = copied["schema"].read_text(encoding="utf-8")
    table_names = extract_table_names(ddl_text)
    drop_sql = ""
    if table_names:
      drop_sql = "DROP TABLE IF EXISTS " + ", ".join(f"`{name}`" for name in table_names) + ";"

    def mysql_exec(sql: str, stdout_path: Path, stderr_path: Path, batch_output: bool = False) -> None:
        cmd = mysql_args() + [db_name]
        if batch_output:
            cmd.extend(["--batch", "--raw", "--skip-column-names"])
        cmd.extend(["-e", sql])
        with stdout_path.open("w", encoding="utf-8") as stdout_handle, stderr_path.open("w", encoding="utf-8") as stderr_handle:
            subprocess.run(cmd, cwd=REPO_ROOT, check=True, stdout=stdout_handle, stderr=stderr_handle, text=True)

    try:
        if drop_sql:
            mysql_exec(drop_sql, source_stdout, source_stderr)
        mysql_exec(f"source {copied['schema']};", source_stdout, source_stderr)
        mysql_exec(f"source {copied['witness']};", source_stdout, source_stderr)
        mysql_exec(normalize_query_text(copied["source"].read_text(encoding="utf-8")), source_out, source_stderr, batch_output=True)
        mysql_exec(normalize_query_text(copied["generated"].read_text(encoding="utf-8")), generated_out, generated_stderr, batch_output=True)
        compare = compare_tsv_outputs(source_out, generated_out)
        payload = {"execution_status": "executed", **compare}
    except subprocess.CalledProcessError as exc:
        payload = {
            "execution_status": "generated_execution_failed",
            "exact_match": False,
            "consistency_status": "not_applicable",
            "failure_category": "execution_failed",
            "blocker_reason": str(exc),
        }
    finally:
        if drop_sql:
            try:
                mysql_exec(drop_sql, generated_stdout, generated_stderr)
            except Exception:
                pass

    write_json(result_check, payload)
    write_json(
        row_metadata_path,
        {
            "run_id": RUN_ID,
            "row_key": row["row_key"],
            "case_id": row["case_id"],
            "engine": row["engine"],
            "previous_ledger": row["previous_ledger"],
            "attempted_recovery_family": row["attempted_recovery_family"],
            "retained_generated_sql_path": row["retained_generated_sql_path"],
            "mysql_database_used": db_name,
            "cleanup_table_names": table_names,
            **payload,
        },
    )
    return payload


rows = read_rows()
records: list[dict[str, Any]] = []
for row in rows:
    execution = run_mysql_execution(row)
    record = {
        "row_key": row["row_key"],
        "case_id": row["case_id"],
        "pool": row["pool"],
        "engine": row["engine"],
        "previous_ledger": row["previous_ledger"],
        "previous_status": row["previous_status"],
        "attempted_recovery_family": row["attempted_recovery_family"],
        "execution_status": execution["execution_status"],
        "exact_match": execution["exact_match"],
        "consistency_status": execution["consistency_status"],
        "recovered_exact": execution["execution_status"] == "executed" and execution["consistency_status"] == "match_exact",
        "failure_category": execution.get("failure_category", ""),
        "blocker_reason": execution.get("blocker_reason", ""),
        "source_sql_path": row["source_sql_path"],
        "schema_path": row["schema_path"],
        "witness_data_path": row["witness_data_path"],
        "generated_sql_path": row["retained_generated_sql_path"],
        "result_check_path": row["expected_result_check_path"],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    records.append(record)

with RUN_EVENT_LONG_PATH.open("w", newline="", encoding="utf-8") as handle:
    fieldnames = [
        "row_key","case_id","pool","engine","previous_ledger","previous_status",
        "attempted_recovery_family","execution_status","exact_match",
        "consistency_status","recovered_exact","failure_category","blocker_reason",
        "source_sql_path","schema_path","witness_data_path","generated_sql_path",
        "result_check_path","claim_boundary"
    ]
    writer = csv.DictWriter(handle, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(records)

recovered_exact_count = sum(1 for record in records if record["recovered_exact"])
counts_by_execution_status = Counter(record["execution_status"] for record in records)
counts_by_consistency_status = Counter(record["consistency_status"] for record in records)
counts_by_engine: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
for record in records:
    counts_by_engine[record["engine"]][record["execution_status"]] += 1

summary = {
    "run_id": RUN_ID,
    "method_id": METHOD_ID,
    "route_id": ROUTE_ID,
    "denominator_id": DENOMINATOR_ID,
    "previous_fail_closed_exact_ledger": f"{PREVIOUS_LEDGER_NUM}/{PREVIOUS_LEDGER_DEN}",
    "planned_rows": len(rows),
    "recovered_exact_count": recovered_exact_count,
    "new_fail_closed_exact_ledger": f"{PREVIOUS_LEDGER_NUM + recovered_exact_count}/{PREVIOUS_LEDGER_DEN}",
    "maximum_possible_ledger_after_this_canary": f"{MAX_LEDGER_AFTER}/{PREVIOUS_LEDGER_DEN}",
    "counts_by_engine": counts_by_engine,
    "counts_by_execution_status": counts_by_execution_status,
    "counts_by_consistency_status": counts_by_consistency_status,
    "current_benchmark_metric_evidence": False,
    "timing_denominator_id": "NA_not_computed",
    "leaderboard_comparable": "no",
    "claim_boundary": CLAIM_BOUNDARY,
    "records": records,
}
write_json(RUN_RESULTS_PATH, summary)
PY
