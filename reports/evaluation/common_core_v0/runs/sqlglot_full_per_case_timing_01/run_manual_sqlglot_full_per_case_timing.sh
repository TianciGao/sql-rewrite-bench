#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../../../../.." && pwd)"
RUN_DIR="${SCRIPT_DIR}"
FREEZE_DIR="${REPO_ROOT}/reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1"
DENOM_CSV="${FREEZE_DIR}/sqlglot_timing_denominator_after_backfill_v1.csv"
BACKFILL_SUMMARY_CSV="${FREEZE_DIR}/sqlglot_result_check_backfill_summary_v1.csv"

if [[ "$(pwd)" != "${REPO_ROOT}" ]]; then
  echo "This script must be run from the repository root: ${REPO_ROOT}" >&2
  exit 1
fi

mkdir -p "${RUN_DIR}"

source "${REPO_ROOT}/scripts/env_postgres.sh"
source "${REPO_ROOT}/scripts/env_mysql.sh"
source "${REPO_ROOT}/scripts/env_spark.sh"

python - "$REPO_ROOT" "$RUN_DIR" "$FREEZE_DIR" "$DENOM_CSV" "$BACKFILL_SUMMARY_CSV" <<'PY'
from __future__ import annotations

import csv
import json
import math
import os
import re
import shutil
import statistics
import sys
import tempfile
import time
import traceback
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

import psycopg
import pymysql
from pyspark.sql import SparkSession

REPO_ROOT = Path(sys.argv[1])
RUN_DIR = Path(sys.argv[2])
FREEZE_DIR = Path(sys.argv[3])
DENOM_CSV = Path(sys.argv[4])
BACKFILL_SUMMARY_CSV = Path(sys.argv[5])

METHOD_ID = "sqlglot"
DENOMINATOR_ID = "common_core_v0_40_same_engine_120"
WARMUP_COUNT = 1
REPEAT_COUNT = 3
QUERY_TIMEOUT_SECONDS = 30
ROUTES = {
    "sqlglot_transpile_same_dialect_noop": {
        "timing_denominator_id": "sqlglot_transpile_same_dialect_noop_exact72_timing",
        "expected_rows": 72,
    },
    "sqlglot_optimize_same_dialect": {
        "timing_denominator_id": "sqlglot_optimize_same_dialect_exact63_timing",
        "expected_rows": 63,
    },
}
EXCLUDED_ROW_IDS = {
    "sqlglot_optimize_same_dialect__PORT_0003__pg__port_exec_only",
    "sqlglot_optimize_same_dialect__PORT_0004__mysql__port_exec_only",
}

README_MD = RUN_DIR / "README.md"
POLICY_MD = RUN_DIR / "timing_policy_v1.md"
COMMAND_MATRIX_CSV = RUN_DIR / "timing_command_matrix.csv"
TIMING_EVENT_LONG_CSV = RUN_DIR / "timing_event_long.csv"
TIMING_FAILURES_CSV = RUN_DIR / "timing_failures.csv"
TIMING_SUMMARY_CSV = RUN_DIR / "timing_summary.csv"
TIMING_SUMMARY_MD = RUN_DIR / "timing_summary.md"
RUN_RESULTS_JSON = RUN_DIR / "run_results.json"
VALIDATION_REPORT_JSON = RUN_DIR / "validation_report.json"
TIMINGS_DIR = RUN_DIR / "timings"
LOGS_DIR = RUN_DIR / "logs"
RESULT_CARD_CSV = FREEZE_DIR / "sqlglot_full_per_case_timing_result_card_v1.csv"
RESULT_CARD_MD = FREEZE_DIR / "sqlglot_full_per_case_timing_result_card_v1.md"

for path in [TIMINGS_DIR, LOGS_DIR]:
    path.mkdir(parents=True, exist_ok=True)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in fieldnames})


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


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
        out.append("| " + " | ".join(str(cell).replace("|", "\\|") for cell in row) + " |")
    return "\n".join(out)


def strip_comment_lines(text: str) -> str:
    lines: list[str] = []
    for line in text.splitlines():
        if re.match(r"^\s*--", line):
            continue
        lines.append(line)
    return "\n".join(lines)


def read_statements(path: Path) -> list[str]:
    text = strip_comment_lines(path.read_text(encoding="utf-8"))
    return [stmt.strip() for stmt in text.split(";") if stmt.strip()]


def read_query(path: Path) -> str:
    return strip_comment_lines(path.read_text(encoding="utf-8")).strip().rstrip(";")


def tsv_cell(value) -> str:
    if value is None:
        return r"\N"
    return str(value)


def rows_to_lines(rows) -> list[str]:
    return ["\t".join(tsv_cell(cell) for cell in row) for row in rows]


def witness_path(case_id: str, pool: str, engine: str) -> Path:
    pool_dir = {
        "performance": "PERF",
        "consistency": "CONS",
        "longtail": "LONGTAIL",
        "portability": "PORT",
    }[pool]
    case_root = REPO_ROOT / "cases" / pool_dir / case_id
    candidates = [
        case_root / "validation" / f"{engine}_witness_data.sql",
        case_root / "validation" / f"load_witness_{engine}.sql",
    ]
    for path in candidates:
        if path.exists():
            return path
    raise FileNotFoundError(f"Missing witness data for {case_id}:{engine}")


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def load_timing_rows() -> list[dict[str, str]]:
    rows = read_csv_rows(DENOM_CSV)
    filtered = [
        row for row in rows
        if row["timing_ready"].lower() in {"true", "yes", "1"}
        and row["exact_match_after_backfill"].lower() in {"true", "yes", "1"}
        and row["route_id"] in ROUTES
        and row["row_id"] not in EXCLUDED_ROW_IDS
    ]
    filtered.sort(key=lambda row: (row["route_id"], row["case_id"], row["engine"]))
    return filtered


def load_backfill_summary() -> dict[str, dict[str, str]]:
    rows = read_csv_rows(BACKFILL_SUMMARY_CSV)
    return {row["route_id"]: row for row in rows}


def ensure_env() -> None:
    missing: list[str] = []
    for key in ["PGHOST", "PGPORT", "PGDATABASE", "PGUSER", "PGPASSWORD"]:
        if not os.environ.get(key):
            missing.append(key)
    for key in ["MYSQL_HOST", "MYSQL_PORT", "MYSQL_DATABASE", "MYSQL_USER", "MYSQL_PASSWORD"]:
        if not os.environ.get(key):
            missing.append(key)
    if not os.environ.get("SPARK_DRIVER_MEMORY"):
        missing.append("SPARK_DRIVER_MEMORY")
    if missing:
        raise RuntimeError(f"Missing required timing environment variables: {', '.join(sorted(missing))}")


def mysql_objects_from_ddl(ddl_path: Path) -> tuple[list[tuple[str, str]], list[str]]:
    stmts = read_statements(ddl_path)
    objects: list[tuple[str, str]] = []
    for stmt in stmts:
        match = re.match(r"(?is)^\s*CREATE\s+(TABLE|VIEW)\s+(IF\s+NOT\s+EXISTS\s+)?(`?)([A-Za-z0-9_]+)\3", stmt)
        if match:
            objects.append((match.group(1).upper(), match.group(4)))
    return objects, stmts


def run_pg_timing(source_sql_path: Path, candidate_sql_path: Path, ddl_path: Path, witness_sql_path: Path, row_id: str) -> dict[str, object]:
    schema_name = re.sub(r"[^a-z0-9_]", "_", f"sqlglot_timing_{row_id.lower()}")[:55]
    payload: dict[str, object] = {
        "source_runtime_ms": [],
        "rewrite_runtime_ms": [],
        "median_source_ms": None,
        "median_rewrite_ms": None,
        "speedup_ratio": None,
        "status": "failure",
        "notes": "",
    }
    with psycopg.connect(
        host=os.environ["PGHOST"],
        port=os.environ["PGPORT"],
        dbname=os.environ["PGDATABASE"],
        user=os.environ["PGUSER"],
        password=os.environ.get("PGPASSWORD"),
        autocommit=False,
    ) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT set_config('statement_timeout', %s, false)", (str(QUERY_TIMEOUT_SECONDS * 1000),))

            def run_query(query_path: Path) -> float:
                start = time.perf_counter()
                try:
                    cur.execute(psycopg.sql.SQL("CREATE SCHEMA {}").format(psycopg.sql.Identifier(schema_name)))
                    cur.execute(psycopg.sql.SQL("SET search_path TO {}, public").format(psycopg.sql.Identifier(schema_name)))
                    for stmt in read_statements(ddl_path):
                        cur.execute(stmt)
                    for stmt in read_statements(witness_sql_path):
                        cur.execute(stmt)
                    cur.execute(read_query(query_path))
                    if cur.description is not None:
                        cur.fetchall()
                finally:
                    conn.rollback()
                return (time.perf_counter() - start) * 1000.0

            for _ in range(WARMUP_COUNT):
                run_query(source_sql_path)
                run_query(candidate_sql_path)
            for _ in range(REPEAT_COUNT):
                payload["source_runtime_ms"].append(run_query(source_sql_path))
                payload["rewrite_runtime_ms"].append(run_query(candidate_sql_path))

    payload["median_source_ms"] = statistics.median(payload["source_runtime_ms"])
    payload["median_rewrite_ms"] = statistics.median(payload["rewrite_runtime_ms"])
    if payload["median_rewrite_ms"] and payload["median_rewrite_ms"] > 0:
        payload["speedup_ratio"] = payload["median_source_ms"] / payload["median_rewrite_ms"]
        payload["status"] = "success"
    else:
        payload["status"] = "failure"
        payload["notes"] = "rewrite median was zero"
    return payload


def run_mysql_timing(source_sql_path: Path, candidate_sql_path: Path, ddl_path: Path, witness_sql_path: Path) -> dict[str, object]:
    objects, ddl_statements = mysql_objects_from_ddl(ddl_path)
    payload: dict[str, object] = {
        "source_runtime_ms": [],
        "rewrite_runtime_ms": [],
        "median_source_ms": None,
        "median_rewrite_ms": None,
        "speedup_ratio": None,
        "status": "failure",
        "notes": "",
    }
    conn = pymysql.connect(
        host=os.environ["MYSQL_HOST"],
        port=int(os.environ["MYSQL_PORT"]),
        user=os.environ["MYSQL_USER"],
        password=os.environ["MYSQL_PASSWORD"],
        database=os.environ["MYSQL_DATABASE"],
        charset="utf8mb4",
        autocommit=True,
        read_timeout=QUERY_TIMEOUT_SECONDS,
        write_timeout=QUERY_TIMEOUT_SECONDS,
    )
    try:
        with conn.cursor() as cur:
            cur.execute(f"USE `{os.environ['MYSQL_DATABASE']}`")

            def cleanup_objects() -> None:
                for obj_type, name in reversed(objects):
                    cur.execute(f"DROP {obj_type} IF EXISTS `{name}`")

            def run_query(query_path: Path) -> float:
                cleanup_objects()
                for stmt in ddl_statements:
                    cur.execute(stmt)
                for stmt in read_statements(witness_sql_path):
                    cur.execute(stmt)
                start = time.perf_counter()
                cur.execute(read_query(query_path))
                cur.fetchall()
                elapsed = (time.perf_counter() - start) * 1000.0
                cleanup_objects()
                return elapsed

            for _ in range(WARMUP_COUNT):
                run_query(source_sql_path)
                run_query(candidate_sql_path)
            for _ in range(REPEAT_COUNT):
                payload["source_runtime_ms"].append(run_query(source_sql_path))
                payload["rewrite_runtime_ms"].append(run_query(candidate_sql_path))
    finally:
        conn.close()

    payload["median_source_ms"] = statistics.median(payload["source_runtime_ms"])
    payload["median_rewrite_ms"] = statistics.median(payload["rewrite_runtime_ms"])
    if payload["median_rewrite_ms"] and payload["median_rewrite_ms"] > 0:
        payload["speedup_ratio"] = payload["median_source_ms"] / payload["median_rewrite_ms"]
        payload["status"] = "success"
    else:
        payload["status"] = "failure"
        payload["notes"] = "rewrite median was zero"
    return payload


def run_spark_timing(source_sql_path: Path, candidate_sql_path: Path, ddl_path: Path, witness_sql_path: Path, row_id: str) -> dict[str, object]:
    warehouse_dir = Path(tempfile.mkdtemp(prefix=f"{row_id.lower()}_spark_sqlglot_timing_"))
    payload: dict[str, object] = {
        "source_runtime_ms": [],
        "rewrite_runtime_ms": [],
        "median_source_ms": None,
        "median_rewrite_ms": None,
        "speedup_ratio": None,
        "status": "failure",
        "notes": "",
    }
    spark = (
        SparkSession.builder.master("local[*]")
        .appName(f"{row_id}_sqlglot_timing")
        .config("spark.ui.enabled", "false")
        .config("spark.sql.session.timeZone", "UTC")
        .config("spark.sql.shuffle.partitions", "1")
        .config("spark.sql.warehouse.dir", str(warehouse_dir))
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("ERROR")

    db_name = re.sub(r"[^a-z0-9_]", "_", f"sqlglot_timing_{row_id.lower()}")[:55]
    try:
        def run_query(query_path: Path) -> float:
            spark.sql(f"CREATE DATABASE IF NOT EXISTS {db_name}")
            spark.sql(f"USE {db_name}")
            for stmt in read_statements(ddl_path):
                spark.sql(stmt)
            for stmt in read_statements(witness_sql_path):
                spark.sql(stmt)
            start = time.perf_counter()
            spark.sql(read_query(query_path)).collect()
            elapsed = (time.perf_counter() - start) * 1000.0
            spark.sql("USE default")
            spark.sql(f"DROP DATABASE IF EXISTS {db_name} CASCADE")
            return elapsed

        for _ in range(WARMUP_COUNT):
            run_query(source_sql_path)
            run_query(candidate_sql_path)
        for _ in range(REPEAT_COUNT):
            payload["source_runtime_ms"].append(run_query(source_sql_path))
            payload["rewrite_runtime_ms"].append(run_query(candidate_sql_path))
    finally:
        try:
            spark.sql("USE default")
            spark.sql(f"DROP DATABASE IF EXISTS {db_name} CASCADE")
        except Exception:
            pass
        spark.stop()
        shutil.rmtree(warehouse_dir, ignore_errors=True)

    payload["median_source_ms"] = statistics.median(payload["source_runtime_ms"])
    payload["median_rewrite_ms"] = statistics.median(payload["rewrite_runtime_ms"])
    if payload["median_rewrite_ms"] and payload["median_rewrite_ms"] > 0:
        payload["speedup_ratio"] = payload["median_source_ms"] / payload["median_rewrite_ms"]
        payload["status"] = "success"
    else:
        payload["status"] = "failure"
        payload["notes"] = "rewrite median was zero"
    return payload


def geometric_mean(values: list[float]) -> float | None:
    positive = [value for value in values if value > 0]
    if not positive:
        return None
    return math.exp(sum(math.log(value) for value in positive) / len(positive))


def classify_speedup(speedup: float) -> str:
    if speedup > 1.05:
        return "win"
    if speedup < 0.95:
        return "loss"
    return "tie"


ensure_env()
all_rows = load_timing_rows()
backfill_summary = load_backfill_summary()

route_counts = Counter(row["route_id"] for row in all_rows)
for route_id, config in ROUTES.items():
    count = route_counts.get(route_id, 0)
    if count != config["expected_rows"]:
        raise RuntimeError(f"Route {route_id} expected {config['expected_rows']} rows but found {count}")

timing_events: list[dict[str, object]] = []
timing_failures: list[dict[str, object]] = []
timing_command_rows: list[dict[str, object]] = []

for row in all_rows:
    row_id = row["row_id"]
    route_id = row["route_id"]
    case_id = row["case_id"]
    pool = row["pool"]
    engine = row["engine"]
    timing_denominator_id = ROUTES[route_id]["timing_denominator_id"]
    source_sql_path = REPO_ROOT / row["source_sql_artifact"]
    candidate_sql_path = REPO_ROOT / row["candidate_sql_artifact"]
    schema_path = REPO_ROOT / row["schema_artifact"]
    result_check_artifact = Path(row["result_check_artifact"])
    witness_sql_path = witness_path(case_id, pool, engine)
    timing_json_path = TIMINGS_DIR / route_id / case_id / engine / "timing.json"
    stdout_log_path = LOGS_DIR / f"{row_id}.stdout.log"
    stderr_log_path = LOGS_DIR / f"{row_id}.stderr.log"

    timing_command_rows.append({
        "row_id": row_id,
        "method_id": METHOD_ID,
        "route_id": route_id,
        "case_id": case_id,
        "engine": engine,
        "timing_denominator_id": timing_denominator_id,
        "warmup_count": WARMUP_COUNT,
        "repeat_count": REPEAT_COUNT,
        "timeout_policy": f"{QUERY_TIMEOUT_SECONDS}s_per_query_attempt",
        "source_sql_artifact": row["source_sql_artifact"],
        "candidate_sql_artifact": row["candidate_sql_artifact"],
        "schema_artifact": row["schema_artifact"],
        "result_check_artifact": row["result_check_artifact"],
        "witness_artifact": str(witness_sql_path.relative_to(REPO_ROOT)),
        "timing_json_artifact": str(timing_json_path.relative_to(REPO_ROOT)),
        "stdout_log_artifact": str(stdout_log_path.relative_to(REPO_ROOT)),
        "stderr_log_artifact": str(stderr_log_path.relative_to(REPO_ROOT)),
        "notes": "route-separated SQLGlot timing after checker backfill",
    })

    payload: dict[str, object]
    try:
        if engine == "pg":
            payload = run_pg_timing(source_sql_path, candidate_sql_path, schema_path, witness_sql_path, row_id)
        elif engine == "mysql":
            payload = run_mysql_timing(source_sql_path, candidate_sql_path, schema_path, witness_sql_path)
        elif engine == "spark":
            payload = run_spark_timing(source_sql_path, candidate_sql_path, schema_path, witness_sql_path, row_id)
        else:
            raise RuntimeError(f"Unsupported engine: {engine}")
        stdout_log_path.write_text(
            f"timing completed for {row_id}\nsource_runtime_ms={payload.get('source_runtime_ms')}\nrewrite_runtime_ms={payload.get('rewrite_runtime_ms')}\n",
            encoding="utf-8",
        )
        stderr_log_path.write_text("", encoding="utf-8")
    except Exception as exc:
        payload = {
            "source_runtime_ms": [],
            "rewrite_runtime_ms": [],
            "median_source_ms": None,
            "median_rewrite_ms": None,
            "speedup_ratio": None,
            "status": "failure",
            "notes": str(exc),
        }
        stderr_log_path.write_text(traceback.format_exc(), encoding="utf-8")
        stdout_log_path.write_text("", encoding="utf-8")

    write_json(timing_json_path, payload)
    success = payload.get("status") == "success"
    speedup_ratio = payload.get("speedup_ratio")
    failure_category = ""
    failure_detail = ""
    if not success:
        failure_category = "timing_failed"
        failure_detail = str(payload.get("notes") or "timing failure")
        timing_failures.append({
            "row_id": row_id,
            "case_id": case_id,
            "engine": engine,
            "failure_stage": "timing",
            "failure_type": failure_category,
            "failure_detail": failure_detail,
            "source_sql_artifact": row["source_sql_artifact"],
            "candidate_sql_artifact": row["candidate_sql_artifact"],
            "notes": "row remained in route-separated timing packet",
        })

    timing_events.append({
        "row_id": row_id,
        "method_id": METHOD_ID,
        "route_id": route_id,
        "case_id": case_id,
        "pool": pool,
        "engine": engine,
        "denominator_id": DENOMINATOR_ID,
        "timing_denominator_id": timing_denominator_id,
        "source_sql_artifact": row["source_sql_artifact"],
        "candidate_sql_artifact": row["candidate_sql_artifact"],
        "schema_artifact": row["schema_artifact"],
        "result_check_artifact": row["result_check_artifact"],
        "source_runtime_ms": payload.get("median_source_ms", ""),
        "rewrite_runtime_ms": payload.get("median_rewrite_ms", ""),
        "speedup_ratio": speedup_ratio if success else "",
        "timing_success": str(success).lower(),
        "timing_failure_category": failure_category,
        "timing_failure_detail": failure_detail,
        "source_artifacts": row["source_artifacts"],
        "notes": "route-separated SQLGlot timing after checker backfill",
    })


summary_rows: list[dict[str, object]] = []
for route_id, config in ROUTES.items():
    route_events = [row for row in timing_events if row["route_id"] == route_id]
    success_events = [row for row in route_events if str(row["timing_success"]).lower() in {"true", "yes", "1"}]
    failed_events = [row for row in route_events if str(row["timing_success"]).lower() not in {"true", "yes", "1"}]
    speedups = [float(row["speedup_ratio"]) for row in success_events]
    median_speedup = statistics.median(speedups) if speedups else None
    gm_speedup = geometric_mean(speedups)
    win_count = sum(classify_speedup(value) == "win" for value in speedups)
    tie_count = sum(classify_speedup(value) == "tie" for value in speedups)
    loss_count = sum(classify_speedup(value) == "loss" for value in speedups)
    regression_count = sum(value < 0.8 for value in speedups)
    best_event = max(success_events, key=lambda row: float(row["speedup_ratio"])) if success_events else None
    worst_event = min(success_events, key=lambda row: float(row["speedup_ratio"])) if success_events else None
    summary_rows.append({
        "method_id": METHOD_ID,
        "route_id": route_id,
        "denominator_id": DENOMINATOR_ID,
        "timing_denominator_id": config["timing_denominator_id"],
        "planned_rows": config["expected_rows"],
        "exact_rows_after_backfill": config["expected_rows"],
        "timing_attempted_rows": len(route_events),
        "timing_success_rows": len(success_events),
        "timing_failed_rows": len(failed_events),
        "median_speedup": median_speedup if median_speedup is not None else "NA_not_computed",
        "gm_speedup": gm_speedup if gm_speedup is not None else "NA_not_computed",
        "win_count": win_count,
        "tie_count": tie_count,
        "loss_count": loss_count,
        "regression_20pct_count": regression_count,
        "regression_rate_20pct": (regression_count / len(success_events)) if success_events else "NA_not_computed",
        "best_case_id": best_event["case_id"] if best_event else "NA_not_computed",
        "best_case_engine": best_event["engine"] if best_event else "NA_not_computed",
        "best_case_speedup": best_event["speedup_ratio"] if best_event else "NA_not_computed",
        "worst_case_id": worst_event["case_id"] if worst_event else "NA_not_computed",
        "worst_case_engine": worst_event["engine"] if worst_event else "NA_not_computed",
        "worst_case_speedup": worst_event["speedup_ratio"] if worst_event else "NA_not_computed",
        "claim_boundary": (
            "route-separated SQLGlot per-case timing after checker backfill; no combined main row; no final ranked leaderboard"
        ),
        "source_artifacts": " | ".join([
            str(DENOM_CSV.relative_to(REPO_ROOT)),
            str((FREEZE_DIR / "sqlglot_result_check_backfill_summary_v1.csv").relative_to(REPO_ROOT)),
            str((FREEZE_DIR / "sqlglot_result_check_backfill_event_long_v1.csv").relative_to(REPO_ROOT)),
        ]),
        "notes": (
            "Optimize uses revised 63-row exact denominator after excluding the two checker_failed rows."
            if route_id == "sqlglot_optimize_same_dialect"
            else "No-op uses the full 72-row exact denominator after checker backfill."
        ),
    })


write_csv(COMMAND_MATRIX_CSV, [
    "row_id",
    "method_id",
    "route_id",
    "case_id",
    "engine",
    "timing_denominator_id",
    "warmup_count",
    "repeat_count",
    "timeout_policy",
    "source_sql_artifact",
    "candidate_sql_artifact",
    "schema_artifact",
    "result_check_artifact",
    "witness_artifact",
    "timing_json_artifact",
    "stdout_log_artifact",
    "stderr_log_artifact",
    "notes",
], timing_command_rows)

write_csv(TIMING_EVENT_LONG_CSV, [
    "row_id",
    "method_id",
    "route_id",
    "case_id",
    "pool",
    "engine",
    "denominator_id",
    "timing_denominator_id",
    "source_sql_artifact",
    "candidate_sql_artifact",
    "schema_artifact",
    "result_check_artifact",
    "source_runtime_ms",
    "rewrite_runtime_ms",
    "speedup_ratio",
    "timing_success",
    "timing_failure_category",
    "timing_failure_detail",
    "source_artifacts",
    "notes",
], timing_events)

write_csv(TIMING_FAILURES_CSV, [
    "row_id",
    "case_id",
    "engine",
    "failure_stage",
    "failure_type",
    "failure_detail",
    "source_sql_artifact",
    "candidate_sql_artifact",
    "notes",
], timing_failures)

write_csv(TIMING_SUMMARY_CSV, [
    "method_id",
    "route_id",
    "denominator_id",
    "timing_denominator_id",
    "planned_rows",
    "exact_rows_after_backfill",
    "timing_attempted_rows",
    "timing_success_rows",
    "timing_failed_rows",
    "median_speedup",
    "gm_speedup",
    "win_count",
    "tie_count",
    "loss_count",
    "regression_20pct_count",
    "regression_rate_20pct",
    "best_case_id",
    "best_case_engine",
    "best_case_speedup",
    "worst_case_id",
    "worst_case_engine",
    "worst_case_speedup",
    "claim_boundary",
    "source_artifacts",
    "notes",
], summary_rows)

TIMING_SUMMARY_MD.write_text(
    "# SQLGlot Full Per-Case Timing Summary v1\n\n"
    "This packet reports route-separated SQLGlot timing after checker backfill. No SQLGlot generation was rerun, no checker was rerun in this timing step, and this does not create a final ranked leaderboard.\n\n"
    "## Table\n\n"
    + csv_to_markdown(TIMING_SUMMARY_CSV)
    + "\n\n## Notes\n\n"
    "- 中文说明：这里仍然是 route-separated 口径，`sqlglot_combined_same_engine_240` 没有进入主 timing summary。\n"
    "- `sqlglot_optimize_same_dialect` 使用的是修订后的 63-row exact denominator，而不是旧的 aggregate 65。\n",
    encoding="utf-8",
)

README_MD.write_text(
    "# SQLGlot Full Per-Case Timing 01\n\n"
    "This run executes route-separated SQLGlot same-engine timing after row-level checker backfill.\n\n"
    "Boundaries:\n"
    "- no SQLGlot generation rerun\n"
    "- no checker rerun in this timing step\n"
    "- no combined SQLGlot main row\n"
    "- no final ranked leaderboard\n",
    encoding="utf-8",
)

POLICY_MD.write_text(
    "# Timing Policy v1\n\n"
    "- warmup count: 1\n"
    "- repeat count: 3\n"
    f"- timeout policy: {QUERY_TIMEOUT_SECONDS}s per query attempt\n"
    "- speedup ratio: source_runtime_ms / rewrite_runtime_ms using row-local medians\n"
    "- win: speedup_ratio > 1.05\n"
    "- tie: 0.95 <= speedup_ratio <= 1.05\n"
    "- loss: speedup_ratio < 0.95\n"
    "- Regression@20: speedup_ratio < 0.8\n"
    "- routes stay separated: `sqlglot_transpile_same_dialect_noop`, `sqlglot_optimize_same_dialect`\n",
    encoding="utf-8",
)

result_card_rows: list[dict[str, object]] = []
for row in summary_rows:
    result_card_rows.append({
        "method_id": row["method_id"],
        "route_id": row["route_id"],
        "timing_denominator_id": row["timing_denominator_id"],
        "exact_rows_after_backfill": row["exact_rows_after_backfill"],
        "timing_success_rows": row["timing_success_rows"],
        "median_speedup": row["median_speedup"],
        "gm_speedup": row["gm_speedup"],
        "regression_rate_20pct": row["regression_rate_20pct"],
        "claim_boundary": row["claim_boundary"],
        "notes": row["notes"],
    })

write_csv(RESULT_CARD_CSV, [
    "method_id",
    "route_id",
    "timing_denominator_id",
    "exact_rows_after_backfill",
    "timing_success_rows",
    "median_speedup",
    "gm_speedup",
    "regression_rate_20pct",
    "claim_boundary",
    "notes",
], result_card_rows)

RESULT_CARD_MD.write_text(
    "# SQLGlot Full Per-Case Timing Result Card v1\n\n"
    "This is route-separated SQLGlot per-case timing after checker backfill.\n\n"
    "- SQLGlot no-op uses 72 exact rows.\n"
    "- SQLGlot optimize uses revised 63 exact rows, not the prior aggregate 65.\n"
    "- The two optimize checker_failed rows are excluded from timing and remain visible in the checker backfill packet.\n"
    "- No SQLGlot generation was rerun.\n"
    "- No checker was rerun in this timing step.\n"
    "- This does not create a final ranked leaderboard.\n\n"
    "## Table\n\n"
    + csv_to_markdown(RESULT_CARD_CSV),
    encoding="utf-8",
)

run_results_payload = {
    "command": "sqlglot_full_per_case_timing_01",
    "ran_at_utc": utc_now(),
    "status": "ok" if not timing_failures else "warning",
    "warmup_count": WARMUP_COUNT,
    "repeat_count": REPEAT_COUNT,
    "timeout_policy": f"{QUERY_TIMEOUT_SECONDS}s_per_query_attempt",
    "expected_noop_rows": ROUTES["sqlglot_transpile_same_dialect_noop"]["expected_rows"],
    "expected_optimize_rows": ROUTES["sqlglot_optimize_same_dialect"]["expected_rows"],
    "route_counts": dict(route_counts),
    "excluded_row_ids": sorted(EXCLUDED_ROW_IDS),
    "summary_rows": summary_rows,
    "claim_boundary": "route-separated SQLGlot per-case timing after checker backfill; no combined main row; no final ranked leaderboard",
}
write_json(RUN_RESULTS_JSON, run_results_payload)

validation_payload = {
    "status": "ok" if not timing_failures else "warning",
    "expected_noop_rows": ROUTES["sqlglot_transpile_same_dialect_noop"]["expected_rows"],
    "expected_optimize_rows": ROUTES["sqlglot_optimize_same_dialect"]["expected_rows"],
    "timing_event_rows": len(timing_events),
    "timing_failure_rows": len(timing_failures),
    "summary_row_count": len(summary_rows),
    "routes_present": sorted(route_counts.keys()),
    "excluded_row_ids": sorted(EXCLUDED_ROW_IDS),
}
write_json(VALIDATION_REPORT_JSON, validation_payload)

print(json.dumps({
    "timing_event_rows": len(timing_events),
    "timing_failure_rows": len(timing_failures),
    "status": validation_payload["status"],
}, ensure_ascii=False))
PY
