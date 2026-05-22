#!/usr/bin/env bash
set -euo pipefail

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
  echo "run from repo root: $REPO_ROOT" >&2
  exit 1
fi

RUN_ID="calcite_hep_mysql_spark_rewrite_expansion_80_01"
METHOD_ID="calcite_hep"
ROUTE_ID="calcite_hep_same_engine_rewrite"
EXPANSION_DENOMINATOR_ID="calcite_hep_mysql_spark_common_core_v0_80"
CLAIM_BOUNDARY="mysql_spark_rewrite_expansion_80_only_not_execution_timing_speedup_or_leaderboard_evidence"

RUN_DIR="$REPO_ROOT/reports/evaluation/common_core_v0/runs/$RUN_ID"
MATRIX_PATH="$RUN_DIR/rewrite_command_matrix.csv"
RUN_RESULTS_PATH="$RUN_DIR/run_results.json"
RUN_EVENT_LONG_PATH="$RUN_DIR/run_event_long.csv"

CALCITE_CHECKOUT_ROOT="${CALCITE_CHECKOUT_ROOT:-$REPO_ROOT/datasets/raw/calcite/calcite}"
CALCITE_WORK_ROOT="${CALCITE_WORK_ROOT:-/tmp/calcite-hep-mysql-spark-rewrite-expansion-80-01}"
GRADLE_USER_HOME="${GRADLE_USER_HOME:-/tmp/calcite-gradle-home}"
WRAPPER_SRC="${WRAPPER_SRC:-$REPO_ROOT/reports/evaluation/common_core_v0/runs/calcite_hep_mysql_spark_canary_02/wrapper_src/CalciteHepTargetDialectCanary.java}"
WRAPPER_CLASSES_DIR="$CALCITE_WORK_ROOT/classes"
WRAPPER_CLASSPATH_FILE="$CALCITE_WORK_ROOT/wrapper_classpath.txt"
MYSQL_DIALECT_SOURCE="$CALCITE_CHECKOUT_ROOT/core/src/main/java/org/apache/calcite/sql/dialect/MysqlSqlDialect.java"
SPARK_DIALECT_SOURCE="$CALCITE_CHECKOUT_ROOT/core/src/main/java/org/apache/calcite/sql/dialect/SparkSqlDialect.java"

mkdir -p "$RUN_DIR" "$CALCITE_WORK_ROOT" "$WRAPPER_CLASSES_DIR"

wrapper_compile_status="not_attempted"
wrapper_compile_blocker=""
mysql_dialect_available="false"
spark_dialect_available="false"

if [[ ! -f "$WRAPPER_SRC" ]]; then
  wrapper_compile_status="setup_failed"
  wrapper_compile_blocker="wrapper_source_missing:$WRAPPER_SRC"
elif [[ ! -d "$CALCITE_CHECKOUT_ROOT" ]]; then
  wrapper_compile_status="setup_failed"
  wrapper_compile_blocker="calcite_checkout_missing:$CALCITE_CHECKOUT_ROOT"
else
  [[ -f "$MYSQL_DIALECT_SOURCE" ]] && mysql_dialect_available="true"
  [[ -f "$SPARK_DIALECT_SOURCE" ]] && spark_dialect_available="true"

  CLASSPATH_CORE="$CALCITE_CHECKOUT_ROOT/core/build/classes/java/main:$CALCITE_CHECKOUT_ROOT/core/build/resources/main:$CALCITE_CHECKOUT_ROOT/linq4j/build/classes/java/main"
  CLASSPATH_JARS="$(find "$GRADLE_USER_HOME/caches/modules-2/files-2.1" -name '*.jar' -print 2>/dev/null | sort | paste -sd: -)"

  if [[ -d "$CALCITE_CHECKOUT_ROOT/core/build/classes/java/main" && -d "$CALCITE_CHECKOUT_ROOT/linq4j/build/classes/java/main" && -n "${CLASSPATH_JARS:-}" ]]; then
    FULL_CLASSPATH="$WRAPPER_CLASSES_DIR:$CLASSPATH_CORE:$CLASSPATH_JARS"
    printf '%s' "$FULL_CLASSPATH" > "$WRAPPER_CLASSPATH_FILE"
    if javac -cp "$CLASSPATH_CORE:$CLASSPATH_JARS" -d "$WRAPPER_CLASSES_DIR" "$WRAPPER_SRC"; then
      wrapper_compile_status="ok"
    else
      wrapper_compile_status="setup_failed"
      wrapper_compile_blocker="wrapper_compile_failed"
    fi
  else
    wrapper_compile_status="setup_failed"
    wrapper_compile_blocker="calcite_classes_or_cached_jars_missing"
  fi
fi

python - <<'PY' "$REPO_ROOT" "$MATRIX_PATH" "$RUN_RESULTS_PATH" "$RUN_EVENT_LONG_PATH" "$WRAPPER_CLASSPATH_FILE" "$WRAPPER_SRC" "$CALCITE_CHECKOUT_ROOT" "$RUN_ID" "$METHOD_ID" "$ROUTE_ID" "$EXPANSION_DENOMINATOR_ID" "$CLAIM_BOUNDARY" "$wrapper_compile_status" "$wrapper_compile_blocker" "$mysql_dialect_available" "$spark_dialect_available"
from __future__ import annotations

import csv
import json
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

repo_root = Path(sys.argv[1])
matrix_path = Path(sys.argv[2])
run_results_path = Path(sys.argv[3])
run_event_long_path = Path(sys.argv[4])
wrapper_classpath_file = Path(sys.argv[5])
wrapper_src = Path(sys.argv[6])
calcite_checkout_root = Path(sys.argv[7])
run_id = sys.argv[8]
method_id = sys.argv[9]
route_id = sys.argv[10]
expansion_denominator_id = sys.argv[11]
claim_boundary = sys.argv[12]
wrapper_compile_status = sys.argv[13]
wrapper_compile_blocker = sys.argv[14]
mysql_dialect_available = sys.argv[15] == "true"
spark_dialect_available = sys.argv[16] == "true"

rows = list(csv.DictReader(matrix_path.open("r", encoding="utf-8")))

event_fields = [
    "run_id",
    "row_key",
    "case_id",
    "pool",
    "engine",
    "method_id",
    "route_id",
    "expansion_denominator_id",
    "source_sql_path",
    "schema_path",
    "witness_data_path",
    "row_status",
    "dialect_class_used",
    "rewrite_changed",
    "generated_sql_path",
    "log_stdout_path",
    "log_stderr_path",
    "row_metadata_path",
    "failure_category",
    "blocker_reason",
    "claim_boundary",
]


def normalize_bool(value: str | None) -> str:
    if value is None:
        return ""
    return value.strip().lower()


def resolve_source_sql(repo_root: Path, matrix_source_path: str) -> tuple[Path | None, str]:
    matrix_path = repo_root / matrix_source_path
    if matrix_path.is_file():
        return matrix_path, matrix_source_path

    case_root = matrix_path.parent
    preferred = case_root / "source.sql"
    fallback = case_root / "source" / "query.sql"
    if preferred.is_file():
        return preferred, str(preferred.relative_to(repo_root))
    if fallback.is_file():
        return fallback, str(fallback.relative_to(repo_root))
    return None, ""


def classify_from_stdout(stdout_kv: dict[str, str], emitted_nonempty: bool, rc: int) -> tuple[str, str, str]:
    if rc != 0 and not stdout_kv:
        return ("setup_failed", "setup_failed", f"wrapper_command_rc_{rc}")
    if normalize_bool(stdout_kv.get("calcite_parse_succeeded")) != "true":
        return ("parser_failed", "parser_failed", stdout_kv.get("blocker_reason", "parse_failed"))
    if normalize_bool(stdout_kv.get("rel_to_sql_succeeded")) == "true" and emitted_nonempty:
        return ("rewrite_success", "", "")
    if normalize_bool(stdout_kv.get("hep_planner_succeeded")) == "true" and normalize_bool(stdout_kv.get("rel_to_sql_succeeded")) != "true":
        return ("rel_to_sql_failed", "rel_to_sql_failed", stdout_kv.get("blocker_reason", "rel_to_sql_failed"))
    if normalize_bool(stdout_kv.get("candidate_sql_emitted")) == "true" and not emitted_nonempty:
        return ("generated_sql_missing", "generated_sql_missing", "generated_sql_missing_after_emit")
    if stdout_kv.get("failure_category") == "rendered_sql_missing":
        return ("generated_sql_missing", "generated_sql_missing", stdout_kv.get("blocker_reason", "generated_sql_missing"))
    return ("hep_rewrite_failed", "hep_rewrite_failed", stdout_kv.get("blocker_reason", "hep_rewrite_failed"))


status_counts: Counter[str] = Counter()
counts_by_engine: dict[str, Counter[str]] = defaultdict(Counter)
row_records: list[dict[str, object]] = []

with run_event_long_path.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=event_fields)
    writer.writeheader()

    for row in rows:
        engine = row["engine"]
        dialect_available = mysql_dialect_available if engine == "mysql" else spark_dialect_available
        dialect_class_used = ""
        if engine == "mysql":
            dialect_class_used = "org.apache.calcite.sql.dialect.MysqlSqlDialect"
        elif engine == "spark":
            dialect_class_used = "org.apache.calcite.sql.dialect.SparkSqlDialect"

        resolved_source_path, resolved_source_rel = resolve_source_sql(repo_root, row["source_sql_path"])
        source_exists = resolved_source_path is not None
        schema_path = repo_root / row["schema_path"]
        schema_exists = schema_path.is_file()
        witness_path = repo_root / row["witness_data_path"]
        witness_exists = witness_path.is_file()
        witness_missing_for_later_execution = not witness_exists

        generated_path = repo_root / row["expected_generated_sql_path"]
        stdout_log_path = repo_root / row["expected_log_stdout_path"]
        stderr_log_path = repo_root / row["expected_log_stderr_path"]
        row_metadata_path = repo_root / row["expected_row_metadata_path"]
        for path in [generated_path.parent, stdout_log_path.parent, stderr_log_path.parent, row_metadata_path.parent]:
            path.mkdir(parents=True, exist_ok=True)

        stdout_kv: dict[str, str] = {}
        row_status = ""
        failure_category = ""
        blocker_reason = ""
        rewrite_changed = ""

        if not source_exists:
            row_status = "setup_failed"
            failure_category = "missing_source_sql"
            blocker_reason = "missing_source_sql"
        elif not schema_exists:
            row_status = "setup_failed"
            failure_category = "missing_schema_sql"
            blocker_reason = "missing_schema_sql"
        elif wrapper_compile_status != "ok":
            row_status = "setup_failed"
            failure_category = "wrapper_compile_failed" if wrapper_compile_blocker == "wrapper_compile_failed" else "setup_failed"
            blocker_reason = wrapper_compile_blocker
        elif not dialect_available:
            row_status = "target_dialect_unavailable"
            failure_category = "target_dialect_unavailable"
            blocker_reason = f"dialect_class_unavailable_for_engine:{engine}"
        else:
            cmd = [
                "java",
                "-cp",
                wrapper_classpath_file.read_text(encoding="utf-8"),
                "CalciteHepTargetDialectCanary",
                "--case-id",
                row["case_id"],
                "--engine",
                engine,
                "--source-sql",
                str(resolved_source_path),
                "--ddl",
                str(schema_path),
                "--output-sql",
                str(generated_path),
            ]
            with stdout_log_path.open("w", encoding="utf-8") as stdout_handle, stderr_log_path.open("w", encoding="utf-8") as stderr_handle:
                proc = subprocess.run(cmd, cwd=repo_root, stdout=stdout_handle, stderr=stderr_handle, text=True)
            if stdout_log_path.is_file():
                for line in stdout_log_path.read_text(encoding="utf-8").splitlines():
                    if "=" in line:
                        k, v = line.split("=", 1)
                        stdout_kv[k.strip()] = v.strip()
            emitted_nonempty = generated_path.is_file() and generated_path.read_text(encoding="utf-8").strip() != ""
            row_status, failure_category, blocker_reason = classify_from_stdout(stdout_kv, emitted_nonempty, proc.returncode)
            rewrite_changed = stdout_kv.get("rewrite_changed", "")
            if row_status == "rewrite_success":
                failure_category = ""
                blocker_reason = ""

        record = {
            "run_id": run_id,
            "row_key": row["row_key"],
            "case_id": row["case_id"],
            "pool": row["pool"],
            "engine": row["engine"],
            "method_id": method_id,
            "route_id": route_id,
            "expansion_denominator_id": expansion_denominator_id,
            "source_sql_path": resolved_source_rel or row["source_sql_path"],
            "schema_path": row["schema_path"],
            "witness_data_path": row["witness_data_path"],
            "row_status": row_status,
            "dialect_class_used": dialect_class_used,
            "rewrite_changed": rewrite_changed,
            "generated_sql_path": row["expected_generated_sql_path"],
            "log_stdout_path": row["expected_log_stdout_path"],
            "log_stderr_path": row["expected_log_stderr_path"],
            "row_metadata_path": row["expected_row_metadata_path"],
            "failure_category": failure_category,
            "blocker_reason": blocker_reason,
            "claim_boundary": claim_boundary,
            "wrapper_stdout_kv": stdout_kv,
            "witness_missing_for_later_execution": witness_missing_for_later_execution,
            "caveat": row["caveat"],
        }
        row_records.append(record)
        status_counts[row_status] += 1
        counts_by_engine[engine][row_status] += 1
        writer.writerow({k: record.get(k, "") for k in event_fields})
        row_metadata_path.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")

payload = {
    "run_id": run_id,
    "method_id": method_id,
    "route_id": route_id,
    "expansion_denominator_id": expansion_denominator_id,
    "planned_rows": len(rows),
    "status_counts": dict(status_counts),
    "counts_by_engine": {engine: dict(counter) for engine, counter in sorted(counts_by_engine.items())},
    "target_dialect_availability": {
        "mysql": mysql_dialect_available,
        "spark": spark_dialect_available,
    },
    "wrapper_compile_status": wrapper_compile_status,
    "wrapper_compile_blocker": wrapper_compile_blocker,
    "wrapper_source": str(wrapper_src),
    "calcite_checkout_root": str(calcite_checkout_root),
    "claim_boundary": claim_boundary,
    "current_benchmark_metric_evidence": False,
    "rows": row_records,
}
run_results_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
PY

echo "wrote $RUN_RESULTS_PATH"
