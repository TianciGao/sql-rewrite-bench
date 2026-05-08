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
echo "This package produces exploratory PostgreSQL execution and validity evidence only."
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

RUN_ID = "r_bot_pg1_execution_canary_01"
METHOD_ID = "r_bot"
ROUTE_ID = "r_bot_pg_rewrite"
CASE_ID = "PERF_0006"
DENOMINATOR_ID = "common_core_v0_40_pg40"
CANARY_DENOMINATOR_ID = "common_core_v0_40_perf_pg1_r_bot_execution_canary"
CLAIM_BOUNDARY = "exploratory_smoke_only_not_current_common_core_metric_evidence"
CURRENT_BENCHMARK_METRIC_EVIDENCE = False
RECOVERY_RUN_ID = "r_bot_pg1_recovery_canary_01"


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

    schema_name = re.sub(r"[^a-z0-9_]", "_", f"rbot_pg1_exec_{row['case_id'].lower()}_{row['route_id'].lower()}")[:55]
    psql_base = ["psql", "-v", "ON_ERROR_STOP=1", "-X", "-q"]

    with stdout_log.open("w", encoding="utf-8") as stdout_handle, stderr_log.open("w", encoding="utf-8") as stderr_handle:
        try:
            stdout_handle.write(
                f"row={row['case_id']} engine={row['engine']} route={row['route_id']} claim_boundary={CLAIM_BOUNDARY}\n"
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
        "row_key": f"{row['case_id'].lower()}__{row['engine']}__{row['route_id']}",
        "record_kind": "execution_row",
        "case_id": row["case_id"],
        "pool": row["pool"],
        "engine": row["engine"],
        "method_id": row["method_id"],
        "route_id": row["route_id"],
        "denominator_id": DENOMINATOR_ID,
        "canary_denominator_id": CANARY_DENOMINATOR_ID,
        "planned_row_status": row["planned_row_status"],
        "claim_boundary": row["claim_boundary"],
        "current_benchmark_metric_evidence": row["current_benchmark_metric_evidence"].strip().lower() == "true",
        "generated_sql_path": row["generated_sql_path"],
        "source_sql_path": row["source_sql_path"],
        "schema_path": row["schema_path"],
        "witness_data_path": row["witness_data_path"],
        "stdout_log": row["expected_stdout_log_path"],
        "stderr_log": row["expected_stderr_log_path"],
        "caveat": row["caveat"],
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
        write_json(REPO_ROOT / row["expected_result_check_path"], {**base, **blocked})
        records.append({**base, **blocked})
        continue

    observed = run_pg_row(row)
    records.append({**base, **observed})

row_records = [record for record in records if record["record_kind"] == "execution_row"]
counts_exec = Counter(record["execution_status_observed"] for record in row_records)
counts_consistency = Counter(record["consistency_check_status"] for record in row_records)

summary = {
    "run_id": RUN_ID,
    "mode": "manual_human_execution",
    "method_id": METHOD_ID,
    "route_id": ROUTE_ID,
    "case_id": CASE_ID,
    "engine": "pg",
    "pool": "performance",
    "planned_rows": len(matrix_rows),
    "rows_ready_to_execute": sum(1 for row in matrix_rows if row["planned_row_status"] == "ready_to_execute"),
    "denominator_id": DENOMINATOR_ID,
    "canary_denominator_id": CANARY_DENOMINATOR_ID,
    "claim_boundary": CLAIM_BOUNDARY,
    "current_benchmark_metric_evidence": CURRENT_BENCHMARK_METRIC_EVIDENCE,
    "recovery_run_reference": {
        "run_id": RECOVERY_RUN_ID,
        "run_results_path": "reports/evaluation/common_core_v0/runs/r_bot_pg1_recovery_canary_01/run_results.json",
        "generated_sql_path": "reports/evaluation/common_core_v0/runs/r_bot_pg1_recovery_canary_01/generated/PERF_0006/pg/r_bot_pg_rewrite.sql",
    },
    "git_commit": git_commit(),
    "pg_check_exit_code": pg_check_exit_code,
    "counts_by_execution_status_observed": dict(counts_exec),
    "counts_by_consistency_check_status": dict(counts_consistency),
    "records": records,
    "notes": [
        "exploratory_pg1_recovery_evidence_only",
        "do_not_treat_as_current_common_core_metric_evidence",
        "no_timing_no_speedup_no_leaderboard",
        "generated_sql_is_executed_as_retained_from_recovery_package_without_modification",
    ],
}

write_json(RUN_RESULTS_JSON, summary)
write_jsonl(RECORDS_JSONL, records)
print(f"wrote {RUN_RESULTS_JSON}")
PY
