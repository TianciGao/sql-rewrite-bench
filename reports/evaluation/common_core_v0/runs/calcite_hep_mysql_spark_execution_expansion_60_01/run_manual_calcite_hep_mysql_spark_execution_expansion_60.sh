#!/usr/bin/env bash
set -u

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

RUN_DIR="$SCRIPT_DIR"
LOG_DIR="$RUN_DIR/logs"
WORKSPACE_DIR="$RUN_DIR/workspaces"
METADATA_DIR="$RUN_DIR/metadata"
MATRIX_CSV="$RUN_DIR/execution_command_matrix.csv"
RUN_RESULTS_JSON="$RUN_DIR/run_results.json"
RUN_EVENT_LONG_CSV="$RUN_DIR/run_event_long.csv"
RECORDS_JSONL="$RUN_DIR/records.tmp.jsonl"

if [[ "$(pwd)" != "$REPO_ROOT" ]]; then
  echo "This script must be run from the repository root: $REPO_ROOT" >&2
  exit 1
fi

mkdir -p "$LOG_DIR" "$WORKSPACE_DIR" "$METADATA_DIR"
: > "$RECORDS_JSONL"

echo "Human-run only."
echo "Codex must not execute this script."
echo "This package produces MySQL/Spark execution and validity evidence only."
echo "It does not compute timing, speedup, or leaderboard artifacts."

source "$REPO_ROOT/scripts/env_mysql.sh"
source "$REPO_ROOT/scripts/env_spark.sh"

python - "$REPO_ROOT" "$RUN_DIR" "$MATRIX_CSV" "$RUN_RESULTS_JSON" "$RUN_EVENT_LONG_CSV" "$RECORDS_JSONL" <<'PY'
from __future__ import annotations

import csv
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import traceback
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

REPO_ROOT = Path(sys.argv[1])
RUN_DIR = Path(sys.argv[2])
MATRIX_CSV = Path(sys.argv[3])
RUN_RESULTS_JSON = Path(sys.argv[4])
RUN_EVENT_LONG_CSV = Path(sys.argv[5])
RECORDS_JSONL = Path(sys.argv[6])

RUN_ID = "calcite_hep_mysql_spark_execution_expansion_60_01"
METHOD_ID = "calcite_hep"
ROUTE_ID = "calcite_hep_same_engine_rewrite"
SOURCE_REWRITE_RUN_ID = "calcite_hep_mysql_spark_rewrite_expansion_80_01"
EXECUTION_DENOMINATOR_ID = "calcite_hep_mysql_spark_execution_expansion_60_only"
CLAIM_BOUNDARY = "mysql_spark_execution_validity_expansion_60_only_not_timing_speedup_or_leaderboard_evidence"


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


def normalize_query_text(text: str) -> str:
    return text.strip().rstrip(";").strip()


def compare_tsv_outputs(source_path: Path, generated_path: Path) -> dict[str, Any]:
    source_text = source_path.read_text(encoding="utf-8")
    generated_text = generated_path.read_text(encoding="utf-8")
    exact_match = source_text == generated_text
    status = "match_exact" if exact_match else "mismatch"
    return {
        "exact_match": exact_match,
        "consistency_status": status,
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


def copy_inputs(workspace: Path, row: dict[str, str]) -> dict[str, Path]:
    workspace.mkdir(parents=True, exist_ok=True)
    ext = row["engine"]
    copied = {
        "schema": workspace / f"ddl_{ext}.sql",
        "witness": workspace / f"{ext}_witness_data.sql",
        "source": workspace / "source.sql",
        "generated": workspace / "generated.sql",
    }
    shutil.copyfile(REPO_ROOT / row["schema_path"], copied["schema"])
    shutil.copyfile(REPO_ROOT / row["witness_data_path"], copied["witness"])
    shutil.copyfile(REPO_ROOT / row["source_sql_path"], copied["source"])
    shutil.copyfile(REPO_ROOT / row["generated_sql_path"], copied["generated"])
    return copied


def run_mysql_row(row: dict[str, str]) -> dict[str, Any]:
    workspace = REPO_ROOT / row["expected_workspace_dir"]
    copied = copy_inputs(workspace, row)
    source_out = REPO_ROOT / row["expected_source_tsv_path"]
    generated_out = REPO_ROOT / row["expected_generated_tsv_path"]
    result_check = REPO_ROOT / row["expected_result_check_path"]
    source_stdout = REPO_ROOT / row["expected_source_stdout_log"]
    source_stderr = REPO_ROOT / row["expected_source_stderr_log"]
    generated_stdout = REPO_ROOT / row["expected_generated_stdout_log"]
    generated_stderr = REPO_ROOT / row["expected_generated_stderr_log"]
    for path in [source_out.parent, source_stdout.parent, generated_stdout.parent]:
        path.mkdir(parents=True, exist_ok=True)

    db_name = os.environ.get("MYSQL_DATABASE", "")
    mysql_base = mysql_args()
    if not db_name:
        payload = {
            "execution_status": "setup_failed",
            "consistency_status": "not_applicable",
            "error_type": "MissingEnvironment",
            "error_message": "MYSQL_DATABASE is not set",
        }
        write_json(result_check, payload)
        return payload

    ddl_text = copied["schema"].read_text(encoding="utf-8")
    table_names = extract_table_names(ddl_text)
    drop_sql = ""
    if table_names:
        joined = ", ".join(f"`{name}`" for name in table_names)
        drop_sql = f"DROP TABLE IF EXISTS {joined};"

    def mysql_exec(sql: str, stdout_path: Path, stderr_path: Path, batch_output: bool = False) -> None:
        cmd = mysql_base + [db_name]
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
    except Exception as exc:
        with source_stderr.open("a", encoding="utf-8") as handle:
            traceback.print_exc(file=handle)
        payload = {
            "execution_status": "setup_failed",
            "consistency_status": "not_applicable",
            "error_type": type(exc).__name__,
            "error_message": str(exc),
        }
        write_json(result_check, payload)
        return payload

    try:
        mysql_exec(normalize_query_text(copied["source"].read_text(encoding="utf-8")), source_out, source_stderr, batch_output=True)
    except Exception as exc:
        with source_stderr.open("a", encoding="utf-8") as handle:
            traceback.print_exc(file=handle)
        payload = {
            "execution_status": "source_execution_failed",
            "consistency_status": "not_applicable",
            "error_type": type(exc).__name__,
            "error_message": str(exc),
        }
        write_json(result_check, payload)
        return payload

    try:
        mysql_exec(normalize_query_text(copied["generated"].read_text(encoding="utf-8")), generated_out, generated_stderr, batch_output=True)
    except Exception as exc:
        with generated_stderr.open("a", encoding="utf-8") as handle:
            traceback.print_exc(file=handle)
        payload = {
            "execution_status": "generated_execution_failed",
            "consistency_status": "not_applicable",
            "error_type": type(exc).__name__,
            "error_message": str(exc),
        }
        write_json(result_check, payload)
        return payload
    finally:
        if drop_sql:
            try:
                mysql_exec(drop_sql, generated_stdout, generated_stderr)
            except Exception:
                pass

    try:
        compare = compare_tsv_outputs(source_out, generated_out)
        payload = {
            "execution_status": "executed",
            **compare,
        }
    except Exception as exc:
        payload = {
            "execution_status": "comparison_failed",
            "consistency_status": "not_applicable",
            "error_type": type(exc).__name__,
            "error_message": str(exc),
        }
    write_json(result_check, payload)
    return payload


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


def run_spark_row(row: dict[str, str]) -> dict[str, Any]:
    workspace = REPO_ROOT / row["expected_workspace_dir"]
    copied = copy_inputs(workspace, row)
    source_out = REPO_ROOT / row["expected_source_tsv_path"]
    generated_out = REPO_ROOT / row["expected_generated_tsv_path"]
    result_check = REPO_ROOT / row["expected_result_check_path"]
    source_stdout = REPO_ROOT / row["expected_source_stdout_log"]
    source_stderr = REPO_ROOT / row["expected_source_stderr_log"]
    generated_stdout = REPO_ROOT / row["expected_generated_stdout_log"]
    generated_stderr = REPO_ROOT / row["expected_generated_stderr_log"]
    for path in [source_out.parent, source_stdout.parent, generated_stdout.parent]:
        path.mkdir(parents=True, exist_ok=True)

    warehouse_dir = Path(tempfile.mkdtemp(prefix=f"calcite_hep_{row['case_id'].lower()}_{row['engine']}_", dir="/tmp"))

    with source_stdout.open("w", encoding="utf-8") as source_stdout_handle, source_stderr.open("w", encoding="utf-8") as source_stderr_handle, generated_stdout.open("w", encoding="utf-8") as generated_stdout_handle, generated_stderr.open("w", encoding="utf-8") as generated_stderr_handle:
        spark = None
        try:
            from pyspark.sql import SparkSession

            spark = (
                SparkSession.builder
                .master("local[*]")
                .appName(f"ccv0_calcite_hep_{row['case_id'].lower()}_{row['engine']}")
                .config("spark.ui.enabled", "false")
                .config("spark.sql.shuffle.partitions", "1")
                .config("spark.sql.warehouse.dir", str(warehouse_dir))
                .getOrCreate()
            )
            for path in [copied["schema"], copied["witness"]]:
                for stmt in spark_read_statements(path.read_text(encoding="utf-8")):
                    spark.sql(stmt).collect()
        except Exception as exc:
            traceback.print_exc(file=source_stderr_handle)
            payload = {
                "execution_status": "setup_failed",
                "consistency_status": "not_applicable",
                "error_type": type(exc).__name__,
                "error_message": str(exc),
            }
            write_json(result_check, payload)
            if spark is not None:
                try:
                    spark.stop()
                except Exception:
                    pass
            shutil.rmtree(warehouse_dir, ignore_errors=True)
            return payload

        try:
            source_df = spark.sql(normalize_query_text(copied["source"].read_text(encoding="utf-8")))
            spark_write_df(source_df, source_out)
        except Exception as exc:
            traceback.print_exc(file=source_stderr_handle)
            payload = {
                "execution_status": "source_execution_failed",
                "consistency_status": "not_applicable",
                "error_type": type(exc).__name__,
                "error_message": str(exc),
            }
            write_json(result_check, payload)
            try:
                spark.stop()
            except Exception:
                pass
            shutil.rmtree(warehouse_dir, ignore_errors=True)
            return payload

        try:
            generated_df = spark.sql(normalize_query_text(copied["generated"].read_text(encoding="utf-8")))
            spark_write_df(generated_df, generated_out)
        except Exception as exc:
            traceback.print_exc(file=generated_stderr_handle)
            payload = {
                "execution_status": "generated_execution_failed",
                "consistency_status": "not_applicable",
                "error_type": type(exc).__name__,
                "error_message": str(exc),
            }
            write_json(result_check, payload)
            try:
                spark.stop()
            except Exception:
                pass
            shutil.rmtree(warehouse_dir, ignore_errors=True)
            return payload

        try:
            compare = compare_tsv_outputs(source_out, generated_out)
            payload = {
                "execution_status": "executed",
                **compare,
            }
        except Exception as exc:
            payload = {
                "execution_status": "comparison_failed",
                "consistency_status": "not_applicable",
                "error_type": type(exc).__name__,
                "error_message": str(exc),
            }
        write_json(result_check, payload)
        try:
            spark.stop()
        except Exception:
            traceback.print_exc(file=generated_stderr_handle)
        shutil.rmtree(warehouse_dir, ignore_errors=True)
        return payload


rows = read_rows()
records: list[dict[str, Any]] = []

for row in rows:
    base_record = {
        "run_id": RUN_ID,
        "row_key": row["row_key"],
        "case_id": row["case_id"],
        "pool": row["pool"],
        "engine": row["engine"],
        "method_id": METHOD_ID,
        "route_id": ROUTE_ID,
        "source_rewrite_run_id": SOURCE_REWRITE_RUN_ID,
        "execution_denominator_id": EXECUTION_DENOMINATOR_ID,
        "source_sql_path": row["source_sql_path"],
        "schema_path": row["schema_path"],
        "witness_data_path": row["witness_data_path"],
        "generated_sql_path": row["generated_sql_path"],
        "row_metadata_path": row["expected_row_metadata_path"],
        "claim_boundary": CLAIM_BOUNDARY,
    }

    required_paths = [
        REPO_ROOT / row["source_sql_path"],
        REPO_ROOT / row["schema_path"],
        REPO_ROOT / row["witness_data_path"],
        REPO_ROOT / row["generated_sql_path"],
    ]
    if row["execution_status_planned"] != "ready_to_execute":
        observed = {
            "execution_status": "setup_failed",
            "consistency_status": "not_applicable",
            "error_type": "PlannedBlocked",
            "error_message": row["blocker_or_caveat"],
        }
    elif not all(path.is_file() for path in required_paths):
        observed = {
            "execution_status": "setup_failed",
            "consistency_status": "not_applicable",
            "error_type": "MissingInputArtifact",
            "error_message": "source_sql_or_schema_or_witness_or_generated_sql_missing",
        }
    elif row["engine"] == "mysql":
        observed = run_mysql_row(row)
    elif row["engine"] == "spark":
        observed = run_spark_row(row)
    else:
        observed = {
            "execution_status": "setup_failed",
            "consistency_status": "not_applicable",
            "error_type": "UnknownEngine",
            "error_message": f"Unknown engine: {row['engine']}",
        }

    metadata_payload = {**base_record, **observed}
    write_json(REPO_ROOT / row["expected_row_metadata_path"], metadata_payload)
    records.append(metadata_payload)

event_fields = [
    "run_id",
    "row_key",
    "case_id",
    "pool",
    "engine",
    "method_id",
    "route_id",
    "source_rewrite_run_id",
    "execution_denominator_id",
    "source_sql_path",
    "schema_path",
    "witness_data_path",
    "generated_sql_path",
    "execution_status",
    "consistency_status",
    "row_metadata_path",
    "claim_boundary",
]

with RUN_EVENT_LONG_CSV.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=event_fields)
    writer.writeheader()
    for record in records:
        writer.writerow({key: record.get(key, "") for key in event_fields})

counts_by_engine: dict[str, Counter[str]] = defaultdict(Counter)
counts_by_execution_status: Counter[str] = Counter()
counts_by_consistency_status: Counter[str] = Counter()
for record in records:
    counts_by_engine[record["engine"]][record["execution_status"]] += 1
    counts_by_execution_status[record["execution_status"]] += 1
    counts_by_consistency_status[record["consistency_status"]] += 1

payload = {
    "run_id": RUN_ID,
    "method_id": METHOD_ID,
    "route_id": ROUTE_ID,
    "source_rewrite_run_id": SOURCE_REWRITE_RUN_ID,
    "execution_denominator_id": EXECUTION_DENOMINATOR_ID,
    "planned_rows": len(rows),
    "counts_by_engine": {engine: dict(counter) for engine, counter in sorted(counts_by_engine.items())},
    "counts_by_execution_status": dict(counts_by_execution_status),
    "counts_by_consistency_status": dict(counts_by_consistency_status),
    "current_benchmark_metric_evidence": False,
    "claim_boundary": CLAIM_BOUNDARY,
    "records": records,
}

write_jsonl(RECORDS_JSONL, records)
write_json(RUN_RESULTS_JSON, payload)
PY

exit 0
