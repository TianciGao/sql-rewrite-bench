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

RUN_ID="calcite_hep_mysql_spark_canary_02"
METHOD_ID="calcite_hep"
ROUTE_ID="calcite_hep_same_engine_rewrite"
CANARY_DENOMINATOR_ID="calcite_hep_mysql_spark_canary_02"
CLAIM_BOUNDARY="mysql_spark_rewrite_canary_v2_only_not_execution_timing_speedup_or_leaderboard_evidence"

RUN_DIR="$REPO_ROOT/reports/evaluation/common_core_v0/runs/$RUN_ID"
MATRIX_PATH="$RUN_DIR/rewrite_command_matrix.csv"
RUN_RESULTS_PATH="$RUN_DIR/run_results.json"
RUN_EVENT_LONG_PATH="$RUN_DIR/run_event_long.csv"

CALCITE_CHECKOUT_ROOT="${CALCITE_CHECKOUT_ROOT:-$REPO_ROOT/datasets/raw/calcite/calcite}"
CALCITE_WORK_ROOT="${CALCITE_WORK_ROOT:-/tmp/calcite-hep-mysql-spark-canary-02}"
GRADLE_USER_HOME="${GRADLE_USER_HOME:-/tmp/calcite-gradle-home}"
WRAPPER_SRC="$RUN_DIR/wrapper_src/CalciteHepTargetDialectCanary.java"
WRAPPER_CLASSES_DIR="$CALCITE_WORK_ROOT/classes"
WRAPPER_CLASSPATH_FILE="$CALCITE_WORK_ROOT/wrapper_classpath.txt"
MYSQL_DIALECT_SOURCE="$CALCITE_CHECKOUT_ROOT/core/src/main/java/org/apache/calcite/sql/dialect/MysqlSqlDialect.java"
SPARK_DIALECT_SOURCE="$CALCITE_CHECKOUT_ROOT/core/src/main/java/org/apache/calcite/sql/dialect/SparkSqlDialect.java"

mkdir -p "$RUN_DIR" "$CALCITE_WORK_ROOT" "$WRAPPER_CLASSES_DIR"

wrapper_compile_status="not_attempted"
wrapper_compile_blocker=""
mysql_dialect_available="false"
spark_dialect_available="false"
classpath_ready="false"

if [[ ! -f "$WRAPPER_SRC" ]]; then
  wrapper_compile_status="wrapper_source_missing"
  wrapper_compile_blocker="$WRAPPER_SRC"
elif [[ ! -d "$CALCITE_CHECKOUT_ROOT" ]]; then
  wrapper_compile_status="calcite_checkout_missing"
  wrapper_compile_blocker="$CALCITE_CHECKOUT_ROOT"
else
  if [[ -f "$MYSQL_DIALECT_SOURCE" ]]; then
    mysql_dialect_available="true"
  fi
  if [[ -f "$SPARK_DIALECT_SOURCE" ]]; then
    spark_dialect_available="true"
  fi

  if (
    cd "$CALCITE_CHECKOUT_ROOT"
    export GRADLE_USER_HOME
    ./gradlew :core:classes >/dev/null
  ); then
    CLASSPATH_CORE="$CALCITE_CHECKOUT_ROOT/core/build/classes/java/main:$CALCITE_CHECKOUT_ROOT/core/build/resources/main:$CALCITE_CHECKOUT_ROOT/linq4j/build/classes/java/main"
    CLASSPATH_JARS="$(find "$GRADLE_USER_HOME/caches/modules-2/files-2.1" -name '*.jar' -print | sort | paste -sd: -)"
    FULL_CLASSPATH="$WRAPPER_CLASSES_DIR:$CLASSPATH_CORE:$CLASSPATH_JARS"
    printf '%s' "$FULL_CLASSPATH" > "$WRAPPER_CLASSPATH_FILE"
    classpath_ready="true"
    if javac -cp "$CLASSPATH_CORE:$CLASSPATH_JARS" -d "$WRAPPER_CLASSES_DIR" "$WRAPPER_SRC"; then
      wrapper_compile_status="ok"
    else
      wrapper_compile_status="wrapper_compile_failed"
      wrapper_compile_blocker="javac_failed_for_package_local_wrapper"
    fi
  else
    wrapper_compile_status="gradle_core_classes_failed"
    wrapper_compile_blocker="gradle_core_classes_failed"
  fi
fi

run_row() {
  local row_key="$1"
  local case_id="$2"
  local pool="$3"
  local engine="$4"
  local source_sql_path="$5"
  local schema_path="$6"
  local witness_data_path="$7"
  local generated_sql_path="$8"
  local stdout_log_path="$9"
  local stderr_log_path="${10}"
  local row_metadata_path="${11}"

  local abs_generated_sql_path="$REPO_ROOT/$generated_sql_path"
  local abs_stdout_log_path="$REPO_ROOT/$stdout_log_path"
  local abs_stderr_log_path="$REPO_ROOT/$stderr_log_path"
  local abs_row_metadata_path="$REPO_ROOT/$row_metadata_path"

  mkdir -p "$(dirname "$abs_generated_sql_path")" "$(dirname "$abs_stdout_log_path")" "$(dirname "$abs_row_metadata_path")"

  local failure_category=""
  local blocker_reason=""
  local row_status="rewrite_failed"
  local dialect_rendering_status=""
  local dialect_class_used=""
  local rewrite_changed_json="null"

  local dialect_available_for_engine="false"
  if [[ "$engine" == "mysql" && "$mysql_dialect_available" == "true" ]]; then
    dialect_available_for_engine="true"
    dialect_class_used="org.apache.calcite.sql.dialect.MysqlSqlDialect"
  elif [[ "$engine" == "spark" && "$spark_dialect_available" == "true" ]]; then
    dialect_available_for_engine="true"
    dialect_class_used="org.apache.calcite.sql.dialect.SparkSqlDialect"
  fi

  local source_missing="false"
  [[ -f "$REPO_ROOT/$source_sql_path" ]] || source_missing="true"
  local schema_missing="false"
  [[ -f "$REPO_ROOT/$schema_path" ]] || schema_missing="true"
  local witness_missing="false"
  [[ -f "$REPO_ROOT/$witness_data_path" ]] || witness_missing="true"

  if [[ "$source_missing" == "true" || "$schema_missing" == "true" || "$witness_missing" == "true" ]]; then
    row_status="preflight_blocked"
    failure_category="missing_case_artifact"
    blocker_reason="source_or_schema_or_witness_missing"
    dialect_rendering_status="target_dialect_unavailable"
  elif [[ "$wrapper_compile_status" != "ok" ]]; then
    row_status="preflight_blocked"
    failure_category="$wrapper_compile_status"
    blocker_reason="$wrapper_compile_blocker"
    dialect_rendering_status="wrapper_compile_failed"
  elif [[ "$dialect_available_for_engine" != "true" ]]; then
    row_status="preflight_blocked"
    failure_category="target_engine_dialect_not_implemented"
    blocker_reason="dialect_class_unavailable_for_engine:$engine"
    dialect_rendering_status="target_dialect_unavailable"
  else
    set +e
    java -cp "$(cat "$WRAPPER_CLASSPATH_FILE")" \
      CalciteHepTargetDialectCanary \
      --case-id "$case_id" \
      --engine "$engine" \
      --source-sql "$REPO_ROOT/$source_sql_path" \
      --ddl "$REPO_ROOT/$schema_path" \
      --output-sql "$abs_generated_sql_path" \
      >"$abs_stdout_log_path" 2>"$abs_stderr_log_path"
    local rc=$?
    set -e

    python - <<'PY' "$REPO_ROOT" "$source_sql_path" "$abs_generated_sql_path" "$abs_stdout_log_path" "$engine" "$rc" "$abs_row_metadata_path" "$row_key" "$case_id" "$pool" "$witness_data_path" "$dialect_class_used" "$METHOD_ID" "$ROUTE_ID" "$CANARY_DENOMINATOR_ID" "$CLAIM_BOUNDARY"
import json
import os
import re
import sys
from pathlib import Path

repo_root = Path(sys.argv[1])
source_sql_path = sys.argv[2]
generated_sql_abs = Path(sys.argv[3])
stdout_log_abs = Path(sys.argv[4])
engine = sys.argv[5]
rc = int(sys.argv[6])
row_metadata_abs = Path(sys.argv[7])
row_key = sys.argv[8]
case_id = sys.argv[9]
pool = sys.argv[10]
witness_data_path = sys.argv[11]
dialect_class_used = sys.argv[12]
method_id = sys.argv[13]
route_id = sys.argv[14]
canary_denominator_id = sys.argv[15]
claim_boundary = sys.argv[16]

def normalize_sql(text: str) -> str:
    text = text.strip()
    if text.endswith(";"):
        text = text[:-1]
    return re.sub(r"\s+", " ", text).strip()

stdout_kv = {}
if stdout_log_abs.is_file():
    for line in stdout_log_abs.read_text(encoding="utf-8").splitlines():
        if "=" in line:
            k, v = line.split("=", 1)
            stdout_kv[k.strip()] = v.strip()

source_sql = (repo_root / source_sql_path).read_text(encoding="utf-8")
generated_sql = generated_sql_abs.read_text(encoding="utf-8") if generated_sql_abs.is_file() else ""

row_status = "rewrite_failed"
dialect_rendering_status = stdout_kv.get("dialect_rendering_status", "")
failure_category = ""
blocker_reason = ""
rewrite_changed = None

if rc != 0:
    row_status = "rewrite_failed"
    dialect_rendering_status = dialect_rendering_status or "hep_rewrite_failed"
    failure_category = stdout_kv.get("failure_category", "wrapper_command_failed")
    blocker_reason = stdout_kv.get("blocker_reason", f"wrapper_command_rc_{rc}")
elif not generated_sql.strip():
    row_status = "rewrite_failed"
    if dialect_rendering_status not in {"parser_failed", "hep_rewrite_failed"}:
        dialect_rendering_status = "rendered_sql_missing"
    failure_category = stdout_kv.get("failure_category", "rendered_sql_missing")
    blocker_reason = stdout_kv.get("blocker_reason", "nonempty_sql_not_written")
else:
    rewrite_changed = normalize_sql(source_sql) != normalize_sql(generated_sql)
    row_status = "rewrite_success"
    dialect_rendering_status = dialect_rendering_status or "target_dialect_rendered"
    failure_category = ""
    blocker_reason = ""

payload = {
    "run_id": "calcite_hep_mysql_spark_canary_02",
    "row_key": row_key,
    "case_id": case_id,
    "pool": pool,
    "engine": engine,
    "method_id": method_id,
    "route_id": route_id,
    "canary_denominator_id": canary_denominator_id,
    "claim_boundary": claim_boundary,
    "source_sql_path": source_sql_path,
    "schema_path": None,
    "witness_data_path": witness_data_path,
    "row_status": row_status,
    "dialect_rendering_status": dialect_rendering_status,
    "dialect_class_used": stdout_kv.get("dialect_class_used", dialect_class_used),
    "generated_sql_path": str(generated_sql_abs.relative_to(repo_root)) if generated_sql_abs.is_file() else str(generated_sql_abs.relative_to(repo_root)),
    "log_stdout_path": str(stdout_log_abs.relative_to(repo_root)),
    "log_stderr_path": "",
    "row_metadata_path": str(row_metadata_abs.relative_to(repo_root)),
    "rewrite_changed": rewrite_changed,
    "failure_category": failure_category,
    "blocker_reason": blocker_reason,
    "wrapper_stdout_kv": stdout_kv,
}

row_metadata_abs.parent.mkdir(parents=True, exist_ok=True)
row_metadata_abs.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
PY

    local row_status_out
    row_status_out="$(python - <<'PY' "$abs_row_metadata_path"
import json, sys
print(json.load(open(sys.argv[1], "r", encoding="utf-8"))["row_status"])
PY
)"
    row_status="$row_status_out"
  fi

  if [[ ! -f "$abs_row_metadata_path" ]]; then
    python - <<'PY' "$abs_row_metadata_path" "$row_key" "$case_id" "$pool" "$engine" "$METHOD_ID" "$ROUTE_ID" "$CANARY_DENOMINATOR_ID" "$CLAIM_BOUNDARY" "$source_sql_path" "$schema_path" "$witness_data_path" "$generated_sql_path" "$stdout_log_path" "$stderr_log_path" "$dialect_rendering_status" "$dialect_class_used" "$failure_category" "$blocker_reason"
import json
import sys
from pathlib import Path

out = Path(sys.argv[1])
payload = {
    "run_id": "calcite_hep_mysql_spark_canary_02",
    "row_key": sys.argv[2],
    "case_id": sys.argv[3],
    "pool": sys.argv[4],
    "engine": sys.argv[5],
    "method_id": sys.argv[6],
    "route_id": sys.argv[7],
    "canary_denominator_id": sys.argv[8],
    "claim_boundary": sys.argv[9],
    "source_sql_path": sys.argv[10],
    "schema_path": sys.argv[11],
    "witness_data_path": sys.argv[12],
    "row_status": "preflight_blocked",
    "dialect_rendering_status": sys.argv[15],
    "dialect_class_used": sys.argv[16],
    "generated_sql_path": sys.argv[13],
    "log_stdout_path": sys.argv[14],
    "log_stderr_path": sys.argv[15],
    "row_metadata_path": str(out),
    "rewrite_changed": None,
    "failure_category": sys.argv[17],
    "blocker_reason": sys.argv[18],
}
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
PY
  fi
}

tail -n +2 "$MATRIX_PATH" | while IFS=, read -r row_key case_id pool engine method_id route_id canary_denominator_id source_sql_path schema_path witness_data_path expected_generated_sql_path expected_stdout_log_path expected_stderr_log_path expected_row_metadata_path rewrite_status_planned blocker_or_caveat; do
  run_row \
    "$row_key" \
    "$case_id" \
    "$pool" \
    "$engine" \
    "$source_sql_path" \
    "$schema_path" \
    "$witness_data_path" \
    "$expected_generated_sql_path" \
    "$expected_stdout_log_path" \
    "$expected_stderr_log_path" \
    "$expected_row_metadata_path"
done

python - <<'PY' "$REPO_ROOT" "$RUN_DIR" "$RUN_RESULTS_PATH" "$RUN_EVENT_LONG_PATH" "$mysql_dialect_available" "$spark_dialect_available" "$wrapper_compile_status" "$wrapper_compile_blocker" "$CLAIM_BOUNDARY"
import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

repo_root = Path(sys.argv[1])
run_dir = Path(sys.argv[2])
run_results_path = Path(sys.argv[3])
run_event_long_path = Path(sys.argv[4])
mysql_dialect_available = sys.argv[5] == "true"
spark_dialect_available = sys.argv[6] == "true"
wrapper_compile_status = sys.argv[7]
wrapper_compile_blocker = sys.argv[8]
claim_boundary = sys.argv[9]

event_fields = [
    "run_id",
    "row_key",
    "case_id",
    "pool",
    "engine",
    "method_id",
    "route_id",
    "canary_denominator_id",
    "source_sql_path",
    "schema_path",
    "witness_data_path",
    "row_status",
    "dialect_rendering_status",
    "dialect_class_used",
    "generated_sql_path",
    "log_stdout_path",
    "log_stderr_path",
    "row_metadata_path",
    "rewrite_changed",
    "failure_category",
    "blocker_reason",
    "claim_boundary",
]

rows = []
for path in sorted((run_dir / "metadata").rglob("row_metadata.json")):
    rows.append(json.loads(path.read_text(encoding="utf-8")))

with run_event_long_path.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=event_fields)
    writer.writeheader()
    for row in rows:
        event_row = {field: row.get(field, "") for field in event_fields}
        event_row["claim_boundary"] = claim_boundary
        writer.writerow(event_row)

status_counts = Counter(row["row_status"] for row in rows)
counts_by_engine = defaultdict(lambda: Counter())
for row in rows:
    counts_by_engine[row["engine"]][row["row_status"]] += 1

payload = {
    "run_id": "calcite_hep_mysql_spark_canary_02",
    "method_id": "calcite_hep",
    "route_id": "calcite_hep_same_engine_rewrite",
    "canary_denominator_id": "calcite_hep_mysql_spark_canary_02",
    "planned_rows": len(rows),
    "status_counts": dict(status_counts),
    "counts_by_engine": {engine: dict(counter) for engine, counter in counts_by_engine.items()},
    "target_dialect_availability": {
        "mysql": mysql_dialect_available,
        "spark": spark_dialect_available,
    },
    "wrapper_compile_status": wrapper_compile_status,
    "wrapper_compile_blocker": wrapper_compile_blocker,
    "claim_boundary": claim_boundary,
    "current_benchmark_metric_evidence": False,
    "rows": rows,
}
run_results_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
PY

echo "wrote $RUN_RESULTS_PATH"
