#!/usr/bin/env bash
set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../../../../.." && pwd)"
RUN_DIR="${SCRIPT_DIR}"
LOG_DIR="${RUN_DIR}/logs"
WORKSPACE_DIR="${RUN_DIR}/workspaces"
TIMING_DIR="${RUN_DIR}/timings"
MATRIX_CSV="${RUN_DIR}/retry_command_matrix.csv"
RECORDS_JSONL="${RUN_DIR}/records.tmp.jsonl"
RUN_RESULTS_JSON="${RUN_DIR}/run_results.json"
WARMUP_COUNT=1
REPEAT_COUNT=3

if [[ "$(pwd)" != "${REPO_ROOT}" ]]; then
  echo "This script must be run from the repository root: ${REPO_ROOT}" >&2
  exit 1
fi

mkdir -p "${LOG_DIR}" "${WORKSPACE_DIR}" "${TIMING_DIR}"
: > "${RECORDS_JSONL}"

echo "Human-run only."
echo "Codex must not execute this script."
echo "This targeted retry may regenerate run-local workspaces, timing JSON, and logs under ${RUN_DIR}."
echo "This script does not compute final GM_Speedup, RegressionRate@20%, or any final leaderboard."

source "${REPO_ROOT}/scripts/env_postgres.sh"
source "${REPO_ROOT}/scripts/env_mysql.sh"
source "${REPO_ROOT}/scripts/env_spark.sh"

append_record() {
  local record_json="$1"
  python - "$RECORDS_JSONL" "$record_json" <<'PY'
import json
import sys
from pathlib import Path

path = Path(sys.argv[1])
record = json.loads(sys.argv[2])
with path.open("a", encoding="utf-8") as handle:
    handle.write(json.dumps(record, ensure_ascii=True) + "\n")
PY
}

run_and_capture_meta() {
  local key="$1"
  local row_status="$2"
  local command="$3"
  local stdout_log="$4"
  local stderr_log="$5"
  local timing_json_path="$6"
  local speedup_exclusion_reason="$7"
  shift 7

  local exit_code=0
  "$@" >"$stdout_log" 2>"$stderr_log" || exit_code=$?

  append_record "$(python - "$key" "$row_status" "$command" "$exit_code" "$stdout_log" "$stderr_log" "$timing_json_path" "$speedup_exclusion_reason" <<'PY'
import json
import sys
from pathlib import Path

timing_path = Path(sys.argv[7])
timing_payload = {}
if timing_path.exists():
    try:
        timing_payload = json.loads(timing_path.read_text(encoding="utf-8"))
    except Exception:
        timing_payload = {}

print(json.dumps({
    "key": sys.argv[1],
    "row_status": sys.argv[2],
    "command": sys.argv[3],
    "exit_code": int(sys.argv[4]),
    "stdout_log": sys.argv[5],
    "stderr_log": sys.argv[6],
    "timing_json_path": sys.argv[7],
    "speedup_exclusion_reason": sys.argv[8],
    "source_runtime_ms": timing_payload.get("source_runtime_ms", []),
    "generated_runtime_ms": timing_payload.get("generated_runtime_ms", []),
    "median_source_ms": timing_payload.get("median_source_ms"),
    "median_generated_ms": timing_payload.get("median_generated_ms"),
    "speedup_ratio": timing_payload.get("speedup_ratio"),
    "notes": timing_payload.get("notes", ""),
}))
PY
)"
}

record_non_execution() {
  local key="$1"
  local row_status="$2"
  local note="$3"
  local exclusion_reason="$4"
  append_record "$(python - "$key" "$row_status" "$note" "$exclusion_reason" <<'PY'
import json
import sys
print(json.dumps({
    "key": sys.argv[1],
    "row_status": sys.argv[2],
    "command": "",
    "exit_code": None,
    "stdout_log": "",
    "stderr_log": "",
    "timing_json_path": "",
    "speedup_exclusion_reason": sys.argv[4],
    "source_runtime_ms": [],
    "generated_runtime_ms": [],
    "median_source_ms": None,
    "median_generated_ms": None,
    "speedup_ratio": None,
    "notes": sys.argv[3],
}))
PY
)"
}

ENV_STDOUT="${LOG_DIR}/env_check.stdout.log"
ENV_STDERR="${LOG_DIR}/env_check.stderr.log"
run_and_capture_meta \
  "env_check" \
  "executed" \
  "python -m scripts.cli env-check" \
  "$ENV_STDOUT" \
  "$ENV_STDERR" \
  "" \
  "not_applicable_env_check" \
  python -m scripts.cli env-check

while IFS= read -r row_json; do
  eval "$(
    python - "$row_json" <<'PY'
import json
import shlex
import sys

row = json.loads(sys.argv[1])
fields = [
    "case_id",
    "pool",
    "engine",
    "route_id",
    "timing_eligible",
    "speedup_eligible",
    "exclusion_reason",
    "retry_reason",
    "source_sql_path",
    "generated_sql_path",
    "schema_path",
    "witness_data_path",
    "expected_retry_timing_output_path",
    "row_status",
    "caveat",
]
for field in fields:
    print(f"{field}={shlex.quote(str(row.get(field, '')))}")
PY
  )"
  key="${case_id,,}__${engine}__${route_id}"
  stdout_log="${LOG_DIR}/${key}.stdout.log"
  stderr_log="${LOG_DIR}/${key}.stderr.log"
  timing_json_path="${REPO_ROOT}/${expected_retry_timing_output_path}"
  workspace_dir="${WORKSPACE_DIR}/${case_id}/${engine}/${route_id}"
  source_sql="${source_sql_path}"
  generated_sql="${generated_sql_path}"
  witness_path="${witness_data_path}"

  if [[ "$engine" != "spark" ]]; then
    record_non_execution "$key" "skipped_non_spark" "Retry package is Spark-only. ${caveat}" "retry_scope_non_spark"
    continue
  fi

  if [[ "$timing_eligible" != "yes" ]]; then
    record_non_execution "$key" "$row_status" "Timing-ineligible row preserved explicitly in retry scope. ${caveat}" "${exclusion_reason}"
    continue
  fi

  mkdir -p "$workspace_dir" "$(dirname "$timing_json_path")"

  run_and_capture_meta \
    "$key" \
    "executed" \
    "python - <<'PY' <spark timing retry runner>" \
    "$stdout_log" \
    "$stderr_log" \
    "$timing_json_path" \
    "${retry_reason}" \
    python - "$REPO_ROOT" "$case_id" "$route_id" "$source_sql" "$generated_sql" "$schema_path" "$witness_path" "$workspace_dir" "$timing_json_path" "$WARMUP_COUNT" "$REPEAT_COUNT" <<'PY'
from pathlib import Path
import json
import shutil
import statistics
import sys
import tempfile
import time

from pyspark.sql import SparkSession

root = Path(sys.argv[1])
case_id = sys.argv[2]
route_id = sys.argv[3]
source_sql = root / sys.argv[4]
generated_sql = root / sys.argv[5]
schema_path = root / sys.argv[6]
witness_path = root / sys.argv[7]
workspace = root / sys.argv[8]
timing_json_path = root / sys.argv[9]
warmup_count = int(sys.argv[10])
repeat_count = int(sys.argv[11])
workspace.mkdir(parents=True, exist_ok=True)
timing_json_path.parent.mkdir(parents=True, exist_ok=True)

schema_sql = workspace / "ddl_spark.sql"
witness_sql = workspace / "spark_witness_data.sql"
source_copy = workspace / "source.sql"
generated_copy = workspace / "generated.sql"
shutil.copyfile(schema_path, schema_sql)
shutil.copyfile(witness_path, witness_sql)
shutil.copyfile(source_sql, source_copy)
shutil.copyfile(generated_sql, generated_copy)

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

def load_single_query(query_path: Path) -> str:
    statements = split_sql_script(query_path.read_text(encoding="utf-8"))
    if not statements:
        raise RuntimeError(f"No Spark query detected in {query_path}")
    if len(statements) != 1:
        raise RuntimeError(f"Expected exactly one Spark query in {query_path}, found {len(statements)}")
    return statements[0]

def run_query(query_path: Path) -> float:
    warehouse_dir = tempfile.mkdtemp(prefix=f"ccv0_direct_llm_timing_retry_{case_id.lower()}_", dir=str(workspace))
    spark = (
        SparkSession.builder
        .master("local[*]")
        .appName(f"ccv0_direct_llm_timing_retry_{case_id.lower()}_{route_id}")
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
        spark.sql(load_single_query(query_path)).collect()
        return (time.perf_counter() - start) * 1000.0
    finally:
        spark.stop()

payload = {
    "case_id": case_id,
    "engine": "spark",
    "route_id": route_id,
    "warmup_count": warmup_count,
    "repeat_count": repeat_count,
    "source_runtime_ms": [],
    "generated_runtime_ms": [],
    "median_source_ms": None,
    "median_generated_ms": None,
    "speedup_ratio": None,
    "status": "failure",
    "notes": "",
}

try:
    for _ in range(warmup_count):
        run_query(source_copy)
        run_query(generated_copy)
    for _ in range(repeat_count):
        payload["source_runtime_ms"].append(run_query(source_copy))
        payload["generated_runtime_ms"].append(run_query(generated_copy))
    payload["median_source_ms"] = statistics.median(payload["source_runtime_ms"])
    payload["median_generated_ms"] = statistics.median(payload["generated_runtime_ms"])
    if payload["median_generated_ms"] and payload["median_generated_ms"] > 0:
        payload["speedup_ratio"] = payload["median_source_ms"] / payload["median_generated_ms"]
    payload["status"] = "success"
except Exception as exc:
    payload["notes"] = f"timing_runner_failed: {exc}"
    timing_json_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    raise

timing_json_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
PY
done < <(
  python - "$MATRIX_CSV" <<'PY'
import csv
import json
import sys
from pathlib import Path

matrix_path = Path(sys.argv[1])
with matrix_path.open(newline="", encoding="utf-8") as handle:
    reader = csv.DictReader(handle)
    for row in reader:
        print(json.dumps(row, ensure_ascii=True))
PY
)

python - "$RECORDS_JSONL" "$RUN_RESULTS_JSON" <<'PY'
import json
import sys
from pathlib import Path

records_path = Path(sys.argv[1])
run_results_path = Path(sys.argv[2])
records = []
if records_path.exists():
    with records_path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                records.append(json.loads(line))

payload = {
    "run_id": "direct_llm_same_engine_timing_retry_spark_perf5_01",
    "denominator_id": "common_core_v0_40",
    "method_id": "direct_llm",
    "route_id": "direct_llm_same_engine_rewrite",
    "engine_scope": ["spark"],
    "retry_case_ids": ["PERF_0008", "PERF_0013", "PERF_0017", "PERF_0019", "PERF_0024"],
    "warmup_count": 1,
    "repeat_count": 3,
    "compute_final_gm_speedup": False,
    "compute_regression_rate": False,
    "compute_leaderboard": False,
    "records": records,
}
run_results_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
PY

rm -f "${RECORDS_JSONL}"

echo "Targeted Direct LLM Spark timing retry package complete."
echo "Review ${RUN_RESULTS_JSON} and ${TIMING_DIR}/ for per-row artifacts."
