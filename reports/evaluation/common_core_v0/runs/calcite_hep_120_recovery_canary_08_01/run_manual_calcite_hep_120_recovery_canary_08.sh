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

RUN_ID="calcite_hep_120_recovery_canary_08_01"
METHOD_ID="calcite_hep"
ROUTE_ID="calcite_hep_same_engine_rewrite"
DENOMINATOR_ID="common_core_v0_40_same_engine_120"
CLAIM_BOUNDARY="calcite_hep_120_recovery_canary_only_not_timing_speedup_or_leaderboard_evidence"

RUN_DIR="$REPO_ROOT/reports/evaluation/common_core_v0/runs/$RUN_ID"
MATRIX_PATH="$RUN_DIR/recovery_command_matrix.csv"
RUN_RESULTS_PATH="$RUN_DIR/run_results.json"
RUN_EVENT_LONG_PATH="$RUN_DIR/run_event_long.csv"
RECORDS_JSONL="$RUN_DIR/records.tmp.jsonl"

CALCITE_CHECKOUT_ROOT="${CALCITE_CHECKOUT_ROOT:-$REPO_ROOT/datasets/raw/calcite/calcite}"
CALCITE_WORK_ROOT="${CALCITE_WORK_ROOT:-/tmp/calcite-hep-120-recovery-canary-08-01}"
GRADLE_USER_HOME="${GRADLE_USER_HOME:-/tmp/calcite-gradle-home}"
WRAPPER_SRC="$RUN_DIR/wrapper_src/CalciteHepRecoveryCanary.java"
WRAPPER_CLASSES_DIR="$CALCITE_WORK_ROOT/classes"
WRAPPER_CLASSPATH_FILE="$CALCITE_WORK_ROOT/wrapper_classpath.txt"
MYSQL_DIALECT_SOURCE="$CALCITE_CHECKOUT_ROOT/core/src/main/java/org/apache/calcite/sql/dialect/MysqlSqlDialect.java"
SPARK_DIALECT_SOURCE="$CALCITE_CHECKOUT_ROOT/core/src/main/java/org/apache/calcite/sql/dialect/SparkSqlDialect.java"
PG_DIALECT_SOURCE="$CALCITE_CHECKOUT_ROOT/core/src/main/java/org/apache/calcite/sql/dialect/PostgresqlSqlDialect.java"

mkdir -p "$RUN_DIR" "$CALCITE_WORK_ROOT" "$WRAPPER_CLASSES_DIR"

echo "Human-run only."
echo "Codex must not execute this script."
echo "This package produces recovery-canary validity evidence only."
echo "It does not compute timing, speedup, or leaderboard artifacts."

source "$REPO_ROOT/scripts/env_postgres.sh"
source "$REPO_ROOT/scripts/env_mysql.sh"
source "$REPO_ROOT/scripts/env_spark.sh"

wrapper_compile_status="not_attempted"
wrapper_compile_blocker=""
pg_dialect_available="false"
mysql_dialect_available="false"
spark_dialect_available="false"

if [[ ! -f "$WRAPPER_SRC" ]]; then
  wrapper_compile_status="setup_failed"
  wrapper_compile_blocker="wrapper_source_missing:$WRAPPER_SRC"
elif [[ ! -d "$CALCITE_CHECKOUT_ROOT" ]]; then
  wrapper_compile_status="setup_failed"
  wrapper_compile_blocker="calcite_checkout_missing:$CALCITE_CHECKOUT_ROOT"
else
  [[ -f "$PG_DIALECT_SOURCE" ]] && pg_dialect_available="true"
  [[ -f "$MYSQL_DIALECT_SOURCE" ]] && mysql_dialect_available="true"
  [[ -f "$SPARK_DIALECT_SOURCE" ]] && spark_dialect_available="true"

  (
    cd "$CALCITE_CHECKOUT_ROOT"
    export GRADLE_USER_HOME
    ./gradlew :core:classes >/dev/null
  ) || {
    wrapper_compile_status="setup_failed"
    wrapper_compile_blocker="gradle_core_classes_failed"
  }

  if [[ "$wrapper_compile_status" != "setup_failed" ]]; then
    CLASSPATH_CORE="$CALCITE_CHECKOUT_ROOT/core/build/classes/java/main:$CALCITE_CHECKOUT_ROOT/core/build/resources/main:$CALCITE_CHECKOUT_ROOT/linq4j/build/classes/java/main"
    CLASSPATH_JARS="$(find "$GRADLE_USER_HOME/caches/modules-2/files-2.1" -name '*.jar' -print | sort | paste -sd: -)"
    if [[ -z "${CLASSPATH_JARS:-}" ]]; then
      wrapper_compile_status="setup_failed"
      wrapper_compile_blocker="calcite_cached_jars_missing"
    else
      FULL_CLASSPATH="$WRAPPER_CLASSES_DIR:$CLASSPATH_CORE:$CLASSPATH_JARS"
      printf '%s' "$FULL_CLASSPATH" > "$WRAPPER_CLASSPATH_FILE"
      if javac -cp "$CLASSPATH_CORE:$CLASSPATH_JARS" -d "$WRAPPER_CLASSES_DIR" "$WRAPPER_SRC"; then
        wrapper_compile_status="ok"
      else
        wrapper_compile_status="setup_failed"
        wrapper_compile_blocker="wrapper_compile_failed"
      fi
    fi
  fi
fi

python - <<'PY' "$REPO_ROOT" "$MATRIX_PATH" "$RUN_RESULTS_PATH" "$RUN_EVENT_LONG_PATH" "$RECORDS_JSONL" "$WRAPPER_CLASSPATH_FILE" "$RUN_ID" "$METHOD_ID" "$ROUTE_ID" "$DENOMINATOR_ID" "$CLAIM_BOUNDARY" "$wrapper_compile_status" "$wrapper_compile_blocker" "$pg_dialect_available" "$mysql_dialect_available" "$spark_dialect_available"
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
MATRIX_PATH = Path(sys.argv[2])
RUN_RESULTS_PATH = Path(sys.argv[3])
RUN_EVENT_LONG_PATH = Path(sys.argv[4])
RECORDS_JSONL = Path(sys.argv[5])
WRAPPER_CLASSPATH_FILE = Path(sys.argv[6])
RUN_ID = sys.argv[7]
METHOD_ID = sys.argv[8]
ROUTE_ID = sys.argv[9]
DENOMINATOR_ID = sys.argv[10]
CLAIM_BOUNDARY = sys.argv[11]
WRAPPER_COMPILE_STATUS = sys.argv[12]
WRAPPER_COMPILE_BLOCKER = sys.argv[13]
PG_DIALECT_AVAILABLE = sys.argv[14] == "true"
MYSQL_DIALECT_AVAILABLE = sys.argv[15] == "true"
SPARK_DIALECT_AVAILABLE = sys.argv[16] == "true"

PREVIOUS_LEDGER_NUM = 70
PREVIOUS_LEDGER_DEN = 120
MAX_LEDGER_AFTER = 78


def read_rows() -> list[dict[str, str]]:
    with MATRIX_PATH.open(newline="", encoding="utf-8") as handle:
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
    return {
        "exact_match": exact_match,
        "consistency_status": "match_exact" if exact_match else "mismatch",
    }


def write_df_tsv(rows: list[tuple[Any, ...]], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        for row in rows:
            values = []
            for value in row:
                values.append("NULL" if value is None else str(value))
            handle.write("\t".join(values) + "\n")


def copy_inputs(workspace: Path, row: dict[str, str], generated_sql_path: Path) -> dict[str, Path]:
    workspace.mkdir(parents=True, exist_ok=True)
    engine = row["engine"]
    copied = {
        "schema": workspace / f"ddl_{engine}.sql",
        "witness": workspace / f"{engine}_witness_data.sql",
        "source": workspace / "source.sql",
        "generated": workspace / "generated.sql",
    }
    shutil.copyfile(REPO_ROOT / row["schema_path"], copied["schema"])
    shutil.copyfile(REPO_ROOT / row["witness_data_path"], copied["witness"])
    shutil.copyfile(REPO_ROOT / row["source_sql_path"], copied["source"])
    shutil.copyfile(generated_sql_path, copied["generated"])
    return copied


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
        r"CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?(?:`([^`]+)`|\"([^\"]+)\"|([A-Za-z_][A-Za-z0-9_]*))",
        re.IGNORECASE,
    )
    table_names: list[str] = []
    for match in pattern.finditer(ddl_text):
        table_name = match.group(1) or match.group(2) or match.group(3)
        if table_name and table_name not in table_names:
            table_names.append(table_name)
    return table_names


def spark_read_statements(text: str) -> list[str]:
    cleaned = re.sub(r"(?m)--.*$", " ", text)
    cleaned = re.sub(r"(?s)/\*.*?\*/", " ", cleaned)
    return [stmt.strip() for stmt in cleaned.split(";") if stmt.strip()]


def detect_dialect_class(engine: str) -> str:
    if engine == "pg":
        return "org.apache.calcite.sql.dialect.PostgresqlSqlDialect"
    if engine == "mysql":
        return "org.apache.calcite.sql.dialect.MysqlSqlDialect"
    if engine == "spark":
        return "org.apache.calcite.sql.dialect.SparkSqlDialect"
    return ""


def dialect_available(engine: str) -> bool:
    return {
        "pg": PG_DIALECT_AVAILABLE,
        "mysql": MYSQL_DIALECT_AVAILABLE,
        "spark": SPARK_DIALECT_AVAILABLE,
    }.get(engine, False)


def run_rewrite(row: dict[str, str]) -> dict[str, Any]:
    generated_sql_path = REPO_ROOT / row["expected_generated_sql_path"]
    generated_sql_path.parent.mkdir(parents=True, exist_ok=True)
    stdout_log = REPO_ROOT / row["expected_generated_stdout_log"]
    stderr_log = REPO_ROOT / row["expected_generated_stderr_log"]
    stdout_log.parent.mkdir(parents=True, exist_ok=True)

    if WRAPPER_COMPILE_STATUS != "ok":
        return {
            "rewrite_status": "rewrite_failed",
            "failure_category": "wrapper_compile_failed",
            "blocker_reason": WRAPPER_COMPILE_BLOCKER,
            "dialect_class_used": detect_dialect_class(row["engine"]),
        }
    if not dialect_available(row["engine"]):
        return {
            "rewrite_status": "rewrite_failed",
            "failure_category": "target_dialect_unavailable",
            "blocker_reason": f"dialect_unavailable_for_engine:{row['engine']}",
            "dialect_class_used": detect_dialect_class(row["engine"]),
        }

    cmd = [
        "java",
        "-cp",
        WRAPPER_CLASSPATH_FILE.read_text(encoding="utf-8"),
        "CalciteHepRecoveryCanary",
        "--case-id",
        row["case_id"],
        "--engine",
        row["engine"],
        "--source-sql",
        str(REPO_ROOT / row["source_sql_path"]),
        "--ddl",
        str(REPO_ROOT / row["schema_path"]),
        "--output-sql",
        str(generated_sql_path),
    ]

    with stdout_log.open("w", encoding="utf-8") as stdout_handle, stderr_log.open("w", encoding="utf-8") as stderr_handle:
        proc = subprocess.run(cmd, cwd=REPO_ROOT, stdout=stdout_handle, stderr=stderr_handle, text=True)

    stdout_kv: dict[str, str] = {}
    for line in stdout_log.read_text(encoding="utf-8").splitlines():
        if "=" in line:
            k, v = line.split("=", 1)
            stdout_kv[k.strip()] = v.strip()

    if proc.returncode != 0:
        return {
            "rewrite_status": "rewrite_failed",
            "failure_category": stdout_kv.get("failure_category", "wrapper_command_failed"),
            "blocker_reason": stdout_kv.get("blocker_reason", f"wrapper_command_rc_{proc.returncode}"),
            "dialect_class_used": stdout_kv.get("dialect_class_used", detect_dialect_class(row["engine"])),
            "wrapper_stdout_kv": stdout_kv,
        }

    if not generated_sql_path.is_file() or not generated_sql_path.read_text(encoding="utf-8").strip():
        return {
            "rewrite_status": "rewrite_failed",
            "failure_category": stdout_kv.get("failure_category", "generated_sql_missing"),
            "blocker_reason": stdout_kv.get("blocker_reason", "nonempty_sql_not_written"),
            "dialect_class_used": stdout_kv.get("dialect_class_used", detect_dialect_class(row["engine"])),
            "wrapper_stdout_kv": stdout_kv,
        }

    return {
        "rewrite_status": "rewrite_success",
        "failure_category": "",
        "blocker_reason": "",
        "dialect_class_used": stdout_kv.get("dialect_class_used", detect_dialect_class(row["engine"])),
        "rewrite_changed": stdout_kv.get("rewrite_changed", ""),
        "wrapper_stdout_kv": stdout_kv,
    }


def run_pg_execution(row: dict[str, str], generated_sql_path: Path) -> dict[str, Any]:
    workspace = REPO_ROOT / row["expected_result_check_path"]
    workspace = workspace.parent
    copied = copy_inputs(workspace, row, generated_sql_path)
    source_out = REPO_ROOT / row["expected_source_tsv_path"]
    generated_out = REPO_ROOT / row["expected_generated_tsv_path"]
    result_check = REPO_ROOT / row["expected_result_check_path"]
    source_stdout = REPO_ROOT / row["expected_source_stdout_log"]
    source_stderr = REPO_ROOT / row["expected_source_stderr_log"]
    generated_stdout = REPO_ROOT / row["expected_generated_stdout_log"]
    generated_stderr = REPO_ROOT / row["expected_generated_stderr_log"]
    for path in [source_out.parent, source_stdout.parent, generated_stdout.parent]:
        path.mkdir(parents=True, exist_ok=True)

    schema_name = re.sub(r"[^a-z0-9_]", "_", f"ccv0_calcite_hep_recovery_{row['case_id'].lower()}")[:55]
    psql_base = ["psql", "-v", "ON_ERROR_STOP=1", "-X", "-q"]

    with source_stdout.open("w", encoding="utf-8") as source_stdout_handle, source_stderr.open("w", encoding="utf-8") as source_stderr_handle, generated_stdout.open("w", encoding="utf-8") as generated_stdout_handle, generated_stderr.open("w", encoding="utf-8") as generated_stderr_handle:
        try:
            subprocess.run(
                psql_base + ["-c", f"DROP SCHEMA IF EXISTS {schema_name} CASCADE; CREATE SCHEMA {schema_name};"],
                cwd=REPO_ROOT,
                check=True,
                stdout=source_stdout_handle,
                stderr=source_stderr_handle,
                text=True,
            )
            for sql_path in [copied["schema"], copied["witness"]]:
                subprocess.run(
                    psql_base + ["-c", f"SET search_path TO {schema_name};", "-f", str(sql_path)],
                    cwd=REPO_ROOT,
                    check=True,
                    stdout=source_stdout_handle,
                    stderr=source_stderr_handle,
                    text=True,
                )
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
                "execution_status": "setup_failed" if source_out.exists() is False and generated_out.exists() is False else "generated_execution_failed",
                "exact_match": False,
                "consistency_status": "not_applicable",
                "failure_category": "execution_failed",
                "blocker_reason": str(exc),
            }
        finally:
            subprocess.run(["psql", "-v", "ON_ERROR_STOP=0", "-X", "-q", "-c", f"DROP SCHEMA IF EXISTS {schema_name} CASCADE;"], cwd=REPO_ROOT, stdout=generated_stdout_handle, stderr=generated_stderr_handle, text=True)
        write_json(result_check, payload)
        return payload


def run_mysql_execution(row: dict[str, str], generated_sql_path: Path) -> dict[str, Any]:
    workspace = (REPO_ROOT / row["expected_result_check_path"]).parent
    copied = copy_inputs(workspace, row, generated_sql_path)
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
    if not db_name:
        payload = {
            "execution_status": "setup_failed",
            "exact_match": False,
            "consistency_status": "not_applicable",
            "failure_category": "missing_mysql_database_env",
            "blocker_reason": "MYSQL_DATABASE is not set",
        }
        write_json(result_check, payload)
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
    return payload


def run_spark_execution(row: dict[str, str], generated_sql_path: Path) -> dict[str, Any]:
    workspace = (REPO_ROOT / row["expected_result_check_path"]).parent
    copied = copy_inputs(workspace, row, generated_sql_path)
    source_out = REPO_ROOT / row["expected_source_tsv_path"]
    generated_out = REPO_ROOT / row["expected_generated_tsv_path"]
    result_check = REPO_ROOT / row["expected_result_check_path"]
    source_stdout = REPO_ROOT / row["expected_source_stdout_log"]
    source_stderr = REPO_ROOT / row["expected_source_stderr_log"]
    generated_stdout = REPO_ROOT / row["expected_generated_stdout_log"]
    generated_stderr = REPO_ROOT / row["expected_generated_stderr_log"]
    for path in [source_out.parent, source_stdout.parent, generated_stdout.parent]:
        path.mkdir(parents=True, exist_ok=True)

    warehouse_dir = Path(tempfile.mkdtemp(prefix=f"calcite_hep_recovery_{row['case_id'].lower()}_{row['engine']}_", dir="/tmp"))

    with source_stdout.open("w", encoding="utf-8") as source_stdout_handle, source_stderr.open("w", encoding="utf-8") as source_stderr_handle, generated_stdout.open("w", encoding="utf-8") as generated_stdout_handle, generated_stderr.open("w", encoding="utf-8") as generated_stderr_handle:
        spark = None
        try:
            from pyspark.sql import SparkSession

            spark = (
                SparkSession.builder
                .master("local[*]")
                .appName(f"ccv0_calcite_hep_recovery_{row['case_id'].lower()}_{row['engine']}")
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
                "exact_match": False,
                "consistency_status": "not_applicable",
                "failure_category": "spark_setup_failed",
                "blocker_reason": str(exc),
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
            source_rows = [tuple(r) for r in spark.sql(normalize_query_text(copied["source"].read_text(encoding="utf-8"))).collect()]
            write_df_tsv(source_rows, source_out)
            generated_rows = [tuple(r) for r in spark.sql(normalize_query_text(copied["generated"].read_text(encoding="utf-8"))).collect()]
            write_df_tsv(generated_rows, generated_out)
            compare = compare_tsv_outputs(source_out, generated_out)
            payload = {"execution_status": "executed", **compare}
        except Exception as exc:
            traceback.print_exc(file=generated_stderr_handle)
            payload = {
                "execution_status": "generated_execution_failed",
                "exact_match": False,
                "consistency_status": "not_applicable",
                "failure_category": "execution_failed",
                "blocker_reason": str(exc),
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

event_fields = [
    "row_key",
    "case_id",
    "pool",
    "engine",
    "previous_status",
    "attempted_recovery_family",
    "execution_status",
    "exact_match",
    "consistency_status",
    "recovered_exact",
    "failure_category",
    "blocker_reason",
    "source_sql_path",
    "schema_path",
    "witness_data_path",
    "generated_sql_path",
    "result_check_path",
    "claim_boundary",
]

for row in rows:
    base_record = {
        "row_key": row["row_key"],
        "case_id": row["case_id"],
        "pool": row["pool"],
        "engine": row["engine"],
        "method_id": METHOD_ID,
        "route_id": ROUTE_ID,
        "denominator_id": DENOMINATOR_ID,
        "previous_status": row["previous_status"],
        "attempted_recovery_family": row["attempted_recovery_family"],
        "source_sql_path": row["source_sql_path"],
        "schema_path": row["schema_path"],
        "witness_data_path": row["witness_data_path"],
        "generated_sql_path": row["expected_generated_sql_path"],
        "result_check_path": row["expected_result_check_path"],
        "row_metadata_path": row["expected_row_metadata_path"],
        "claim_boundary": CLAIM_BOUNDARY,
    }

    required = [
        REPO_ROOT / row["source_sql_path"],
        REPO_ROOT / row["schema_path"],
        REPO_ROOT / row["witness_data_path"],
    ]
    if not all(path.is_file() for path in required):
        observed = {
            "execution_status": "setup_failed",
            "exact_match": False,
            "consistency_status": "not_applicable",
            "recovered_exact": False,
            "failure_category": "missing_input_artifact",
            "blocker_reason": "source_or_schema_or_witness_missing",
        }
    else:
        rewrite = run_rewrite(row)
        generated_sql_path = REPO_ROOT / row["expected_generated_sql_path"]
        if rewrite["rewrite_status"] != "rewrite_success":
            observed = {
                "execution_status": "not_executed_rewrite_failed",
                "exact_match": False,
                "consistency_status": "not_applicable",
                "recovered_exact": False,
                "failure_category": rewrite["failure_category"],
                "blocker_reason": rewrite["blocker_reason"],
                "dialect_class_used": rewrite.get("dialect_class_used", ""),
                "wrapper_stdout_kv": rewrite.get("wrapper_stdout_kv", {}),
            }
        else:
            if row["engine"] == "pg":
                execution = run_pg_execution(row, generated_sql_path)
            elif row["engine"] == "mysql":
                execution = run_mysql_execution(row, generated_sql_path)
            elif row["engine"] == "spark":
                execution = run_spark_execution(row, generated_sql_path)
            else:
                execution = {
                    "execution_status": "setup_failed",
                    "exact_match": False,
                    "consistency_status": "not_applicable",
                    "failure_category": "unknown_engine",
                    "blocker_reason": row["engine"],
                }
            observed = {
                **execution,
                "recovered_exact": bool(execution.get("execution_status") == "executed" and execution.get("exact_match") is True),
                "failure_category": execution.get("failure_category", ""),
                "blocker_reason": execution.get("blocker_reason", ""),
                "dialect_class_used": rewrite.get("dialect_class_used", ""),
                "wrapper_stdout_kv": rewrite.get("wrapper_stdout_kv", {}),
            }

    metadata_payload = {**base_record, **observed}
    write_json(REPO_ROOT / row["expected_row_metadata_path"], metadata_payload)
    records.append(metadata_payload)

with RUN_EVENT_LONG_PATH.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=event_fields)
    writer.writeheader()
    for record in records:
        writer.writerow({key: record.get(key, "") for key in event_fields})

counts_by_execution_status = Counter(record["execution_status"] for record in records)
counts_by_consistency_status = Counter(record["consistency_status"] for record in records)
counts_by_engine: dict[str, Counter[str]] = defaultdict(Counter)
for record in records:
    counts_by_engine[record["engine"]][record["execution_status"]] += 1

recovered_exact_count = sum(1 for record in records if record["recovered_exact"])
payload = {
    "run_id": RUN_ID,
    "method_id": METHOD_ID,
    "route_id": ROUTE_ID,
    "denominator_id": DENOMINATOR_ID,
    "previous_fail_closed_exact_ledger": f"{PREVIOUS_LEDGER_NUM}/{PREVIOUS_LEDGER_DEN}",
    "planned_rows": len(rows),
    "recovered_exact_count": recovered_exact_count,
    "new_fail_closed_exact_ledger": f"{PREVIOUS_LEDGER_NUM + recovered_exact_count}/{PREVIOUS_LEDGER_DEN}",
    "maximum_possible_ledger_after_this_canary": f"{MAX_LEDGER_AFTER}/{PREVIOUS_LEDGER_DEN}",
    "counts_by_engine": {engine: dict(counter) for engine, counter in sorted(counts_by_engine.items())},
    "counts_by_execution_status": dict(counts_by_execution_status),
    "counts_by_consistency_status": dict(counts_by_consistency_status),
    "current_benchmark_metric_evidence": False,
    "timing_denominator_id": "NA_not_computed",
    "leaderboard_comparable": "no",
    "claim_boundary": CLAIM_BOUNDARY,
    "wrapper_compile_status": WRAPPER_COMPILE_STATUS,
    "wrapper_compile_blocker": WRAPPER_COMPILE_BLOCKER,
    "target_dialect_availability": {
        "pg": PG_DIALECT_AVAILABLE,
        "mysql": MYSQL_DIALECT_AVAILABLE,
        "spark": SPARK_DIALECT_AVAILABLE,
    },
    "records": records,
}

write_jsonl(RECORDS_JSONL, records)
write_json(RUN_RESULTS_PATH, payload)
PY

exit 0
