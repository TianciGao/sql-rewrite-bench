#!/usr/bin/env bash
set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../../../../.." && pwd)"
RUN_DIR="${SCRIPT_DIR}"
LOG_DIR="${RUN_DIR}/logs"
WORKSPACE_DIR="${RUN_DIR}/workspaces"
TIMING_DIR="${RUN_DIR}/timings"
MATRIX_CSV="${RUN_DIR}/timing_command_matrix.csv"
RUN_RESULTS_JSON="${RUN_DIR}/run_results.json"
WARMUP_COUNT=1
REPEAT_COUNT=3

if [[ "$(pwd)" != "${REPO_ROOT}" ]]; then
  echo "This script must be run from the repository root: ${REPO_ROOT}" >&2
  exit 1
fi

mkdir -p "${LOG_DIR}" "${WORKSPACE_DIR}" "${TIMING_DIR}"

echo "Human-run only."
echo "Codex must not execute this script."
echo "This timing package targets the 21 Calcite HEP PG40 timing-eligible rows only."
echo "It does not compute final GM_Speedup, final RegressionRate@20%, or any leaderboard."

source "${REPO_ROOT}/scripts/env_postgres.sh"

python - "$REPO_ROOT" "$RUN_DIR" "$MATRIX_CSV" "$RUN_RESULTS_JSON" "$WARMUP_COUNT" "$REPEAT_COUNT" <<'PY'
from __future__ import annotations

import csv
import json
import re
import shutil
import statistics
import subprocess
import sys
import time
import traceback
from collections import Counter
from pathlib import Path
from typing import Any

REPO_ROOT = Path(sys.argv[1])
RUN_DIR = Path(sys.argv[2])
MATRIX_CSV = Path(sys.argv[3])
RUN_RESULTS_JSON = Path(sys.argv[4])
WARMUP_COUNT = int(sys.argv[5])
REPEAT_COUNT = int(sys.argv[6])

DENOMINATOR_ID = "common_core_v0_40_pg40"
METHOD_ID = "calcite_hep"
ROUTE_ID = "calcite_hep_pg_rewrite"
RUN_ID = "calcite_hep_pg40_timing_01"


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


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


def read_rows() -> list[dict[str, str]]:
    with MATRIX_CSV.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def make_schema_name(case_id: str, route_id: str) -> str:
    raw = f"ccv0_calcite_timing_{case_id.lower()}_{route_id.lower()}"
    return re.sub(r"[^a-z0-9_]", "_", raw)[:55]


def run_pg_timed_query(
    schema_name: str,
    schema_sql: Path,
    witness_sql: Path,
    query_sql: Path,
    stdout_handle,
    stderr_handle,
) -> float:
    psql_base = ["psql", "-v", "ON_ERROR_STOP=1", "-X", "-q"]
    start = time.perf_counter()
    try:
        subprocess.run(
            psql_base + ["-c", f"DROP SCHEMA IF EXISTS {schema_name} CASCADE; CREATE SCHEMA {schema_name};"],
            cwd=REPO_ROOT,
            check=True,
            stdout=stdout_handle,
            stderr=stderr_handle,
            text=True,
        )
        subprocess.run(
            psql_base + ["-c", f"SET search_path TO {schema_name};", "-f", str(schema_sql)],
            cwd=REPO_ROOT,
            check=True,
            stdout=stdout_handle,
            stderr=stderr_handle,
            text=True,
        )
        subprocess.run(
            psql_base + ["-c", f"SET search_path TO {schema_name};", "-f", str(witness_sql)],
            cwd=REPO_ROOT,
            check=True,
            stdout=stdout_handle,
            stderr=stderr_handle,
            text=True,
        )
        subprocess.run(
            psql_base + ["-c", f"SET search_path TO {schema_name};", "-f", str(query_sql)],
            cwd=REPO_ROOT,
            check=True,
            stdout=stdout_handle,
            stderr=stderr_handle,
            text=True,
        )
    finally:
        subprocess.run(
            ["psql", "-v", "ON_ERROR_STOP=0", "-X", "-q", "-c", f"DROP SCHEMA IF EXISTS {schema_name} CASCADE;"],
            cwd=REPO_ROOT,
            check=False,
            stdout=stdout_handle,
            stderr=stderr_handle,
            text=True,
        )
    return (time.perf_counter() - start) * 1000.0


def run_row(row: dict[str, str]) -> dict[str, Any]:
    case_id = row["case_id"]
    pool = row["pool"]
    route_id = row["route_id"]
    stdout_log = REPO_ROOT / row["expected_log_stdout"]
    stderr_log = REPO_ROOT / row["expected_log_stderr"]
    workspace_dir = REPO_ROOT / row["expected_workspace_dir"]
    timing_json_path = REPO_ROOT / row["expected_timing_output_path"]
    source_sql = REPO_ROOT / row["source_sql_path"]
    generated_sql = REPO_ROOT / row["generated_sql_path"]
    schema_path = REPO_ROOT / row["schema_path"]
    witness_path = REPO_ROOT / row["witness_data_path"]

    for path in [stdout_log.parent, stderr_log.parent, workspace_dir, timing_json_path.parent]:
        path.mkdir(parents=True, exist_ok=True)

    schema_copy = workspace_dir / "ddl_pg.sql"
    witness_copy = workspace_dir / "pg_witness_data.sql"
    source_copy = workspace_dir / "source.sql"
    generated_copy = workspace_dir / "generated.sql"
    shutil.copyfile(schema_path, schema_copy)
    shutil.copyfile(witness_path, witness_copy)
    shutil.copyfile(source_sql, source_copy)
    shutil.copyfile(generated_sql, generated_copy)

    payload: dict[str, Any] = {
        "case_id": case_id,
        "pool": pool,
        "engine": "pg",
        "route_id": route_id,
        "method_id": METHOD_ID,
        "denominator_id": DENOMINATOR_ID,
        "warmup_count": WARMUP_COUNT,
        "repeat_count": REPEAT_COUNT,
        "source_runtime_ms": [],
        "generated_runtime_ms": [],
        "median_source_ms": None,
        "median_generated_ms": None,
        "speedup_ratio": None,
        "timing_status": "timing_failed",
        "timing_json_path": row["expected_timing_output_path"],
        "stdout_log": row["expected_log_stdout"],
        "stderr_log": row["expected_log_stderr"],
        "notes": "",
        "caveat": row["caveat"],
    }

    schema_name = make_schema_name(case_id, route_id)

    with stdout_log.open("w", encoding="utf-8") as stdout_handle, stderr_log.open("w", encoding="utf-8") as stderr_handle:
        stdout_handle.write(f"case_id={case_id} pool={pool} engine=pg route_id={route_id}\n")
        stdout_handle.write(f"warmup_count={WARMUP_COUNT} repeat_count={REPEAT_COUNT}\n")
        try:
            for _ in range(WARMUP_COUNT):
                run_pg_timed_query(schema_name, schema_copy, witness_copy, source_copy, stdout_handle, stderr_handle)
                run_pg_timed_query(schema_name, schema_copy, witness_copy, generated_copy, stdout_handle, stderr_handle)
            for _ in range(REPEAT_COUNT):
                payload["source_runtime_ms"].append(
                    run_pg_timed_query(schema_name, schema_copy, witness_copy, source_copy, stdout_handle, stderr_handle)
                )
                payload["generated_runtime_ms"].append(
                    run_pg_timed_query(schema_name, schema_copy, witness_copy, generated_copy, stdout_handle, stderr_handle)
                )
            payload["median_source_ms"] = statistics.median(payload["source_runtime_ms"])
            payload["median_generated_ms"] = statistics.median(payload["generated_runtime_ms"])
            if payload["median_generated_ms"] and payload["median_generated_ms"] > 0:
                payload["speedup_ratio"] = payload["median_source_ms"] / payload["median_generated_ms"]
            payload["timing_status"] = "timing_success"
        except Exception as exc:
            traceback.print_exc(file=stderr_handle)
            payload["notes"] = f"timing_runner_failed: {type(exc).__name__}: {exc}"

    write_json(timing_json_path, payload)
    return payload


rows = read_rows()
records = [run_row(row) for row in rows]

summary = {
    "run_id": RUN_ID,
    "denominator_id": DENOMINATOR_ID,
    "method_id": METHOD_ID,
    "route_id": ROUTE_ID,
    "planned_timing_rows": len(rows),
    "warmup_count": WARMUP_COUNT,
    "repeat_count": REPEAT_COUNT,
    "git_commit": git_commit(),
    "counts_by_pool": dict(Counter(record["pool"] for record in records)),
    "counts_by_timing_status": dict(Counter(record["timing_status"] for record in records)),
    "records": records,
}
write_json(RUN_RESULTS_JSON, summary)
print(f"wrote {RUN_RESULTS_JSON}")
PY
