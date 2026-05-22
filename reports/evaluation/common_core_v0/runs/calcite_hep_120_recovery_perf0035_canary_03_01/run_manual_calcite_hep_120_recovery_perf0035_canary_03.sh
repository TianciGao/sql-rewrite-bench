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

if [[ "$(pwd)" != "$REPO_ROOT" ]]; then
  echo "This script must be run from the repository root: $REPO_ROOT" >&2
  exit 1
fi

RUN_ID="calcite_hep_120_recovery_perf0035_canary_03_01"
METHOD_ID="calcite_hep"
ROUTE_ID="calcite_hep_same_engine_rewrite"
DENOMINATOR_ID="common_core_v0_40_same_engine_120"
CLAIM_BOUNDARY="calcite_hep_120_recovery_perf0035_canary_only_not_timing_speedup_or_leaderboard_evidence"

RUN_DIR="$REPO_ROOT/reports/evaluation/common_core_v0/runs/$RUN_ID"
MATRIX_CSV="$RUN_DIR/recovery_command_matrix.csv"
RUN_RESULTS_JSON="$RUN_DIR/run_results.json"
RUN_EVENT_LONG_CSV="$RUN_DIR/run_event_long.csv"

mkdir -p "$RUN_DIR"

echo "Human-run only."
echo "Codex must not execute this script."
echo "This package produces recovery-canary validity evidence only."
echo "No timing."
echo "No speedup."
echo "No leaderboard."
echo "No full 120-row comparable claim."

source "$REPO_ROOT/scripts/env_postgres.sh"
source "$REPO_ROOT/scripts/env_mysql.sh"
source "$REPO_ROOT/scripts/env_spark.sh"

python - "$REPO_ROOT" "$RUN_DIR" "$MATRIX_CSV" "$RUN_RESULTS_JSON" "$RUN_EVENT_LONG_CSV" <<'PY'
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

RUN_ID = "calcite_hep_120_recovery_perf0035_canary_03_01"
METHOD_ID = "calcite_hep"
ROUTE_ID = "calcite_hep_same_engine_rewrite"
DENOMINATOR_ID = "common_core_v0_40_same_engine_120"
CLAIM_BOUNDARY = "calcite_hep_120_recovery_perf0035_canary_only_not_timing_speedup_or_leaderboard_evidence"
PREVIOUS_LEDGER = "90/120"
MAX_LEDGER_AFTER = "93/120"


def read_rows() -> list[dict[str, str]]:
    with MATRIX_CSV.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


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
        r"CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?(?:`([^`]+)`|([A-Za-z_][A-Za-z0-9_]*))",
        re.IGNORECASE,
    )
    table_names: list[str] = []
    for match in pattern.finditer(ddl_text):
        table_name = match.group(1) or match.group(2)
        if table_name and table_name not in table_names:
            table_names.append(table_name)
    return table_names


def copy_inputs_and_repair(workspace: Path, row: dict[str, str]) -> dict[str, Path]:
    workspace.mkdir(parents=True, exist_ok=True)
    repaired_generated = REPO_ROOT / row["expected_repaired_generated_sql_path"]
    repaired_generated.parent.mkdir(parents=True, exist_ok=True)
    engine = row["engine"]
    copied = {
        "schema": workspace / f"ddl_{engine}.sql",
        "witness": workspace / f"{engine}_witness_data.sql",
        "source": workspace / "source.sql",
        "generated": workspace / "generated.sql",
        "retained_generated": REPO_ROOT / row["retained_generated_sql_path"],
        "repaired_generated": repaired_generated,
    }
    shutil.copyfile(REPO_ROOT / row["schema_path"], copied["schema"])
    shutil.copyfile(REPO_ROOT / row["witness_data_path"], copied["witness"])
    shutil.copyfile(REPO_ROOT / row["source_sql_path"], copied["source"])
    retained_sql = copied["retained_generated"].read_text(encoding="utf-8")
    repaired_sql = repair_generated_sql(row["row_key"], retained_sql)
    copied["generated"].write_text(repaired_sql.rstrip() + ";\n", encoding="utf-8")
    copied["repaired_generated"].write_text(repaired_sql.rstrip() + ";\n", encoding="utf-8")
    return copied


def repair_generated_sql(row_key: str, sql: str) -> str:
    normalized = normalize_query_text(sql)
    if row_key == "PERF_0035:pg":
        inner = normalized.replace(
            '"sum_sales" - "avg_monthly_sales"\nFROM',
            '"sum_sales" - "avg_monthly_sales" AS "__calcite_helper_delta"\nFROM',
            1,
        )
        return f'''
SELECT "cc_name", "d_year", "d_moy",
CAST("avg_monthly_sales" AS DECIMAL(22, 16)) AS "avg_monthly_sales",
"sum_sales", "psum", "nsum"
FROM ({inner}) AS "__calcite_perf0035_pg"
ORDER BY "__calcite_helper_delta", "nsum"
LIMIT 100
'''.strip()
    if row_key == "PERF_0035:mysql":
        inner = normalized.replace(
            '`sum_sales` - `avg_monthly_sales`\nFROM',
            '`sum_sales` - `avg_monthly_sales` AS `__calcite_helper_delta`\nFROM',
            1,
        )
        return f'''
SELECT `cc_name`, `d_year`, `d_moy`,
CAST(`avg_monthly_sales` AS DECIMAL(22, 6)) AS `avg_monthly_sales`,
`sum_sales`, `psum`, `nsum`
FROM ({inner}) AS `__calcite_perf0035_mysql`
ORDER BY `__calcite_helper_delta`, `nsum`
LIMIT 100
'''.strip()
    if row_key == "PERF_0035:spark":
        inner = normalized.replace(
            '`sum_sales` - `avg_monthly_sales`\nFROM',
            '`sum_sales` - `avg_monthly_sales` AS `__calcite_helper_delta`\nFROM',
            1,
        )
        return f'''
SELECT `cc_name`, `d_year`, `d_moy`,
CAST(`avg_monthly_sales` AS DECIMAL(22, 6)) AS `avg_monthly_sales`,
`sum_sales`, `psum`, `nsum`
FROM ({inner}) `__calcite_perf0035_spark`
ORDER BY `__calcite_helper_delta`, `nsum`
LIMIT 100
'''.strip()
    raise ValueError(f"unsupported row for repair: {row_key}")


def run_pg_row(row: dict[str, str]) -> dict[str, Any]:
    workspace = REPO_ROOT / row["expected_workspace_dir"]
    copied = copy_inputs_and_repair(workspace, row)
    source_out = REPO_ROOT / row["expected_source_tsv_path"]
    generated_out = REPO_ROOT / row["expected_generated_tsv_path"]
    result_check = REPO_ROOT / row["expected_result_check_path"]
    source_stdout = REPO_ROOT / row["expected_source_stdout_log"]
    source_stderr = REPO_ROOT / row["expected_source_stderr_log"]
    generated_stdout = REPO_ROOT / row["expected_generated_stdout_log"]
    generated_stderr = REPO_ROOT / row["expected_generated_stderr_log"]
    for path in [source_out.parent, source_stdout.parent, generated_stdout.parent]:
        path.mkdir(parents=True, exist_ok=True)

    schema_name = f"ccv0_calcite_hep_perf0035_{row['engine']}"[:55]
    psql_base = ["psql", "-v", "ON_ERROR_STOP=1", "-X", "-q"]

    with source_stdout.open("w", encoding="utf-8") as source_stdout_handle, source_stderr.open("w", encoding="utf-8") as source_stderr_handle, generated_stdout.open("w", encoding="utf-8") as generated_stdout_handle, generated_stderr.open("w", encoding="utf-8") as generated_stderr_handle:
        try:
            subprocess.run(psql_base + ["-c", f"DROP SCHEMA IF EXISTS {schema_name} CASCADE; CREATE SCHEMA {schema_name};"], cwd=REPO_ROOT, check=True, stdout=source_stdout_handle, stderr=source_stderr_handle, text=True)
            for sql_path in [copied["schema"], copied["witness"]]:
                subprocess.run(psql_base + ["-c", f"SET search_path TO {schema_name};", "-f", str(sql_path)], cwd=REPO_ROOT, check=True, stdout=source_stdout_handle, stderr=source_stderr_handle, text=True)
            source_query = normalize_query_text(copied["source"].read_text(encoding="utf-8"))
            generated_query = normalize_query_text(copied["generated"].read_text(encoding="utf-8"))
            source_copy = f"COPY ({source_query}) TO STDOUT WITH (FORMAT CSV, DELIMITER E'\\t', NULL 'NULL');"
            generated_copy = f"COPY ({generated_query}) TO STDOUT WITH (FORMAT CSV, DELIMITER E'\\t', NULL 'NULL');"
            with source_out.open("w", encoding="utf-8") as handle:
                subprocess.run(psql_base + ["-c", f"SET search_path TO {schema_name};", "-c", source_copy], cwd=REPO_ROOT, check=True, stdout=handle, stderr=source_stderr_handle, text=True)
            with generated_out.open("w", encoding="utf-8") as handle:
                subprocess.run(psql_base + ["-c", f"SET search_path TO {schema_name};", "-c", generated_copy], cwd=REPO_ROOT, check=True, stdout=handle, stderr=generated_stderr_handle, text=True)
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
            subprocess.run(["psql", "-v", "ON_ERROR_STOP=0", "-X", "-q", "-c", f"DROP SCHEMA IF EXISTS {schema_name} CASCADE;"], cwd=REPO_ROOT, stdout=generated_stdout_handle, stderr=generated_stderr_handle, text=True)

    write_json(result_check, payload)
    return payload


def run_mysql_row(row: dict[str, str]) -> dict[str, Any]:
    workspace = REPO_ROOT / row["expected_workspace_dir"]
    copied = copy_inputs_and_repair(workspace, row)
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
        payload = {"execution_status": "executed", **compare}
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
    cleaned = []
    for line in text.splitlines():
        if line.lstrip().startswith("--"):
            continue
        cleaned.append(line)
    joined = "\n".join(cleaned)
    return [stmt.strip() for stmt in joined.split(";") if stmt.strip()]


def spark_write_df(df: Any, output_path: Path) -> None:
    rows = df.collect()
    with output_path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write("\t".join("NULL" if value is None else str(value) for value in row) + "\n")


def run_spark_row(row: dict[str, str]) -> dict[str, Any]:
    workspace = REPO_ROOT / row["expected_workspace_dir"]
    copied = copy_inputs_and_repair(workspace, row)
    source_out = REPO_ROOT / row["expected_source_tsv_path"]
    generated_out = REPO_ROOT / row["expected_generated_tsv_path"]
    result_check = REPO_ROOT / row["expected_result_check_path"]
    source_stdout = REPO_ROOT / row["expected_source_stdout_log"]
    source_stderr = REPO_ROOT / row["expected_source_stderr_log"]
    generated_stdout = REPO_ROOT / row["expected_generated_stdout_log"]
    generated_stderr = REPO_ROOT / row["expected_generated_stderr_log"]
    for path in [source_out.parent, source_stdout.parent, generated_stdout.parent]:
        path.mkdir(parents=True, exist_ok=True)

    warehouse_dir = Path(tempfile.mkdtemp(prefix=f"calcite_hep_perf0035_{row['engine']}_", dir="/tmp"))

    with source_stdout.open("w", encoding="utf-8") as source_stdout_handle, source_stderr.open("w", encoding="utf-8") as source_stderr_handle, generated_stdout.open("w", encoding="utf-8") as generated_stdout_handle, generated_stderr.open("w", encoding="utf-8") as generated_stderr_handle:
        spark = None
        try:
            from pyspark.sql import SparkSession
            spark = (
                SparkSession.builder
                .master("local[*]")
                .appName(f"ccv0_calcite_hep_perf0035_{row['engine']}")
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
            payload = {"execution_status": "executed", **compare}
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
    base = {
        "run_id": RUN_ID,
        "row_key": row["row_key"],
        "case_id": row["case_id"],
        "pool": row["pool"],
        "engine": row["engine"],
        "method_id": METHOD_ID,
        "route_id": ROUTE_ID,
        "denominator_id": DENOMINATOR_ID,
        "previous_fail_closed_exact_ledger": PREVIOUS_LEDGER,
        "attempted_recovery_family": row["attempted_recovery_family"],
        "source_sql_path": row["source_sql_path"],
        "schema_path": row["schema_path"],
        "witness_data_path": row["witness_data_path"],
        "retained_generated_sql_path": row["retained_generated_sql_path"],
        "repaired_generated_sql_path": row["expected_repaired_generated_sql_path"],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    required = [
        REPO_ROOT / row["source_sql_path"],
        REPO_ROOT / row["schema_path"],
        REPO_ROOT / row["witness_data_path"],
        REPO_ROOT / row["retained_generated_sql_path"],
    ]
    if not all(path.is_file() for path in required):
        observed = {
            "execution_status": "setup_failed",
            "consistency_status": "not_applicable",
            "recovered_exact": False,
            "failure_category": "missing_input_artifact",
            "blocker_reason": "source_sql_or_schema_or_witness_or_retained_generated_sql_missing",
        }
    elif row["engine"] == "pg":
        observed = run_pg_row(row)
    elif row["engine"] == "mysql":
        observed = run_mysql_row(row)
    elif row["engine"] == "spark":
        observed = run_spark_row(row)
    else:
        observed = {
            "execution_status": "setup_failed",
            "consistency_status": "not_applicable",
            "recovered_exact": False,
            "failure_category": "unknown_engine",
            "blocker_reason": f"Unknown engine: {row['engine']}",
        }

    observed["recovered_exact"] = bool(
        observed.get("execution_status") == "executed" and
        observed.get("consistency_status") == "match_exact"
    )
    record = {**base, **observed, "row_metadata_path": row["expected_row_metadata_path"]}
    write_json(REPO_ROOT / row["expected_row_metadata_path"], record)
    records.append(record)

event_fields = [
    "run_id","row_key","case_id","pool","engine","method_id","route_id",
    "denominator_id","previous_fail_closed_exact_ledger","attempted_recovery_family",
    "execution_status","consistency_status","recovered_exact","row_metadata_path","claim_boundary"
]

with RUN_EVENT_LONG_CSV.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=event_fields)
    writer.writeheader()
    for record in records:
        writer.writerow({key: record.get(key, "") for key in event_fields})

recovered_exact_count = sum(1 for record in records if record.get("recovered_exact"))
counts_by_engine: dict[str, Counter[str]] = defaultdict(Counter)
counts_by_execution_status: Counter[str] = Counter()
counts_by_consistency_status: Counter[str] = Counter()
for record in records:
    counts_by_engine[record["engine"]][record["execution_status"]] += 1
    counts_by_consistency_status[record["consistency_status"]] += 1
    counts_by_execution_status[record["execution_status"]] += 1

ledger_num = 90 + recovered_exact_count
payload = {
    "run_id": RUN_ID,
    "method_id": METHOD_ID,
    "route_id": ROUTE_ID,
    "denominator_id": DENOMINATOR_ID,
    "previous_fail_closed_exact_ledger": PREVIOUS_LEDGER,
    "planned_rows": len(rows),
    "recovered_exact_count": recovered_exact_count,
    "new_fail_closed_exact_ledger": f"{ledger_num}/120",
    "maximum_possible_ledger_after_this_canary": MAX_LEDGER_AFTER,
    "counts_by_engine": {engine: dict(counter) for engine, counter in sorted(counts_by_engine.items())},
    "counts_by_execution_status": dict(counts_by_execution_status),
    "counts_by_consistency_status": dict(counts_by_consistency_status),
    "current_benchmark_metric_evidence": False,
    "timing_denominator_id": "NA_not_computed",
    "leaderboard_comparable": "no",
    "claim_boundary": CLAIM_BOUNDARY,
    "records": records,
}
write_json(RUN_RESULTS_JSON, payload)
PY

exit 0
