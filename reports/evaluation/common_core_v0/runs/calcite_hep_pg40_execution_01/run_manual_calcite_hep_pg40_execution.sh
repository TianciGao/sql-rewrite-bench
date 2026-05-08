#!/usr/bin/env bash
set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../../../../.." && pwd)"
RUN_DIR="${SCRIPT_DIR}"
LOG_DIR="${RUN_DIR}/logs"
WORKSPACE_DIR="${RUN_DIR}/workspaces"
MATRIX_CSV="${RUN_DIR}/execution_command_matrix.csv"
RUN_RESULTS_JSON="${RUN_DIR}/run_results.json"
RECORDS_JSONL="${RUN_DIR}/records.tmp.jsonl"

if [[ "$(pwd)" != "${REPO_ROOT}" ]]; then
  echo "This script must be run from the repository root: ${REPO_ROOT}" >&2
  exit 1
fi

mkdir -p "${LOG_DIR}" "${WORKSPACE_DIR}"

echo "Human-run only."
echo "Codex must not execute this script."
echo "This package produces execution and validity evidence only."
echo "It does not compute timing, speedup, or leaderboard artifacts."

source "${REPO_ROOT}/scripts/env_postgres.sh"

python - "$REPO_ROOT" "$RUN_DIR" "$MATRIX_CSV" "$RUN_RESULTS_JSON" "$RECORDS_JSONL" <<'PY'
from __future__ import annotations

import csv
import json
import os
import re
import subprocess
import sys
import traceback
from collections import Counter
from pathlib import Path
from typing import Any

REPO_ROOT = Path(sys.argv[1])
RUN_DIR = Path(sys.argv[2])
MATRIX_CSV = Path(sys.argv[3])
RUN_RESULTS_JSON = Path(sys.argv[4])
RECORDS_JSONL = Path(sys.argv[5])

DENOMINATOR_ID = "common_core_v0_40_pg40"
METHOD_ID = "calcite_hep"
ROUTE_ID = "calcite_hep_pg_rewrite"
RUN_ID = "calcite_hep_pg40_execution_01"


def read_rows() -> list[dict[str, str]]:
    with MATRIX_CSV.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=True) + "\n")


def git_commit() -> str:
    try:
        proc = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=REPO_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        return proc.stdout.strip()
    except Exception:
        return ""


def normalize_query_text(text: str) -> str:
    return text.strip().rstrip(";").strip()


def compare_tsv_outputs(source_path: Path, generated_path: Path) -> dict[str, Any]:
    source_text = source_path.read_text(encoding="utf-8")
    generated_text = generated_path.read_text(encoding="utf-8")
    exact_match = source_text == generated_text
    source_lines = sorted(line.rstrip("\n") for line in source_text.splitlines())
    generated_lines = sorted(line.rstrip("\n") for line in generated_text.splitlines())
    sorted_match = source_lines == generated_lines
    if exact_match:
        status = "match_exact"
    elif sorted_match:
        status = "match_after_sort_normalization"
    else:
        status = "mismatch"
    return {
        "exact_match": exact_match,
        "sorted_match": sorted_match,
        "consistency_check_status": status,
    }


def log_path_from_row(row: dict[str, str], kind: str) -> Path:
    key = f"expected_log_{kind}"
    value = row.get(key, "").strip()
    if value:
        return REPO_ROOT / value
    fallback = RUN_DIR / "logs" / f"{row['case_id']}_{row['engine']}_{row['route_id']}.{kind}.log"
    return fallback


def run_pg_row(row: dict[str, str]) -> dict[str, Any]:
    stdout_log = log_path_from_row(row, "stdout")
    stderr_log = log_path_from_row(row, "stderr")
    source_out = REPO_ROOT / row["expected_source_output_path"]
    generated_out = REPO_ROOT / row["expected_generated_output_path"]
    result_check = REPO_ROOT / row["expected_result_check_path"]
    for path in [stdout_log.parent, stderr_log.parent, source_out.parent, generated_out.parent, result_check.parent]:
        path.mkdir(parents=True, exist_ok=True)

    schema_name = re.sub(r"[^a-z0-9_]", "_", f"ccv0_calcite_hep_{row['case_id'].lower()}")[:55]
    psql_base = ["psql", "-v", "ON_ERROR_STOP=1", "-X", "-q"]

    with stdout_log.open("w", encoding="utf-8") as stdout_handle, stderr_log.open("w", encoding="utf-8") as stderr_handle:
        try:
            stdout_handle.write(f"row={row['case_id']} engine={row['engine']} route={row['route_id']}\n")
            subprocess.run(
                psql_base + ["-c", f"DROP SCHEMA IF EXISTS {schema_name} CASCADE; CREATE SCHEMA {schema_name};"],
                cwd=REPO_ROOT,
                check=True,
                stdout=stdout_handle,
                stderr=stderr_handle,
                text=True,
            )
            for sql_path in [row["schema_path"], row["witness_data_path"]]:
                subprocess.run(
                    psql_base + ["-c", f"SET search_path TO {schema_name};", "-f", str(REPO_ROOT / sql_path)],
                    cwd=REPO_ROOT,
                    check=True,
                    stdout=stdout_handle,
                    stderr=stderr_handle,
                    text=True,
                )

            source_query = normalize_query_text((REPO_ROOT / row["source_sql_path"]).read_text(encoding="utf-8"))
            generated_query = normalize_query_text((REPO_ROOT / row["generated_sql_path"]).read_text(encoding="utf-8"))
            source_copy_sql = f"COPY ({source_query}) TO STDOUT WITH (FORMAT CSV, DELIMITER E'\\t', NULL 'NULL');"
            generated_copy_sql = f"COPY ({generated_query}) TO STDOUT WITH (FORMAT CSV, DELIMITER E'\\t', NULL 'NULL');"

            with source_out.open("w", encoding="utf-8") as source_handle:
                subprocess.run(
                    psql_base + ["-c", f"SET search_path TO {schema_name};", "-c", source_copy_sql],
                    cwd=REPO_ROOT,
                    check=True,
                    stdout=source_handle,
                    stderr=stderr_handle,
                    text=True,
                )
            with generated_out.open("w", encoding="utf-8") as generated_handle:
                subprocess.run(
                    psql_base + ["-c", f"SET search_path TO {schema_name};", "-c", generated_copy_sql],
                    cwd=REPO_ROOT,
                    check=True,
                    stdout=generated_handle,
                    stderr=stderr_handle,
                    text=True,
                )

            compare = compare_tsv_outputs(source_out, generated_out)
            payload = {
                "execution_status_observed": "executed",
                "result_check_path": row["expected_result_check_path"],
                "source_output_path": row["expected_source_output_path"],
                "generated_output_path": row["expected_generated_output_path"],
                **compare,
            }
            write_json(result_check, payload)
            return payload
        except Exception as exc:
            traceback.print_exc(file=stderr_handle)
            payload = {
                "execution_status_observed": "execution_failed",
                "consistency_check_status": "not_checked_execution_failed",
                "error_type": type(exc).__name__,
                "error_message": str(exc),
                "result_check_path": row["expected_result_check_path"],
                "source_output_path": row["expected_source_output_path"],
                "generated_output_path": row["expected_generated_output_path"],
            }
            write_json(result_check, payload)
            return payload
        finally:
            subprocess.run(
                ["psql", "-v", "ON_ERROR_STOP=0", "-X", "-q", "-c", f"DROP SCHEMA IF EXISTS {schema_name} CASCADE;"],
                cwd=REPO_ROOT,
                stdout=stdout_handle,
                stderr=stderr_handle,
                text=True,
            )


matrix_rows = read_rows()
records: list[dict[str, Any]] = []

for row in matrix_rows:
    base = {
        "case_id": row["case_id"],
        "pool": row["pool"],
        "engine": row["engine"],
        "route_id": row["route_id"],
        "method_id": METHOD_ID,
        "denominator_id": DENOMINATOR_ID,
        "generation_status": row["generation_status"],
        "execution_status_planned": row["execution_status"],
        "control_source_artifact": row["control_source_artifact"],
        "caveat": row["caveat"],
    }
    if row["execution_status"] != "ready_to_execute":
        result_check = {
            "execution_status_observed": "not_executed_generation_failed",
            "consistency_check_status": "not_checked_generation_failed",
            "exclusion_reason": row["exclusion_reason"],
            "result_check_path": row["expected_result_check_path"],
            "source_output_path": row["expected_source_output_path"],
            "generated_output_path": row["expected_generated_output_path"],
        }
        write_json(REPO_ROOT / row["expected_result_check_path"], result_check)
        records.append({**base, **result_check})
        continue
    observed = run_pg_row(row)
    records.append({**base, **observed})

counts_exec = Counter(r["execution_status_observed"] for r in records)
counts_consistency = Counter(r["consistency_check_status"] for r in records)
summary = {
    "run_id": RUN_ID,
    "denominator_id": DENOMINATOR_ID,
    "method_id": METHOD_ID,
    "route_id": ROUTE_ID,
    "planned_rows": len(matrix_rows),
    "rows_ready_to_execute": sum(1 for r in matrix_rows if r["execution_status"] == "ready_to_execute"),
    "rows_not_executed_generation_failed": sum(1 for r in matrix_rows if r["execution_status"] == "not_executed_generation_failed"),
    "git_commit": git_commit(),
    "counts_by_execution_status_observed": dict(counts_exec),
    "counts_by_consistency_check_status": dict(counts_consistency),
    "records": records,
}
write_json(RUN_RESULTS_JSON, summary)
write_jsonl(RECORDS_JSONL, records)
print(f"wrote {RUN_RESULTS_JSON}")
PY
