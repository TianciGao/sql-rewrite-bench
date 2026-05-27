#!/usr/bin/env bash
set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

discover_repo_root() {
  local current="$1"
  while [[ "$current" != "/" ]]; do
    if [[ -d "$current/.git" ]] || [[ -f "$current/reports/curation/common_core_v0_final_denominator.csv" ]] || [[ -f "$current/reports/evaluation/common_core_v0/r_bot_formal_protocol/r_bot_common_core_v0_40_same_engine_candidate_matrix.csv" ]]; then
      printf '%s\n' "$current"
      return 0
    fi
    current="$(dirname -- "$current")"
  done
  return 1
}

REPO_ROOT="$(discover_repo_root "$SCRIPT_DIR")" || {
  echo "failed to discover repo root from package root: $SCRIPT_DIR" >&2
  exit 1
}
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
echo "This package produces PostgreSQL execution and validity evidence only for the generated PG15 subset from the PG40 expansion run."
echo "It does not compute timing, speedup, or leaderboard artifacts."

source "${REPO_ROOT}/scripts/env_postgres.sh"

python - "$REPO_ROOT" "$RUN_DIR" "$MATRIX_CSV" "$RUN_RESULTS_JSON" "$RECORDS_JSONL" <<'PY'
from __future__ import annotations

import csv
import json
import re
import shutil
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

RUN_ID = "r_bot_pg15_execution_expansion_02"
METHOD_ID = "r_bot"
ROUTE_ID = "r_bot_same_engine_rewrite"
GENERATION_DENOMINATOR_ID = "common_core_v0_40_pg40"
EXECUTION_DENOMINATOR_ID = "generated_pg15_from_pg40_expansion_only"
CLAIM_BOUNDARY = "formal_generated_pg15_from_pg40_expansion_execution_validity_only_not_timing_speedup_or_leaderboard_evidence"
CURRENT_BENCHMARK_METRIC_EVIDENCE = False
SOURCE_GENERATION_RUN_ID = "r_bot_pg40_generation_expansion_02"
SOURCE_GENERATION_RUN_RESULTS = (
    "reports/evaluation/common_core_v0/runs/"
    "r_bot_pg40_generation_expansion_02/run_results.json"
)


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


def exact_compare_tsv_outputs(source_path: Path, generated_path: Path) -> dict[str, Any]:
    source_text = source_path.read_text(encoding="utf-8")
    generated_text = generated_path.read_text(encoding="utf-8")
    exact_match = source_text == generated_text
    return {
        "exact_match": exact_match,
        "consistency_check_status": "match_exact" if exact_match else "mismatch",
    }


def run_command(command: list[str], stdout_path: Path, stderr_path: Path) -> int:
    stdout_path.parent.mkdir(parents=True, exist_ok=True)
    stderr_path.parent.mkdir(parents=True, exist_ok=True)
    with stdout_path.open("w", encoding="utf-8") as stdout_handle, stderr_path.open("w", encoding="utf-8") as stderr_handle:
        proc = subprocess.run(
            command,
            cwd=REPO_ROOT,
            stdout=stdout_handle,
            stderr=stderr_handle,
            text=True,
        )
    return proc.returncode


def run_psql_capture(command: list[str], stdout_handle: Any, stderr_handle: Any) -> None:
    subprocess.run(
        command,
        cwd=REPO_ROOT,
        check=True,
        stdout=stdout_handle,
        stderr=stderr_handle,
        text=True,
    )


def run_pg_row(row: dict[str, str]) -> dict[str, Any]:
    stdout_log = REPO_ROOT / row["expected_stdout_log_path"]
    stderr_log = REPO_ROOT / row["expected_stderr_log_path"]
    source_out = REPO_ROOT / row["expected_source_output_path"]
    generated_out = REPO_ROOT / row["expected_generated_output_path"]
    result_check = REPO_ROOT / row["expected_result_check_path"]
    workspace = result_check.parent
    workspace.mkdir(parents=True, exist_ok=True)
    stdout_log.parent.mkdir(parents=True, exist_ok=True)
    stderr_log.parent.mkdir(parents=True, exist_ok=True)

    source_sql_path = REPO_ROOT / row["source_sql_path"]
    generated_sql_path = REPO_ROOT / row["generated_sql_path"]
    schema_path = REPO_ROOT / row["schema_path"]
    witness_path = REPO_ROOT / row["witness_data_path"]

    shutil.copy2(source_sql_path, workspace / "source.sql")
    shutil.copy2(generated_sql_path, workspace / "generated.sql")
    shutil.copy2(schema_path, workspace / "ddl_pg.sql")
    shutil.copy2(witness_path, workspace / "pg_witness_data.sql")

    schema_name = re.sub(r"[^a-z0-9_]", "_", f"rbot_pg15_exec_{row['case_id'].lower()}")[:55]
    psql_base = ["psql", "-v", "ON_ERROR_STOP=1", "-X", "-q"]

    with stdout_log.open("w", encoding="utf-8") as stdout_handle, stderr_log.open("w", encoding="utf-8") as stderr_handle:
        try:
            stdout_handle.write(
                f"row={row['case_id']} engine={row['engine']} route={row['route_id']} "
                f"claim_boundary={CLAIM_BOUNDARY}\n"
            )
            run_psql_capture(
                psql_base + ["-c", f"DROP SCHEMA IF EXISTS {schema_name} CASCADE; CREATE SCHEMA {schema_name};"],
                stdout_handle,
                stderr_handle,
            )
            for sql_path in [schema_path, witness_path]:
                run_psql_capture(
                    psql_base + ["-c", f"SET search_path TO {schema_name};", "-f", str(sql_path)],
                    stdout_handle,
                    stderr_handle,
                )

            source_query = normalize_query_text(source_sql_path.read_text(encoding="utf-8"))
            generated_query = normalize_query_text(generated_sql_path.read_text(encoding="utf-8"))
            source_copy_sql = f"COPY ({source_query}) TO STDOUT WITH (FORMAT CSV, DELIMITER E'\\t', NULL 'NULL');"
            generated_copy_sql = f"COPY ({generated_query}) TO STDOUT WITH (FORMAT CSV, DELIMITER E'\\t', NULL 'NULL');"

            with source_out.open("w", encoding="utf-8") as source_handle:
                run_psql_capture(
                    psql_base + ["-c", f"SET search_path TO {schema_name};", "-c", source_copy_sql],
                    source_handle,
                    stderr_handle,
                )
            with generated_out.open("w", encoding="utf-8") as generated_handle:
                run_psql_capture(
                    psql_base + ["-c", f"SET search_path TO {schema_name};", "-c", generated_copy_sql],
                    generated_handle,
                    stderr_handle,
                )

            compare = exact_compare_tsv_outputs(source_out, generated_out)
            payload = {
                "execution_status_observed": "executed",
                "result_check_path": row["expected_result_check_path"],
                "source_output_path": row["expected_source_output_path"],
                "generated_output_path": row["expected_generated_output_path"],
                "claim_boundary": CLAIM_BOUNDARY,
                "current_benchmark_metric_evidence": CURRENT_BENCHMARK_METRIC_EVIDENCE,
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
                "claim_boundary": CLAIM_BOUNDARY,
                "current_benchmark_metric_evidence": CURRENT_BENCHMARK_METRIC_EVIDENCE,
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

pg_check_stdout = RUN_DIR / "logs" / "pg_check.stdout.log"
pg_check_stderr = RUN_DIR / "logs" / "pg_check.stderr.log"
pg_check_exit_code = run_command(
    ["python", "-m", "scripts.cli", "pg-check"],
    pg_check_stdout,
    pg_check_stderr,
)

records.append(
    {
        "row_key": "pg_check",
        "record_kind": "preflight",
        "execution_status_observed": "executed" if pg_check_exit_code == 0 else "execution_failed",
        "consistency_check_status": "not_applicable",
        "command": "python -m scripts.cli pg-check",
        "exit_code": pg_check_exit_code,
        "stdout_log": str(pg_check_stdout.relative_to(REPO_ROOT)),
        "stderr_log": str(pg_check_stderr.relative_to(REPO_ROOT)),
        "claim_boundary": CLAIM_BOUNDARY,
        "current_benchmark_metric_evidence": CURRENT_BENCHMARK_METRIC_EVIDENCE,
    }
)

for row in matrix_rows:
    base = {
        "row_key": row["row_key"].lower(),
        "record_kind": "execution_row",
        "case_id": row["case_id"],
        "pool": row["pool"],
        "engine": row["engine"],
        "method_id": row["method_id"],
        "route_id": row["route_id"],
        "denominator_id": row["denominator_id"],
        "execution_denominator_id": row["execution_denominator_id"],
        "generation_row_status": row["generation_row_status"],
        "claim_boundary": row["claim_boundary"],
        "current_benchmark_metric_evidence": row["current_benchmark_metric_evidence"].strip().lower() == "true",
        "generated_sql_path": row["generated_sql_path"],
        "source_sql_path": row["source_sql_path"],
        "schema_path": row["schema_path"],
        "witness_data_path": row["witness_data_path"],
        "stdout_log": row["expected_stdout_log_path"],
        "stderr_log": row["expected_stderr_log_path"],
        "caveat": row["caveat"],
        "source_generation_run_id": SOURCE_GENERATION_RUN_ID,
        "source_generation_run_results_path": SOURCE_GENERATION_RUN_RESULTS,
    }

    if pg_check_exit_code != 0:
        blocked = {
            "execution_status_observed": "not_executed_preflight_failed",
            "consistency_check_status": "not_checked_preflight_failed",
            "preflight_failure": "pg_check_failed",
            "result_check_path": row["expected_result_check_path"],
            "source_output_path": row["expected_source_output_path"],
            "generated_output_path": row["expected_generated_output_path"],
        }
        payload = {**base, **blocked}
        write_json(REPO_ROOT / row["expected_result_check_path"], blocked)
        records.append(payload)
        continue

    result = run_pg_row(row)
    payload = {
        **base,
        **result,
    }
    records.append(payload)

write_jsonl(RECORDS_JSONL, records)

row_records = [record for record in records if record["record_kind"] == "execution_row"]
execution_status_counts = Counter(record["execution_status_observed"] for record in row_records)
consistency_status_counts = Counter(record["consistency_check_status"] for record in row_records)

payload = {
    "run_id": RUN_ID,
    "method_id": METHOD_ID,
    "route_id": ROUTE_ID,
    "generation_denominator_id": GENERATION_DENOMINATOR_ID,
    "execution_denominator_id": EXECUTION_DENOMINATOR_ID,
    "planned_execution_rows": len(matrix_rows),
    "git_commit": git_commit(),
    "claim_boundary": CLAIM_BOUNDARY,
    "current_benchmark_metric_evidence": CURRENT_BENCHMARK_METRIC_EVIDENCE,
    "source_generation_run_id": SOURCE_GENERATION_RUN_ID,
    "source_generation_run_results_path": SOURCE_GENERATION_RUN_RESULTS,
    "pg_check_exit_code": pg_check_exit_code,
    "counts_by_execution_status": dict(execution_status_counts),
    "counts_by_consistency_status": dict(consistency_status_counts),
    "rows": row_records,
    "notes": [
        "execution_validity_package_for_generated_pg15_from_pg40_expansion_only",
        "no_timing_computed",
        "no_speedup_computed",
        "no_leaderboard_created",
        "failed_generation_rows_remain_in_pg40_generation_denominator_outside_this_execution_subset",
        "existing_pg7_retained_evidence_is_not_overwritten",
    ],
}
write_json(RUN_RESULTS_JSON, payload)
PY
