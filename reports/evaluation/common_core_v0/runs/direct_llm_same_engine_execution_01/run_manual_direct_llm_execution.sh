#!/usr/bin/env bash
set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../../../../.." && pwd)"
RUN_DIR="${SCRIPT_DIR}"
LOG_DIR="${RUN_DIR}/logs"
WORKSPACE_DIR="${RUN_DIR}/workspaces"
MATRIX_CSV="${RUN_DIR}/execution_command_matrix.csv"
RECORDS_JSONL="${RUN_DIR}/records.tmp.jsonl"
RUN_RESULTS_JSON="${RUN_DIR}/run_results.json"

if [[ "$(pwd)" != "${REPO_ROOT}" ]]; then
  echo "This script must be run from the repository root: ${REPO_ROOT}" >&2
  exit 1
fi

mkdir -p "${LOG_DIR}" "${WORKSPACE_DIR}"

echo "Human-run only."
echo "Codex must not execute this script."
echo "This script prepares execution evidence only."
echo "It does not compute timing, speedup, or any leaderboard artifact."
echo "It does not use tmp_repo and must be run from the real repository root."

source "${REPO_ROOT}/scripts/env_postgres.sh"
source "${REPO_ROOT}/scripts/env_mysql.sh"
source "${REPO_ROOT}/scripts/env_spark.sh"

ENV_STDOUT="${LOG_DIR}/env_check.stdout.log"
ENV_STDERR="${LOG_DIR}/env_check.stderr.log"
ENV_CHECK_EXIT_CODE=0
python -m scripts.cli env-check >"${ENV_STDOUT}" 2>"${ENV_STDERR}" || ENV_CHECK_EXIT_CODE=$?

python - "$REPO_ROOT" "$RUN_DIR" "$MATRIX_CSV" "$RECORDS_JSONL" "$RUN_RESULTS_JSON" "$ENV_CHECK_EXIT_CODE" "$ENV_STDOUT" "$ENV_STDERR" <<'PY'
from __future__ import annotations

import csv
import json
import os
import re
import shutil
import subprocess
import sys
import traceback
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


REPO_ROOT = Path(sys.argv[1])
RUN_DIR = Path(sys.argv[2])
MATRIX_CSV = Path(sys.argv[3])
RECORDS_JSONL = Path(sys.argv[4])
RUN_RESULTS_JSON = Path(sys.argv[5])
ENV_CHECK_EXIT_CODE = int(sys.argv[6])
ENV_STDOUT = sys.argv[7]
ENV_STDERR = sys.argv[8]

RUN_ID = "direct_llm_same_engine_execution_01"
METHOD_ID = "direct_llm"
ROUTE_ID = "direct_llm_same_engine_rewrite"
DENOMINATOR_ID = "common_core_v0_40"


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


def copy_inputs(workspace: Path, row: dict[str, str]) -> dict[str, Path]:
    workspace.mkdir(parents=True, exist_ok=True)
    copied = {
        "schema": workspace / Path(row["schema_path"]).name,
        "witness": workspace / Path(row["witness_data_path"]).name,
        "source": workspace / "source.sql",
        "generated": workspace / "generated.sql",
    }
    shutil.copyfile(REPO_ROOT / row["schema_path"], copied["schema"])
    shutil.copyfile(REPO_ROOT / row["witness_data_path"], copied["witness"])
    shutil.copyfile(REPO_ROOT / row["source_sql_path"], copied["source"])
    shutil.copyfile(REPO_ROOT / row["generated_sql_path"], copied["generated"])
    return copied


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
        "source_output_path": str(source_path.relative_to(REPO_ROOT)),
        "generated_output_path": str(generated_path.relative_to(REPO_ROOT)),
        "exact_match": exact_match,
        "sorted_match": sorted_match,
        "consistency_check_status": status,
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
        r"CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?(?:`([^`]+)`|([A-Za-z_][A-Za-z0-9_]*))",
        re.IGNORECASE,
    )
    table_names: list[str] = []
    for match in pattern.finditer(ddl_text):
        table_name = match.group(1) or match.group(2)
        if table_name and table_name not in table_names:
            table_names.append(table_name)
    return table_names


def run_postgres_row(row: dict[str, str], stdout_log: Path, stderr_log: Path) -> dict[str, Any]:
    workspace = (REPO_ROOT / row["expected_output_path"]).parent
    copied = copy_inputs(workspace, row)
    source_out = workspace / "source.tsv"
    generated_out = workspace / "generated.tsv"
    result_check = workspace / "result_check.json"
    schema_name = re.sub(r"[^a-z0-9_]", "_", f"ccv0_direct_llm_{row['case_id'].lower()}_{row['engine']}")[:55]
    psql_base = ["psql", "-v", "ON_ERROR_STOP=1", "-X", "-q"]

    with stdout_log.open("w", encoding="utf-8") as stdout_handle, stderr_log.open("w", encoding="utf-8") as stderr_handle:
        try:
            stdout_handle.write(f"row={row['case_id']} engine={row['engine']} route={row['route_id']}\n")
            subprocess.run(psql_base + ["-c", f"DROP SCHEMA IF EXISTS {schema_name} CASCADE; CREATE SCHEMA {schema_name};"], cwd=REPO_ROOT, check=True, stdout=stdout_handle, stderr=stderr_handle, text=True)
            for path in [copied["schema"], copied["witness"]]:
                subprocess.run(psql_base + ["-c", f"SET search_path TO {schema_name};", "-f", str(path)], cwd=REPO_ROOT, check=True, stdout=stdout_handle, stderr=stderr_handle, text=True)

            source_query = normalize_query_text(copied["source"].read_text(encoding="utf-8"))
            generated_query = normalize_query_text(copied["generated"].read_text(encoding="utf-8"))
            source_copy_sql = f"COPY ({source_query}) TO STDOUT WITH (FORMAT CSV, DELIMITER E'\\t', NULL 'NULL');"
            generated_copy_sql = f"COPY ({generated_query}) TO STDOUT WITH (FORMAT CSV, DELIMITER E'\\t', NULL 'NULL');"

            with source_out.open("w", encoding="utf-8") as handle:
                subprocess.run(psql_base + ["-c", f"SET search_path TO {schema_name};", "-c", source_copy_sql], cwd=REPO_ROOT, check=True, stdout=handle, stderr=stderr_handle, text=True)
            with generated_out.open("w", encoding="utf-8") as handle:
                subprocess.run(psql_base + ["-c", f"SET search_path TO {schema_name};", "-c", generated_copy_sql], cwd=REPO_ROOT, check=True, stdout=handle, stderr=stderr_handle, text=True)

            compare = compare_tsv_outputs(source_out, generated_out)
            payload = {
                "execution_status_observed": "executed",
                **compare,
                "result_check_path": str(result_check.relative_to(REPO_ROOT)),
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
                "result_check_path": str(result_check.relative_to(REPO_ROOT)),
            }
            write_json(result_check, payload)
            return payload
        finally:
            subprocess.run(["psql", "-v", "ON_ERROR_STOP=0", "-X", "-q", "-c", f"DROP SCHEMA IF EXISTS {schema_name} CASCADE;"], cwd=REPO_ROOT, stdout=stdout_handle, stderr=stderr_handle, text=True)


def run_mysql_row(row: dict[str, str], stdout_log: Path, stderr_log: Path) -> dict[str, Any]:
    workspace = (REPO_ROOT / row["expected_output_path"]).parent
    copied = copy_inputs(workspace, row)
    source_out = workspace / "source.tsv"
    generated_out = workspace / "generated.tsv"
    result_check = workspace / "result_check.json"
    db_name = os.environ.get("MYSQL_DATABASE", "")
    mysql_base = mysql_args()
    if not db_name:
        payload = {
            "execution_status_observed": "execution_failed",
            "consistency_check_status": "not_checked_execution_failed",
            "error_type": "MissingEnvironment",
            "error_message": "MYSQL_DATABASE is not set",
            "result_check_path": str(result_check.relative_to(REPO_ROOT)),
        }
        write_json(result_check, payload)
        return payload

    ddl_text = copied["schema"].read_text(encoding="utf-8")
    table_names = extract_table_names(ddl_text)
    drop_sql = ""
    if table_names:
        joined = ", ".join(f"`{name}`" for name in table_names)
        drop_sql = f"DROP TABLE IF EXISTS {joined};"

    with stdout_log.open("w", encoding="utf-8") as stdout_handle, stderr_log.open("w", encoding="utf-8") as stderr_handle:
        def mysql_exec(sql: str, output_path: Path | None = None) -> None:
            cmd = mysql_base + [db_name, "--batch", "--raw", "--skip-column-names", "-e", sql]
            if output_path is None:
                subprocess.run(cmd, cwd=REPO_ROOT, check=True, stdout=stdout_handle, stderr=stderr_handle, text=True)
            else:
                with output_path.open("w", encoding="utf-8") as handle:
                    subprocess.run(cmd, cwd=REPO_ROOT, check=True, stdout=handle, stderr=stderr_handle, text=True)

        try:
            stdout_handle.write(f"row={row['case_id']} engine={row['engine']} route={row['route_id']}\n")
            if drop_sql:
                mysql_exec(drop_sql)
            mysql_exec(f"source {copied['schema']};")
            mysql_exec(f"source {copied['witness']};")
            mysql_exec(normalize_query_text(copied["source"].read_text(encoding='utf-8')), source_out)
            mysql_exec(normalize_query_text(copied["generated"].read_text(encoding='utf-8')), generated_out)
            compare = compare_tsv_outputs(source_out, generated_out)
            payload = {
                "execution_status_observed": "executed",
                **compare,
                "result_check_path": str(result_check.relative_to(REPO_ROOT)),
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
                "result_check_path": str(result_check.relative_to(REPO_ROOT)),
            }
            write_json(result_check, payload)
            return payload
        finally:
            if drop_sql:
                try:
                    mysql_exec(drop_sql)
                except Exception:
                    traceback.print_exc(file=stderr_handle)


def spark_read_statements(text: str) -> list[str]:
    return [stmt.strip() for stmt in text.split(";") if stmt.strip()]


def spark_write_df(df: Any, output_path: Path) -> None:
    rows = df.collect()
    with output_path.open("w", encoding="utf-8") as handle:
        for row in rows:
            values = []
            for value in row:
                if value is None:
                    values.append("NULL")
                else:
                    values.append(str(value))
            handle.write("\t".join(values) + "\n")


def run_spark_row(row: dict[str, str], stdout_log: Path, stderr_log: Path) -> dict[str, Any]:
    workspace = (REPO_ROOT / row["expected_output_path"]).parent
    copied = copy_inputs(workspace, row)
    source_out = workspace / "source.tsv"
    generated_out = workspace / "generated.tsv"
    result_check = workspace / "result_check.json"
    warehouse_dir = workspace / "warehouse"
    warehouse_dir.mkdir(parents=True, exist_ok=True)

    with stdout_log.open("w", encoding="utf-8") as stdout_handle, stderr_log.open("w", encoding="utf-8") as stderr_handle:
        spark = None
        try:
            from pyspark.sql import SparkSession

            stdout_handle.write(f"row={row['case_id']} engine={row['engine']} route={row['route_id']}\n")
            spark = (
                SparkSession.builder
                .master("local[*]")
                .appName(f"ccv0_direct_llm_{row['case_id'].lower()}_{row['route_id']}")
                .config("spark.ui.enabled", "false")
                .config("spark.sql.shuffle.partitions", "1")
                .config("spark.sql.warehouse.dir", str(warehouse_dir))
                .getOrCreate()
            )
            for path in [copied["schema"], copied["witness"]]:
                for stmt in spark_read_statements(path.read_text(encoding="utf-8")):
                    spark.sql(stmt).collect()
            source_df = spark.sql(normalize_query_text(copied["source"].read_text(encoding="utf-8")))
            generated_df = spark.sql(normalize_query_text(copied["generated"].read_text(encoding="utf-8")))
            spark_write_df(source_df, source_out)
            spark_write_df(generated_df, generated_out)
            compare = compare_tsv_outputs(source_out, generated_out)
            payload = {
                "execution_status_observed": "executed",
                **compare,
                "result_check_path": str(result_check.relative_to(REPO_ROOT)),
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
                "result_check_path": str(result_check.relative_to(REPO_ROOT)),
            }
            write_json(result_check, payload)
            return payload
        finally:
            if spark is not None:
                try:
                    spark.stop()
                except Exception:
                    traceback.print_exc(file=stderr_handle)


rows = read_rows()
records: list[dict[str, Any]] = [
    {
        "row_key": "env_check",
        "case_id": "",
        "pool": "",
        "engine": "",
        "route_id": "",
        "preflight_status": "env_check",
        "execution_status_expected": "env_check",
        "execution_status_observed": "executed" if ENV_CHECK_EXIT_CODE == 0 else "execution_failed",
        "consistency_check_status": "not_applicable",
        "expected_log_stdout": str(Path(ENV_STDOUT).relative_to(REPO_ROOT)),
        "expected_log_stderr": str(Path(ENV_STDERR).relative_to(REPO_ROOT)),
        "notes": "python -m scripts.cli env-check",
        "exit_code": ENV_CHECK_EXIT_CODE,
    }
]

for row in rows:
    stdout_log = REPO_ROOT / row["expected_log_stdout"]
    stderr_log = REPO_ROOT / row["expected_log_stderr"]
    stdout_log.parent.mkdir(parents=True, exist_ok=True)
    stderr_log.parent.mkdir(parents=True, exist_ok=True)

    base_record = {
        "row_key": f"{row['case_id'].lower()}__{row['engine']}__{row['route_id']}",
        "case_id": row["case_id"],
        "pool": row["pool"],
        "engine": row["engine"],
        "route_id": row["route_id"],
        "generated_sql_path": row["generated_sql_path"],
        "source_sql_path": row["source_sql_path"],
        "schema_path": row["schema_path"],
        "witness_data_path": row["witness_data_path"],
        "control_source_artifact": row["control_source_artifact"],
        "expected_output_path": row["expected_output_path"],
        "expected_log_stdout": row["expected_log_stdout"],
        "expected_log_stderr": row["expected_log_stderr"],
        "preflight_status": row["preflight_status"],
        "execution_status_expected": row["execution_status"],
        "consistency_check_status_expected": row["consistency_check_status"],
        "exclusion_reason": row["exclusion_reason"],
        "caveat": row["caveat"],
    }

    if row["execution_status"] != "ready_to_execute":
        records.append(
            {
                **base_record,
                "execution_status_observed": "not_executed_preflight_blocked",
                "consistency_check_status": "not_checked_preflight_blocked",
                "notes": "Row remains explicit and is not executed because required preflight artifacts are missing.",
            }
        )
        continue

    if row["engine"] == "pg":
        observed = run_postgres_row(row, stdout_log, stderr_log)
    elif row["engine"] == "mysql":
        observed = run_mysql_row(row, stdout_log, stderr_log)
    elif row["engine"] == "spark":
        observed = run_spark_row(row, stdout_log, stderr_log)
    else:
        observed = {
            "execution_status_observed": "execution_failed",
            "consistency_check_status": "not_checked_execution_failed",
            "error_type": "UnknownEngine",
            "error_message": f"Unknown engine: {row['engine']}",
        }

    records.append({**base_record, **observed})

summary_counter = Counter(record.get("execution_status_observed", "") for record in records if record["row_key"] != "env_check")
pool_counter: dict[str, Counter[str]] = defaultdict(Counter)
engine_counter: dict[str, Counter[str]] = defaultdict(Counter)
for record in records:
    if record["row_key"] == "env_check":
        continue
    pool_counter[record["pool"]][record["execution_status_expected"]] += 1
    engine_counter[record["engine"]][record["execution_status_expected"]] += 1

payload = {
    "run_id": RUN_ID,
    "mode": "manual_human_execution",
    "repo_root": str(REPO_ROOT),
    "denominator_id": DENOMINATOR_ID,
    "method_id": METHOD_ID,
    "route_id": ROUTE_ID,
    "git_commit": git_commit(),
    "planned_rows": len(rows),
    "ready_to_execute_rows": sum(1 for row in rows if row["execution_status"] == "ready_to_execute"),
    "preflight_caveat_rows": sum(1 for row in rows if row["preflight_status"] == "preflight_caveat"),
    "blocked_rows": sum(1 for row in rows if row["preflight_status"] == "preflight_blocked_missing_artifact"),
    "summary_counts": dict(summary_counter),
    "counts_by_pool": {pool: dict(counter) for pool, counter in sorted(pool_counter.items())},
    "counts_by_engine": {engine: dict(counter) for engine, counter in sorted(engine_counter.items())},
    "records": records,
}

write_jsonl(RECORDS_JSONL, records)
write_json(RUN_RESULTS_JSON, payload)
PY

exit 0
