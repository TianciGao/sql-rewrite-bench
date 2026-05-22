#!/usr/bin/env bash
set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../../../../.." && pwd)"
RUN_DIR="${SCRIPT_DIR}"
LOG_DIR="${RUN_DIR}/logs"
WORKSPACE_DIR="${RUN_DIR}/workspaces"
TIMING_DIR="${RUN_DIR}/timings"
MATRIX_CSV="${RUN_DIR}/timing_command_matrix.csv"
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
echo "This full timing run may regenerate run-local workspaces, timing JSON, and logs under ${RUN_DIR}."
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
    "source_sql_path",
    "generated_sql_path",
    "schema_path",
    "witness_data_path",
    "runner_kind",
    "control_source_artifact",
    "expected_timing_output_path",
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
  timing_json_path="${REPO_ROOT}/${expected_timing_output_path}"
  workspace_dir="${WORKSPACE_DIR}/${case_id}/${engine}/${route_id}"
  source_sql="${source_sql_path}"
  generated_sql="${generated_sql_path}"
  witness_path="${witness_data_path}"

  if [[ "$timing_eligible" != "yes" ]]; then
    record_non_execution "$key" "$row_status" "Timing-ineligible row preserved explicitly outside the execution matrix. ${caveat}" "${exclusion_reason}"
    continue
  fi

  mkdir -p "$workspace_dir" "$(dirname "$timing_json_path")"

  case "$runner_kind" in
    pg_inline_psql|postgres_inline_cli)
      run_and_capture_meta \
        "$key" \
        "executed" \
        "python - <<'PY' <postgres timing runner>" \
        "$stdout_log" \
        "$stderr_log" \
        "$timing_json_path" \
        "${exclusion_reason}" \
        python - "$REPO_ROOT" "$case_id" "$route_id" "$source_sql" "$generated_sql" "$schema_path" "$witness_path" "$workspace_dir" "$timing_json_path" "$WARMUP_COUNT" "$REPEAT_COUNT" <<'PY'
from pathlib import Path
import json
import re
import shutil
import statistics
import subprocess
import sys
import time

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

schema_sql = workspace / "ddl_pg.sql"
witness_sql = workspace / "pg_witness_data.sql"
source_copy = workspace / "source.sql"
generated_copy = workspace / "generated.sql"
shutil.copyfile(schema_path, schema_sql)
shutil.copyfile(witness_path, witness_sql)
shutil.copyfile(source_sql, source_copy)
shutil.copyfile(generated_sql, generated_copy)

schema_name = f"ccv0_sqlglot_timing_{case_id.lower()}_{route_id.lower()}"
schema_name = re.sub(r"[^a-z0-9_]", "_", schema_name)[:55]

def run_query(query_path: Path) -> float:
    setup = f"DROP SCHEMA IF EXISTS {schema_name} CASCADE; CREATE SCHEMA {schema_name}; SET search_path TO {schema_name};"
    start = time.perf_counter()
    try:
        subprocess.run(["psql", "-v", "ON_ERROR_STOP=1", "-c", setup, "-f", str(schema_sql)], check=True)
        subprocess.run(["psql", "-v", "ON_ERROR_STOP=1", "-c", f"SET search_path TO {schema_name};", "-f", str(witness_sql)], check=True)
        subprocess.run(["psql", "-v", "ON_ERROR_STOP=1", "-c", f"SET search_path TO {schema_name};", "-f", str(query_path)], check=True)
    finally:
        subprocess.run(["psql", "-v", "ON_ERROR_STOP=1", "-c", f"DROP SCHEMA IF EXISTS {schema_name} CASCADE;"], check=False)
    return (time.perf_counter() - start) * 1000.0

payload = {
    "case_id": case_id,
    "engine": "pg",
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
      ;;
    mysql_inline_cli)
      run_and_capture_meta \
        "$key" \
        "executed" \
        "python - <<'PY' <mysql timing runner>" \
        "$stdout_log" \
        "$stderr_log" \
        "$timing_json_path" \
        "${exclusion_reason}" \
        python - "$REPO_ROOT" "$case_id" "$route_id" "$source_sql" "$generated_sql" "$schema_path" "$witness_path" "$workspace_dir" "$timing_json_path" "$WARMUP_COUNT" "$REPEAT_COUNT" <<'PY'
from pathlib import Path
import json
import os
import re
import shutil
import statistics
import subprocess
import sys
import time

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

schema_sql = workspace / "ddl_mysql.sql"
witness_sql = workspace / "mysql_witness_data.sql"
source_copy = workspace / "source.sql"
generated_copy = workspace / "generated.sql"
shutil.copyfile(schema_path, schema_sql)
shutil.copyfile(witness_path, witness_sql)
shutil.copyfile(source_sql, source_copy)
shutil.copyfile(generated_sql, generated_copy)

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

def extract_table_names(ddl_text: str) -> list[str]:
    pattern = re.compile(
        r"^\s*CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?(?:`([^`]+)`|([A-Za-z_][A-Za-z0-9_]*))",
        re.IGNORECASE | re.MULTILINE,
    )
    out = []
    for match in pattern.finditer(ddl_text):
        name = match.group(1) or match.group(2)
        if name and name not in out:
            out.append(name)
    return out

table_names = extract_table_names(schema_sql.read_text(encoding="utf-8"))
if not table_names:
    raise RuntimeError(f"No MySQL table names detected in DDL: {schema_sql}")

def mysql_exec(sql: str) -> None:
    subprocess.run(mysql_args + [mysql_database, "-e", sql], check=True)

def cleanup_tables(check: bool) -> None:
    if not table_names:
        return
    quoted = ", ".join(f"`{name.replace('`', '``')}`" for name in table_names)
    subprocess.run(
        mysql_args + [mysql_database, "-e", f"DROP TABLE IF EXISTS {quoted};"],
        check=check,
    )

def run_query(query_path: Path) -> float:
    start = time.perf_counter()
    try:
        cleanup_tables(check=True)
        for path in [schema_sql, witness_sql, query_path]:
            subprocess.run(mysql_args + [mysql_database, "-e", f"source {path};"], check=True)
    finally:
        cleanup_tables(check=False)
    return (time.perf_counter() - start) * 1000.0

payload = {
    "case_id": case_id,
    "engine": "mysql",
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
      ;;
    spark_inline_pyspark)
      run_and_capture_meta \
        "$key" \
        "executed" \
        "python - <<'PY' <spark timing runner>" \
        "$stdout_log" \
        "$stderr_log" \
        "$timing_json_path" \
        "${exclusion_reason}" \
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

def run_query(query_path: Path) -> float:
    warehouse_dir = tempfile.mkdtemp(prefix=f"ccv0_sqlglot_timing_{case_id.lower()}_", dir=str(workspace))
    spark = (
        SparkSession.builder
        .master("local[*]")
        .appName(f"ccv0_sqlglot_timing_{case_id.lower()}_{route_id}")
        .config("spark.ui.enabled", "false")
        .config("spark.sql.shuffle.partitions", "1")
        .config("spark.sql.warehouse.dir", warehouse_dir)
        .getOrCreate()
    )
    try:
        start = time.perf_counter()
        for path in [schema_sql, witness_sql, query_path]:
            statements = [s.strip() for s in path.read_text(encoding='utf-8').split(';') if s.strip()]
            for stmt in statements:
                spark.sql(stmt).collect()
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
      ;;
    *)
      record_non_execution "$key" "script_error" "Unknown runner kind: ${runner_kind}" "script_error_unknown_runner"
      ;;
  esac
done < <(
  python - "$MATRIX_CSV" <<'PY'
import csv
import json
import sys
from pathlib import Path

matrix_path = Path(sys.argv[1])
runner_by_engine = {
    "pg": "pg_inline_psql",
    "mysql": "mysql_inline_cli",
    "spark": "spark_inline_pyspark",
}

with matrix_path.open(newline="", encoding="utf-8") as handle:
    reader = csv.DictReader(handle)
    for row in reader:
        row["runner_kind"] = runner_by_engine.get(row["engine"], row.get("runner_kind", ""))
        print(json.dumps(row, ensure_ascii=True))
PY
)

python - "$RECORDS_JSONL" "$RUN_RESULTS_JSON" <<'PY'
import json
import sys
from pathlib import Path

records_path = Path(sys.argv[1])
out_path = Path(sys.argv[2])
records = []
if records_path.exists():
    with records_path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                records.append(json.loads(line))

payload = {
    "run_id": "sqlglot_same_engine_timing_01",
    "mode": "manual_human_full_timing_run",
    "denominator_id": "common_core_v0_40",
    "method_id": "sqlglot",
    "method_role": "same_engine_timing_full_run",
    "run_scope": "sqlglot_same_engine_timing_full_eligible_rows",
    "warmup_count": 1,
    "repeat_count": 3,
    "records": records,
}
out_path.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
PY

echo "Wrote ${RUN_RESULTS_JSON}"
exit 0
