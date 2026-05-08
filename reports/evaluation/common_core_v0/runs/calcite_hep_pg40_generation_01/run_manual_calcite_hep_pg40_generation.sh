#!/usr/bin/env bash
set -u

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")"/../../../../../.. && pwd)"
RUN_DIR="$ROOT_DIR/reports/evaluation/common_core_v0/runs/calcite_hep_pg40_generation_01"
MATRIX_PATH="$RUN_DIR/generation_command_matrix.csv"
LOG_DIR="$RUN_DIR/logs"
ROW_RESULT_DIR="$RUN_DIR/row_results"
GENERATED_DIR="$RUN_DIR/generated"
RUN_RESULTS_PATH="$RUN_DIR/run_results.json"

CALCITE_CHECKOUT_ROOT="${CALCITE_CHECKOUT_ROOT:-$ROOT_DIR/datasets/raw/calcite/calcite}"
CALCITE_WRAPPER_SOURCE="$ROOT_DIR/tools/calcite_hep/CalciteHepRewriteSmoke.java"
CALCITE_WORK_ROOT="${CALCITE_WORK_ROOT:-/tmp/calcite-hep-pg40-generation}"
GRADLE_USER_HOME="${GRADLE_USER_HOME:-/tmp/calcite-gradle-home}"
WRAPPER_CLASSES_DIR="$CALCITE_WORK_ROOT/classes"
WRAPPER_CLASSPATH_FILE="$CALCITE_WORK_ROOT/wrapper_classpath.txt"

if [[ "$(pwd)" != "$ROOT_DIR" ]]; then
  echo "run from repo root: $ROOT_DIR" >&2
  exit 1
fi

mkdir -p "$LOG_DIR" "$ROW_RESULT_DIR" "$GENERATED_DIR" "$CALCITE_WORK_ROOT"

wrapper_status="present"
wrapper_blocker=""

if [[ ! -f "$CALCITE_WRAPPER_SOURCE" ]]; then
  wrapper_status="missing"
  wrapper_blocker="wrapper_source_missing:$CALCITE_WRAPPER_SOURCE"
fi

if [[ ! -d "$CALCITE_CHECKOUT_ROOT" ]]; then
  wrapper_status="missing"
  if [[ -n "$wrapper_blocker" ]]; then
    wrapper_blocker="$wrapper_blocker;calcite_checkout_missing:$CALCITE_CHECKOUT_ROOT"
  else
    wrapper_blocker="calcite_checkout_missing:$CALCITE_CHECKOUT_ROOT"
  fi
fi

if [[ "$wrapper_status" == "present" ]]; then
  (
    set -e
    cd "$CALCITE_CHECKOUT_ROOT"
    export GRADLE_USER_HOME
    ./gradlew :core:classes >/dev/null
  ) || {
    wrapper_status="missing"
    wrapper_blocker="gradle_core_classes_failed"
  }
fi

if [[ "$wrapper_status" == "present" ]]; then
  mkdir -p "$WRAPPER_CLASSES_DIR"
  CLASSPATH_CORE="$CALCITE_CHECKOUT_ROOT/core/build/classes/java/main:$CALCITE_CHECKOUT_ROOT/core/build/resources/main:$CALCITE_CHECKOUT_ROOT/linq4j/build/classes/java/main"
  CLASSPATH_JARS="$(find "$GRADLE_USER_HOME/caches/modules-2/files-2.1" -name '*.jar' -print | sort | paste -sd: -)"
  FULL_CLASSPATH="$WRAPPER_CLASSES_DIR:$CLASSPATH_CORE:$CLASSPATH_JARS"
  printf '%s' "$FULL_CLASSPATH" > "$WRAPPER_CLASSPATH_FILE"
  javac -cp "$CLASSPATH_CORE:$CLASSPATH_JARS" -d "$WRAPPER_CLASSES_DIR" "$CALCITE_WRAPPER_SOURCE" || {
    wrapper_status="missing"
    wrapper_blocker="wrapper_compile_failed"
  }
fi

run_row() {
  local case_id="$1"
  local pool="$2"
  local engine="$3"
  local route_id="$4"
  local source_sql_path="$5"
  local schema_path="$6"
  local expected_generated_sql_path="$7"
  local caveat="$8"

  local stdout_log="$LOG_DIR/${case_id}_${engine}.stdout.log"
  local stderr_log="$LOG_DIR/${case_id}_${engine}.stderr.log"
  local row_dir="$ROW_RESULT_DIR/$case_id/$engine"
  local row_result_path="$row_dir/result.json"
  mkdir -p "$row_dir" "$(dirname "$expected_generated_sql_path")"

  if [[ "$wrapper_status" != "present" ]]; then
    python - <<PY
import json, os
payload = {
  "case_id": ${case_id@Q},
  "pool": ${pool@Q},
  "engine": ${engine@Q},
  "route_id": ${route_id@Q},
  "source_sql_path": ${source_sql_path@Q},
  "schema_path": ${schema_path@Q},
  "generated_sql_path": ${expected_generated_sql_path@Q},
  "stdout_log_path": ${stdout_log@Q},
  "stderr_log_path": ${stderr_log@Q},
  "generation_status": "blocked_runner_missing",
  "blocker_reason": ${wrapper_blocker@Q},
  "caveat": ${caveat@Q},
  "is_noop": None
}
os.makedirs(os.path.dirname(${row_result_path@Q}), exist_ok=True)
with open(${row_result_path@Q}, "w", encoding="utf-8") as fh:
    json.dump(payload, fh, indent=2, ensure_ascii=True)
    fh.write("\\n")
PY
    return
  fi

  java -cp "$(cat "$WRAPPER_CLASSPATH_FILE")" \
    CalciteHepRewriteSmoke \
    --mode real_route_canary \
    --case-id "$case_id" \
    --source-sql "$ROOT_DIR/$source_sql_path" \
    --ddl "$ROOT_DIR/$schema_path" \
    --output-sql "$ROOT_DIR/$expected_generated_sql_path" \
    >"$stdout_log" 2>"$stderr_log"
  local rc=$?

  python - <<PY
import json, os, re

case_id = ${case_id@Q}
pool = ${pool@Q}
engine = ${engine@Q}
route_id = ${route_id@Q}
source_path = os.path.join(${ROOT_DIR@Q}, ${source_sql_path@Q})
schema_path = os.path.join(${ROOT_DIR@Q}, ${schema_path@Q})
generated_path = os.path.join(${ROOT_DIR@Q}, ${expected_generated_sql_path@Q})
stdout_path = ${stdout_log@Q}
stderr_path = ${stderr_log@Q}
row_result_path = ${row_result_path@Q}
caveat = ${caveat@Q}
rc = ${rc}

def normalize_sql(text: str) -> str:
    text = text.strip()
    if text.endswith(";"):
        text = text[:-1]
    text = re.sub(r"\\s+", " ", text).strip()
    return text

stdout_kv = {}
if os.path.isfile(stdout_path):
    with open(stdout_path, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.rstrip("\\n")
            if "=" in line:
                k, v = line.split("=", 1)
                stdout_kv[k.strip()] = v.strip()

with open(source_path, "r", encoding="utf-8") as fh:
    source_sql = fh.read()

generated_sql = ""
if os.path.isfile(generated_path):
    with open(generated_path, "r", encoding="utf-8") as fh:
        generated_sql = fh.read()

status = "generation_failed_command"
blocker_reason = ""
is_noop = None

if rc != 0:
    status = "generation_failed_command"
    blocker_reason = f"wrapper_command_rc_{rc}"
elif not generated_sql.strip():
    blocker_stage = stdout_kv.get("blocker_stage", "")
    blocker_message = stdout_kv.get("blocker_message", "")
    if stdout_kv.get("calcite_parse_succeeded") == "false":
        status = "generation_failed_parse"
    elif blocker_stage in {"validate", "sql_to_rel", "hep_planner", "rel_to_sql", "schema_ingestion"}:
        status = "generation_failed_unsupported_sql"
    else:
        status = "generation_failed_no_output"
    blocker_reason = blocker_message or blocker_stage or "no_output_sql_emitted"
else:
    is_noop = normalize_sql(source_sql) == normalize_sql(generated_sql)
    if stdout_kv.get("emission_mode") == "calcite_rel_to_sql" and stdout_kv.get("candidate_sql_emitted") == "true":
        status = "generation_success_noop" if is_noop else "generation_success"
    else:
        status = "generation_success_noop" if is_noop else "generation_failed_unsupported_sql"
        blocker_reason = stdout_kv.get("emission_mode", "non_calcite_rel_to_sql_output")

payload = {
    "case_id": case_id,
    "pool": pool,
    "engine": engine,
    "route_id": route_id,
    "source_sql_path": ${source_sql_path@Q},
    "schema_path": ${schema_path@Q},
    "generated_sql_path": ${expected_generated_sql_path@Q},
    "stdout_log_path": os.path.relpath(stdout_path, ${ROOT_DIR@Q}),
    "stderr_log_path": os.path.relpath(stderr_path, ${ROOT_DIR@Q}),
    "generation_status": status,
    "blocker_reason": blocker_reason,
    "caveat": caveat,
    "is_noop": is_noop,
    "wrapper_stdout_kv": stdout_kv,
}

os.makedirs(os.path.dirname(row_result_path), exist_ok=True)
with open(row_result_path, "w", encoding="utf-8") as fh:
    json.dump(payload, fh, indent=2, ensure_ascii=True)
    fh.write("\\n")
PY
}

tail -n +2 "$MATRIX_PATH" | while IFS=, read -r case_id pool engine route_id source_sql_path schema_path calcite_wrapper_available expected_generated_sql_path generation_status exclusion_reason caveat; do
  run_row "$case_id" "$pool" "$engine" "$route_id" "$source_sql_path" "$schema_path" "$expected_generated_sql_path" "$caveat"
done

python - <<PY
import csv, json, os
from collections import Counter

root = ${ROOT_DIR@Q}
run_dir = ${RUN_DIR@Q}
matrix_path = ${MATRIX_PATH@Q}
row_root = os.path.join(run_dir, "row_results")
rows = []
for dirpath, _, filenames in os.walk(row_root):
    for name in filenames:
        if name == "result.json":
            with open(os.path.join(dirpath, name), "r", encoding="utf-8") as fh:
                rows.append(json.load(fh))
rows.sort(key=lambda r: (r["case_id"], r["engine"]))
counts = Counter(r["generation_status"] for r in rows)
payload = {
    "denominator_id": "common_core_v0_40_pg40",
    "method_id": "calcite_hep",
    "route_id": "calcite_hep_pg_rewrite",
    "planned_rows": 40,
    "engine": "pg",
    "wrapper_status": ${wrapper_status@Q},
    "wrapper_blocker": ${wrapper_blocker@Q},
    "matrix_path": os.path.relpath(matrix_path, root),
    "row_count": len(rows),
    "counts_by_generation_status": dict(counts),
    "rows": rows,
}
with open(${RUN_RESULTS_PATH@Q}, "w", encoding="utf-8") as fh:
    json.dump(payload, fh, indent=2, ensure_ascii=True)
    fh.write("\\n")
PY

echo "wrote $RUN_RESULTS_PATH"
