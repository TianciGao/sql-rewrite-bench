#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../../../../.." && pwd)"
RUN_DIR="${SCRIPT_DIR}"
FREEZE_DIR="${REPO_ROOT}/reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1"
PRELIGHT_CSV="${FREEZE_DIR}/calcite_hep_93_exact_timing_denominator_preflight_v1.csv"

if [[ "$(pwd)" != "${REPO_ROOT}" ]]; then
  echo "This script must be run from the repository root: ${REPO_ROOT}" >&2
  exit 1
fi

mkdir -p "${RUN_DIR}"

source "${REPO_ROOT}/scripts/env_postgres.sh"
source "${REPO_ROOT}/scripts/env_mysql.sh"
source "${REPO_ROOT}/scripts/env_spark.sh"

python - "$REPO_ROOT" "$RUN_DIR" "$FREEZE_DIR" "$PRELIGHT_CSV" <<'PY'
from __future__ import annotations

import csv
import json
import math
import os
import re
import shutil
import statistics
import subprocess
import sys
import tempfile
import time
import traceback
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(sys.argv[1])
RUN_DIR = Path(sys.argv[2])
FREEZE_DIR = Path(sys.argv[3])
PREFLIGHT_CSV = Path(sys.argv[4])

METHOD_ID = "calcite_hep"
PACKET_ROUTE_ID = "calcite_hep_93_exact_timing"
DENOMINATOR_ID = "common_core_v0_40_same_engine_calcite_hep_exact93_timing"
WARMUP_COUNT = 1
REPEAT_COUNT = 3
EXPECTED_ROWS = 93
RUNNER_USED = str(RUN_DIR / "run_manual_calcite_hep_93_exact_timing.sh")

LOG_DIR = RUN_DIR / "logs"
WORKSPACE_DIR = RUN_DIR / "workspaces"
TIMING_DIR = RUN_DIR / "timings"
TIMING_EVENT_LONG = RUN_DIR / "timing_event_long.csv"
TIMING_SUMMARY_CSV = RUN_DIR / "timing_summary.csv"
TIMING_SUMMARY_MD = RUN_DIR / "timing_summary.md"
RUN_RESULTS_JSON = RUN_DIR / "run_results.json"
VALIDATION_REPORT_JSON = RUN_DIR / "validation_report.json"
TIMING_COMMAND_MATRIX = RUN_DIR / "timing_command_matrix.csv"
TIMING_FAILURES_CSV = RUN_DIR / "timing_failures.csv"
README_MD = RUN_DIR / "README.md"
RESULT_CARD_CSV = FREEZE_DIR / "calcite_hep_93_exact_timing_result_card_v1.csv"
RESULT_CARD_MD = FREEZE_DIR / "calcite_hep_93_exact_timing_result_card_v1.md"

for path in [LOG_DIR, WORKSPACE_DIR, TIMING_DIR]:
    path.mkdir(parents=True, exist_ok=True)


def ensure_env() -> None:
    missing = []
    for key in ["PGHOST", "PGPORT", "PGDATABASE", "PGUSER", "PGPASSWORD"]:
        if not os.environ.get(key):
            missing.append(key)
    for key in ["MYSQL_HOST", "MYSQL_PORT", "MYSQL_DATABASE", "MYSQL_USER", "MYSQL_PASSWORD"]:
        if not os.environ.get(key):
            missing.append(key)
    for key in ["SPARK_LOCAL_IP", "SPARK_DRIVER_MEMORY"]:
        if not os.environ.get(key):
            missing.append(key)
    if missing:
        raise RuntimeError(f"Missing required timing environment variables: {', '.join(sorted(missing))}")


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in fieldnames})


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def csv_to_markdown(path: Path) -> str:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.reader(handle)
        rows = list(reader)
    if not rows:
        return ""
    header = rows[0]
    body = rows[1:]
    out = []
    out.append("| " + " | ".join(header) + " |")
    out.append("| " + " | ".join(["---"] * len(header)) + " |")
    for row in body:
        out.append("| " + " | ".join(row) + " |")
    return "\n".join(out)


def load_preflight_rows() -> list[dict[str, str]]:
    with PREFLIGHT_CSV.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    filtered = [
        row for row in rows
        if row["exact_match_retained"].lower() in {"true", "yes", "1"}
        and row["timing_ready"].lower() in {"true", "yes", "1"}
        and row["timing_readiness_status"] == "timing_ready"
    ]
    filtered.sort(key=lambda row: (row["case_id"], row["engine"]))
    return filtered


def pool_case_dir(pool: str, case_id: str) -> Path:
    return REPO_ROOT / "cases" / pool / case_id


ENGINE_TO_SCHEMA = {
    "pg": "ddl_pg.sql",
    "mysql": "ddl_mysql.sql",
    "spark": "ddl_spark.sql",
}

ENGINE_TO_WITNESS = {
    "pg": "pg_witness_data.sql",
    "mysql": "mysql_witness_data.sql",
    "spark": "spark_witness_data.sql",
}


def derive_schema_and_witness(row: dict[str, str]) -> tuple[Path, Path]:
    case_dir = pool_case_dir(row["pool"], row["case_id"])
    engine = row["engine"]
    schema = case_dir / "schema" / ENGINE_TO_SCHEMA[engine]
    witness = case_dir / "validation" / ENGINE_TO_WITNESS[engine]
    return schema, witness


def build_matrix_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    out = []
    for row in rows:
        rewrite_sql = row["rewrite_sql_artifact"]
        candidate_sql = row["candidate_sql_artifact"]
        selected_sql = rewrite_sql if rewrite_sql not in {"", "NA_not_found"} else candidate_sql
        if selected_sql in {"", "NA_not_found"}:
            raise RuntimeError(f"Missing rewrite or candidate SQL for {row['row_id']}")
        schema_path, witness_path = derive_schema_and_witness(row)
        if not schema_path.exists():
            raise RuntimeError(f"Missing schema artifact for {row['row_id']}: {schema_path}")
        if not witness_path.exists():
            raise RuntimeError(f"Missing witness artifact for {row['row_id']}: {witness_path}")
        source_sql = REPO_ROOT / row["source_sql_artifact"]
        rewrite_sql_path = REPO_ROOT / selected_sql
        if not source_sql.exists():
            raise RuntimeError(f"Missing source SQL for {row['row_id']}: {source_sql}")
        if not rewrite_sql_path.exists():
            raise RuntimeError(f"Missing rewrite SQL for {row['row_id']}: {rewrite_sql_path}")
        key = f"{row['case_id']}__{row['engine']}"
        out.append({
            "row_id": row["row_id"],
            "case_id": row["case_id"],
            "pool": row["pool"],
            "engine": row["engine"],
            "denominator_id": DENOMINATOR_ID,
            "method_id": METHOD_ID,
            "route_id": row["calcite_hep_route_id"],
            "source_sql_path": row["source_sql_artifact"],
            "rewrite_sql_path": selected_sql,
            "schema_path": str(schema_path.relative_to(REPO_ROOT)),
            "witness_data_path": str(witness_path.relative_to(REPO_ROOT)),
            "exact_match_source": row["exact_match_source"],
            "result_check_artifact": row["result_check_artifact"],
            "expected_timing_output_path": str((TIMING_DIR / row["case_id"] / row["engine"] / f"{PACKET_ROUTE_ID}.json").relative_to(REPO_ROOT)),
            "expected_stdout_log": str((LOG_DIR / f"{key}.stdout.log").relative_to(REPO_ROOT)),
            "expected_stderr_log": str((LOG_DIR / f"{key}.stderr.log").relative_to(REPO_ROOT)),
            "expected_workspace_dir": str((WORKSPACE_DIR / row["case_id"] / row["engine"]).relative_to(REPO_ROOT)),
            "warmup_count": str(WARMUP_COUNT),
            "repeat_count": str(REPEAT_COUNT),
            "source_artifacts": row["source_artifacts"],
            "notes": row["notes"],
        })
    return out


def make_schema_name(case_id: str, route_id: str) -> str:
    raw = f"ccv0_calcite_93_timing_{case_id.lower()}_{route_id.lower()}"
    return re.sub(r"[^a-z0-9_]", "_", raw)[:55]


def split_sql_script(sql_text: str) -> list[str]:
    statements = []
    current = []
    in_single = False
    in_double = False
    in_backtick = False
    in_line_comment = False
    in_block_comment = False
    i = 0
    while i < len(sql_text):
        ch = sql_text[i]
        nxt = sql_text[i + 1] if i + 1 < len(sql_text) else ""
        if in_line_comment:
            if ch == "\n":
                in_line_comment = False
                current.append(ch)
            i += 1
            continue
        if in_block_comment:
            if ch == "*" and nxt == "/":
                in_block_comment = False
                i += 2
                continue
            i += 1
            continue
        if not (in_single or in_double or in_backtick):
            if ch == "-" and nxt == "-":
                in_line_comment = True
                i += 2
                continue
            if ch == "/" and nxt == "*":
                in_block_comment = True
                i += 2
                continue
        if ch == "'" and not (in_double or in_backtick):
            if in_single and nxt == "'":
                current.extend([ch, nxt])
                i += 2
                continue
            in_single = not in_single
            current.append(ch)
            i += 1
            continue
        if ch == '"' and not (in_single or in_backtick):
            if in_double and nxt == '"':
                current.extend([ch, nxt])
                i += 2
                continue
            in_double = not in_double
            current.append(ch)
            i += 1
            continue
        if ch == "`" and not (in_single or in_double):
            in_backtick = not in_backtick
            current.append(ch)
            i += 1
            continue
        if ch == ";" and not (in_single or in_double or in_backtick):
            statement = "".join(current).strip()
            if statement:
                statements.append(statement)
            current = []
            i += 1
            continue
        current.append(ch)
        i += 1
    tail = "".join(current).strip()
    if tail:
        statements.append(tail)
    return statements


def load_single_query(query_path: Path, engine: str) -> str:
    statements = split_sql_script(query_path.read_text(encoding="utf-8"))
    if not statements:
        raise RuntimeError(f"No {engine} query detected in {query_path}")
    if len(statements) != 1:
        raise RuntimeError(f"Expected exactly one {engine} query in {query_path}, found {len(statements)}")
    return statements[0]


def extract_mysql_table_names(ddl_text: str) -> list[str]:
    pattern = re.compile(
        r"^\s*CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?(?:`([^`]+)`|([A-Za-z_][A-Za-z0-9_]*))",
        re.IGNORECASE | re.MULTILINE,
    )
    out: list[str] = []
    for match in pattern.finditer(ddl_text):
        name = match.group(1) or match.group(2)
        if name and name not in out:
            out.append(name)
    return out


def run_pg_timed_query(schema_name: str, schema_sql: Path, witness_sql: Path, query_sql: Path, stdout_handle, stderr_handle) -> float:
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


def run_mysql_timed_query(schema_sql: Path, witness_sql: Path, query_sql: Path) -> float:
    mysql_args = ["mysql"]
    if os.environ.get("MYSQL_HOST"):
        mysql_args.extend(["--host", os.environ["MYSQL_HOST"]])
    if os.environ.get("MYSQL_PORT"):
        mysql_args.extend(["--port", os.environ["MYSQL_PORT"]])
    if os.environ.get("MYSQL_USER"):
        mysql_args.extend(["--user", os.environ["MYSQL_USER"]])
    if os.environ.get("MYSQL_PASSWORD"):
        mysql_args.append(f"--password={os.environ['MYSQL_PASSWORD']}")
    mysql_database = os.environ.get("MYSQL_DATABASE", "bench")
    table_names = extract_mysql_table_names(schema_sql.read_text(encoding="utf-8"))
    if not table_names:
        raise RuntimeError(f"No MySQL table names detected in DDL: {schema_sql}")

    def cleanup_tables(check: bool) -> None:
        quoted = ", ".join(f"`{name.replace('`', '``')}`" for name in table_names)
        subprocess.run(mysql_args + [mysql_database, "-e", f"DROP TABLE IF EXISTS {quoted};"], check=check)

    start = time.perf_counter()
    try:
        cleanup_tables(check=True)
        for path in [schema_sql, witness_sql, query_sql]:
            subprocess.run(mysql_args + [mysql_database, "-e", f"source {path};"], check=True)
    finally:
        cleanup_tables(check=False)
    return (time.perf_counter() - start) * 1000.0


def run_spark_timed_query(case_id: str, route_id: str, workspace: Path, schema_sql: Path, witness_sql: Path, query_sql: Path) -> float:
    from pyspark.sql import SparkSession

    warehouse_dir = tempfile.mkdtemp(prefix=f"ccv0_calcite_hep_93_{case_id.lower()}_", dir=str(workspace))
    spark = (
        SparkSession.builder
        .master("local[*]")
        .appName(f"ccv0_calcite_hep_93_{case_id.lower()}_{route_id}")
        .config("spark.ui.enabled", "false")
        .config("spark.sql.shuffle.partitions", "1")
        .config("spark.sql.warehouse.dir", warehouse_dir)
        .getOrCreate()
    )
    try:
        start = time.perf_counter()
        for setup_path in [schema_sql, witness_sql]:
            for stmt in split_sql_script(setup_path.read_text(encoding="utf-8")):
                spark.sql(stmt).collect()
        spark.sql(load_single_query(query_sql, "spark")).collect()
        return (time.perf_counter() - start) * 1000.0
    finally:
        spark.stop()


def run_row(row: dict[str, str]) -> dict[str, object]:
    case_id = row["case_id"]
    pool = row["pool"]
    engine = row["engine"]
    route_id = row["route_id"]
    stdout_log = REPO_ROOT / row["expected_stdout_log"]
    stderr_log = REPO_ROOT / row["expected_stderr_log"]
    workspace_dir = REPO_ROOT / row["expected_workspace_dir"]
    timing_json_path = REPO_ROOT / row["expected_timing_output_path"]
    source_sql = REPO_ROOT / row["source_sql_path"]
    rewrite_sql = REPO_ROOT / row["rewrite_sql_path"]
    schema_path = REPO_ROOT / row["schema_path"]
    witness_path = REPO_ROOT / row["witness_data_path"]

    for path in [stdout_log.parent, stderr_log.parent, workspace_dir, timing_json_path.parent]:
        path.mkdir(parents=True, exist_ok=True)

    schema_copy = workspace_dir / schema_path.name
    witness_copy = workspace_dir / witness_path.name
    source_copy = workspace_dir / "source.sql"
    rewrite_copy = workspace_dir / "rewrite.sql"
    shutil.copyfile(schema_path, schema_copy)
    shutil.copyfile(witness_path, witness_copy)
    shutil.copyfile(source_sql, source_copy)
    shutil.copyfile(rewrite_sql, rewrite_copy)

    payload: dict[str, object] = {
        "row_id": row["row_id"],
        "case_id": case_id,
        "pool": pool,
        "engine": engine,
        "denominator_id": DENOMINATOR_ID,
        "method_id": METHOD_ID,
        "route_id": route_id,
        "warmup_count": WARMUP_COUNT,
        "repeat_count": REPEAT_COUNT,
        "source_runtime_ms_runs": [],
        "rewrite_runtime_ms_runs": [],
        "median_source_ms": None,
        "median_rewrite_ms": None,
        "speedup_ratio": None,
        "timing_status": "timing_failed",
        "timing_failure_type": "",
        "timing_failure_detail": "",
        "timing_json_path": row["expected_timing_output_path"],
        "stdout_log": row["expected_stdout_log"],
        "stderr_log": row["expected_stderr_log"],
        "source_sql_artifact": row["source_sql_path"],
        "rewrite_sql_artifact": row["rewrite_sql_path"],
        "exact_match_source": row["exact_match_source"],
        "result_check_artifact": row["result_check_artifact"],
        "source_artifacts": row["source_artifacts"],
        "notes": row["notes"],
    }

    with stdout_log.open("w", encoding="utf-8") as stdout_handle, stderr_log.open("w", encoding="utf-8") as stderr_handle:
        stdout_handle.write(f"row_id={row['row_id']} case_id={case_id} pool={pool} engine={engine} route_id={route_id}\n")
        stdout_handle.write(f"warmup_count={WARMUP_COUNT} repeat_count={REPEAT_COUNT}\n")
        try:
            if engine == "pg":
                schema_name = make_schema_name(case_id, route_id)
                for _ in range(WARMUP_COUNT):
                    run_pg_timed_query(schema_name, schema_copy, witness_copy, source_copy, stdout_handle, stderr_handle)
                    run_pg_timed_query(schema_name, schema_copy, witness_copy, rewrite_copy, stdout_handle, stderr_handle)
                for _ in range(REPEAT_COUNT):
                    payload["source_runtime_ms_runs"].append(
                        run_pg_timed_query(schema_name, schema_copy, witness_copy, source_copy, stdout_handle, stderr_handle)
                    )
                    payload["rewrite_runtime_ms_runs"].append(
                        run_pg_timed_query(schema_name, schema_copy, witness_copy, rewrite_copy, stdout_handle, stderr_handle)
                    )
            elif engine == "mysql":
                for _ in range(WARMUP_COUNT):
                    run_mysql_timed_query(schema_copy, witness_copy, source_copy)
                    run_mysql_timed_query(schema_copy, witness_copy, rewrite_copy)
                for _ in range(REPEAT_COUNT):
                    payload["source_runtime_ms_runs"].append(run_mysql_timed_query(schema_copy, witness_copy, source_copy))
                    payload["rewrite_runtime_ms_runs"].append(run_mysql_timed_query(schema_copy, witness_copy, rewrite_copy))
            elif engine == "spark":
                for _ in range(WARMUP_COUNT):
                    run_spark_timed_query(case_id, route_id, workspace_dir, schema_copy, witness_copy, source_copy)
                    run_spark_timed_query(case_id, route_id, workspace_dir, schema_copy, witness_copy, rewrite_copy)
                for _ in range(REPEAT_COUNT):
                    payload["source_runtime_ms_runs"].append(
                        run_spark_timed_query(case_id, route_id, workspace_dir, schema_copy, witness_copy, source_copy)
                    )
                    payload["rewrite_runtime_ms_runs"].append(
                        run_spark_timed_query(case_id, route_id, workspace_dir, schema_copy, witness_copy, rewrite_copy)
                    )
            else:
                raise RuntimeError(f"Unsupported engine {engine}")

            payload["median_source_ms"] = statistics.median(payload["source_runtime_ms_runs"])
            payload["median_rewrite_ms"] = statistics.median(payload["rewrite_runtime_ms_runs"])
            if payload["median_rewrite_ms"] and float(payload["median_rewrite_ms"]) > 0:
                payload["speedup_ratio"] = float(payload["median_source_ms"]) / float(payload["median_rewrite_ms"])
            payload["timing_status"] = "timing_success"
        except Exception as exc:
            payload["timing_failure_type"] = type(exc).__name__
            payload["timing_failure_detail"] = str(exc)
            traceback.print_exc(file=stderr_handle)

    write_json(timing_json_path, payload)
    return payload


def safe_num(value: object) -> str:
    if value is None:
        return "NA_not_computed"
    if isinstance(value, str):
        return value
    return f"{float(value):.12g}"


def summarize(records: list[dict[str, object]]) -> dict[str, object]:
    success = [r for r in records if r["timing_status"] == "timing_success"]
    failed = [r for r in records if r["timing_status"] != "timing_success"]
    summary: dict[str, object] = {
        "method_id": METHOD_ID,
        "route_id": PACKET_ROUTE_ID,
        "denominator_id": DENOMINATOR_ID,
        "planned_exact_rows": EXPECTED_ROWS,
        "timing_attempted_rows": len(records),
        "timing_success_rows": len(success),
        "timing_failed_rows": len(failed),
        "median_speedup": "NA_not_computed",
        "gm_speedup": "NA_not_computed",
        "win_count": "NA_not_computed",
        "tie_count": "NA_not_computed",
        "loss_count": "NA_not_computed",
        "regression_20pct_count": "NA_not_computed",
        "regression_rate_20pct": "NA_not_computed",
        "best_case_id": "NA_not_computed",
        "best_case_engine": "NA_not_computed",
        "best_case_speedup": "NA_not_computed",
        "worst_case_id": "NA_not_computed",
        "worst_case_engine": "NA_not_computed",
        "worst_case_speedup": "NA_not_computed",
        "claim_boundary": "Calcite HEP 93 exact-row correctness-gated timing only; not a new correctness result; not a final ranked leaderboard",
        "notes": "GM speedup and Regression@20 are computed only on timing_success rows. Existing PG-only 21-row timing evidence was not reused as the 93-row timing result.",
    }
    if success:
        speedups = [float(r["speedup_ratio"]) for r in success if r["speedup_ratio"] is not None]
        summary["median_speedup"] = safe_num(statistics.median(speedups))
        summary["gm_speedup"] = safe_num(math.exp(sum(math.log(x) for x in speedups) / len(speedups)))
        win_count = sum(1 for x in speedups if x > 1.05)
        tie_count = sum(1 for x in speedups if 0.95 <= x <= 1.05)
        loss_count = sum(1 for x in speedups if x < 0.95)
        regression_count = sum(1 for x in speedups if x < 0.8)
        summary["win_count"] = str(win_count)
        summary["tie_count"] = str(tie_count)
        summary["loss_count"] = str(loss_count)
        summary["regression_20pct_count"] = str(regression_count)
        summary["regression_rate_20pct"] = safe_num(regression_count / len(speedups))
        best = max(success, key=lambda r: float(r["speedup_ratio"]))
        worst = min(success, key=lambda r: float(r["speedup_ratio"]))
        summary["best_case_id"] = str(best["case_id"])
        summary["best_case_engine"] = str(best["engine"])
        summary["best_case_speedup"] = safe_num(best["speedup_ratio"])
        summary["worst_case_id"] = str(worst["case_id"])
        summary["worst_case_engine"] = str(worst["engine"])
        summary["worst_case_speedup"] = safe_num(worst["speedup_ratio"])
    return summary


def main() -> None:
    ensure_env()
    rows = load_preflight_rows()
    if len(rows) != EXPECTED_ROWS:
        raise RuntimeError(f"Expected {EXPECTED_ROWS} timing-ready rows, found {len(rows)}")
    matrix_rows = build_matrix_rows(rows)
    matrix_fields = [
        "row_id", "case_id", "pool", "engine", "denominator_id", "method_id", "route_id",
        "source_sql_path", "rewrite_sql_path", "schema_path", "witness_data_path",
        "exact_match_source", "result_check_artifact", "expected_timing_output_path",
        "expected_stdout_log", "expected_stderr_log", "expected_workspace_dir",
        "warmup_count", "repeat_count", "source_artifacts", "notes",
    ]
    write_csv(TIMING_COMMAND_MATRIX, matrix_fields, matrix_rows)

    records = [run_row(row) for row in matrix_rows]
    summary = summarize(records)

    event_rows = []
    failure_rows = []
    for record in records:
        success = record["timing_status"] == "timing_success"
        event_rows.append({
            "row_id": record["row_id"],
            "case_id": record["case_id"],
            "pool": record["pool"],
            "engine": record["engine"],
            "denominator_id": record["denominator_id"],
            "method_id": record["method_id"],
            "route_id": record["route_id"],
            "source_sql_artifact": record["source_sql_artifact"],
            "rewrite_sql_artifact": record["rewrite_sql_artifact"],
            "exact_match_retained": "true",
            "timing_attempted": "true",
            "timing_success": "true" if success else "false",
            "source_runtime_ms": safe_num(record["median_source_ms"]) if success else "NA_not_computed",
            "rewrite_runtime_ms": safe_num(record["median_rewrite_ms"]) if success else "NA_not_computed",
            "speedup_ratio": safe_num(record["speedup_ratio"]) if success else "NA_not_computed",
            "timing_failure_type": "" if success else str(record["timing_failure_type"]),
            "timing_failure_detail": "" if success else str(record["timing_failure_detail"]),
            "source_artifacts": f"{record['exact_match_source']}|{record['result_check_artifact']}|{record['source_artifacts']}",
            "notes": str(record["notes"]),
        })
        if not success:
            failure_rows.append({
                "row_id": record["row_id"],
                "case_id": record["case_id"],
                "engine": record["engine"],
                "failure_stage": "timing",
                "failure_type": record["timing_failure_type"],
                "failure_detail": record["timing_failure_detail"],
                "source_sql_artifact": record["source_sql_artifact"],
                "rewrite_sql_artifact": record["rewrite_sql_artifact"],
                "notes": record["notes"],
            })

    write_csv(
        TIMING_EVENT_LONG,
        [
            "row_id", "case_id", "pool", "engine", "denominator_id", "method_id", "route_id",
            "source_sql_artifact", "rewrite_sql_artifact", "exact_match_retained", "timing_attempted",
            "timing_success", "source_runtime_ms", "rewrite_runtime_ms", "speedup_ratio",
            "timing_failure_type", "timing_failure_detail", "source_artifacts", "notes",
        ],
        event_rows,
    )
    write_csv(
        TIMING_FAILURES_CSV,
        [
            "row_id", "case_id", "engine", "failure_stage", "failure_type", "failure_detail",
            "source_sql_artifact", "rewrite_sql_artifact", "notes",
        ],
        failure_rows,
    )
    write_csv(
        TIMING_SUMMARY_CSV,
        [
            "method_id", "route_id", "denominator_id", "planned_exact_rows", "timing_attempted_rows",
            "timing_success_rows", "timing_failed_rows", "median_speedup", "gm_speedup", "win_count",
            "tie_count", "loss_count", "regression_20pct_count", "regression_rate_20pct",
            "best_case_id", "best_case_engine", "best_case_speedup",
            "worst_case_id", "worst_case_engine", "worst_case_speedup",
            "claim_boundary", "notes",
        ],
        [summary],
    )

    success_rows = [r for r in records if r["timing_status"] == "timing_success"]
    validation_report = {
        "expected_denominator_rows": EXPECTED_ROWS,
        "input_preflight_path": str(PREFLIGHT_CSV.relative_to(REPO_ROOT)),
        "timing_event_long_rows": len(event_rows),
        "timing_attempted_rows": len(event_rows),
        "timing_success_rows": len(success_rows),
        "timing_failed_rows": len(event_rows) - len(success_rows),
        "unexpected_extra_rows": 0,
        "missing_denominator_rows": EXPECTED_ROWS - len(event_rows),
        "exact_match_rechecked_or_retained_policy": "retained_exact_match_only_no_checker_rerun",
        "timing_policy": {
            "warmup_count": WARMUP_COUNT,
            "repeat_count": REPEAT_COUNT,
            "speedup_ratio": "source_runtime_ms / rewrite_runtime_ms using row-local medians",
            "win_threshold": "> 1.05",
            "tie_threshold": "0.95 <= x <= 1.05",
            "loss_threshold": "< 0.95",
            "regression_20pct_threshold": "< 0.8",
        },
        "command_or_runner_used": RUNNER_USED,
        "status": "ok" if len(event_rows) == EXPECTED_ROWS else "failed",
    }
    write_json(VALIDATION_REPORT_JSON, validation_report)

    run_results = {
        "method_id": METHOD_ID,
        "route_id": PACKET_ROUTE_ID,
        "denominator_id": DENOMINATOR_ID,
        "planned_exact_rows": EXPECTED_ROWS,
        "warmup_count": WARMUP_COUNT,
        "repeat_count": REPEAT_COUNT,
        "counts_by_engine": dict(Counter(r["engine"] for r in records)),
        "counts_by_timing_status": dict(Counter(r["timing_status"] for r in records)),
        "summary": summary,
        "records": records,
    }
    write_json(RUN_RESULTS_JSON, run_results)

    TIMING_SUMMARY_MD.write_text(
        "# Calcite HEP 93 Exact Timing Summary\n\n"
        "This is a correctness-gated timing summary for the retained 93 exact-match Calcite HEP rows only.\n"
        "It is not a new correctness result and it is not a final ranked leaderboard.\n\n"
        + csv_to_markdown(TIMING_SUMMARY_CSV)
        + "\n\n## Interpretation notes\n\n"
        "- GM speedup and Regression@20 are computed only on timing_success rows.\n"
        "- Existing PG-only 21-row timing evidence was not reused as the 93-row timing result.\n",
        encoding="utf-8",
    )

    README_MD.write_text(
        "# Calcite HEP 93 Exact Timing Packet\n\n"
        "This run packet times exactly the 93 retained exact-match Calcite HEP rows listed in the preflight denominator.\n"
        "It does not regenerate Calcite rewrites, does not change the 93/120 correctness ledger, and does not create a final ranked leaderboard.\n\n"
        "## Inputs\n\n"
        f"- preflight denominator: `{PREFLIGHT_CSV.relative_to(REPO_ROOT)}`\n"
        f"- timing runner: `{Path(RUNNER_USED).relative_to(REPO_ROOT)}`\n"
        f"- warmup_count = {WARMUP_COUNT}\n"
        f"- repeat_count = {REPEAT_COUNT}\n\n"
        "## Outputs\n\n"
        "- `timing_event_long.csv`\n"
        "- `timing_summary.csv`\n"
        "- `timing_summary.md`\n"
        "- `run_results.json`\n"
        "- `validation_report.json`\n"
        "- `timing_command_matrix.csv`\n"
        "- `timing_failures.csv`\n\n"
        "## Boundary\n\n"
        "Existing Calcite HEP PG-only timing evidence was not reused as the 93-row timing result.\n",
        encoding="utf-8",
    )

    result_card_rows = [{
        **summary,
        "claim_boundary": "This is Calcite HEP 93 exact-row correctness-gated timing only. This is not a new correctness result and does not change the 93/120 fail-closed ledger. This is not a final ranked leaderboard.",
        "notes": "Existing PG-only 21-row timing evidence was not reused as the 93-row timing result. GM speedup and Regression@20 are based only on timing_success rows.",
        "source_artifacts": f"{RUN_DIR.relative_to(REPO_ROOT)}/timing_summary.csv|{RUN_DIR.relative_to(REPO_ROOT)}/timing_event_long.csv|{PREFLIGHT_CSV.relative_to(REPO_ROOT)}",
    }]
    write_csv(
        RESULT_CARD_CSV,
        [
            "method_id", "route_id", "denominator_id", "planned_exact_rows", "timing_attempted_rows",
            "timing_success_rows", "timing_failed_rows", "median_speedup", "gm_speedup", "win_count",
            "tie_count", "loss_count", "regression_20pct_count", "regression_rate_20pct",
            "best_case_id", "best_case_engine", "best_case_speedup",
            "worst_case_id", "worst_case_engine", "worst_case_speedup",
            "claim_boundary", "source_artifacts", "notes",
        ],
        result_card_rows,
    )
    RESULT_CARD_MD.write_text(
        "# Calcite HEP 93 Exact Timing Result Card\n\n"
        "This is Calcite HEP 93 exact-row correctness-gated timing.\n\n"
        "- This is not a new correctness result.\n"
        "- This does not change the 93/120 fail-closed correctness ledger.\n"
        "- This is not a final ranked leaderboard.\n"
        "- Existing PG-only 21-row timing evidence was not reused as the 93-row timing result.\n"
        "- GM speedup and Regression@20, if computed, are based only on timing_success rows.\n\n"
        + csv_to_markdown(RESULT_CARD_CSV)
        + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
PY
