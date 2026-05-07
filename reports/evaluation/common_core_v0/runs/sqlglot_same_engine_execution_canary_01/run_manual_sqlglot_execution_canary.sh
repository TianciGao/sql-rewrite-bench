#!/usr/bin/env bash
set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../../../../.." && pwd)"
RUN_DIR="${SCRIPT_DIR}"
LOG_DIR="${RUN_DIR}/logs"
WORKSPACE_DIR="${RUN_DIR}/workspaces"
MATRIX_CSV="${RUN_DIR}/execution_command_matrix.csv"
RECORDS_JSONL="${RUN_DIR}/records.tmp.jsonl"
RUN_RESULTS_JSON="${RUN_DIR}/run_results.json"

if [[ "$(pwd)" != "${REPO_ROOT}" ]]; then
  echo "This script must be run from the repository root: ${REPO_ROOT}" >&2
  exit 1
fi

mkdir -p "${LOG_DIR}" "${WORKSPACE_DIR}"
: > "${RECORDS_JSONL}"

echo "Human-run only."
echo "Codex must not execute this script."
echo "This canary may regenerate run-local workspaces and logs under ${RUN_DIR}."
echo "This script does not compute timing, leaderboard metrics, or plan artifacts."

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

run_and_capture() {
  local key="$1"
  local row_status="$2"
  local command="$3"
  local stdout_log="$4"
  local stderr_log="$5"
  shift 5

  local exit_code=0
  "$@" >"$stdout_log" 2>"$stderr_log" || exit_code=$?

  append_record "$(python - "$key" "$row_status" "$command" "$exit_code" "$stdout_log" "$stderr_log" <<'PY'
import json
import sys
print(json.dumps({
    "key": sys.argv[1],
    "row_status": sys.argv[2],
    "command": sys.argv[3],
    "exit_code": int(sys.argv[4]),
    "stdout_log": sys.argv[5],
    "stderr_log": sys.argv[6],
    "notes": "",
}))
PY
)"
}

record_non_execution() {
  local key="$1"
  local row_status="$2"
  local note="$3"
  append_record "$(python - "$key" "$row_status" "$note" <<'PY'
import json
import sys
print(json.dumps({
    "key": sys.argv[1],
    "row_status": sys.argv[2],
    "command": "",
    "exit_code": None,
    "stdout_log": "",
    "stderr_log": "",
    "notes": sys.argv[3],
}))
PY
)"
}

ENV_STDOUT="${LOG_DIR}/env_check.stdout.log"
ENV_STDERR="${LOG_DIR}/env_check.stderr.log"
run_and_capture \
  "env_check" \
  "executed" \
  "python -m scripts.cli env-check" \
  "$ENV_STDOUT" \
  "$ENV_STDERR" \
  python -m scripts.cli env-check

python - "$REPO_ROOT" "$MATRIX_CSV" <<'PY' | while IFS=$'\t' read -r row_key row_status command_kind case_id engine route_id source_sql generated_sql schema_path witness_path workspace_dir stdout_log stderr_log; do
import csv
import sys
from pathlib import Path

root = Path(sys.argv[1])
matrix_path = Path(sys.argv[2])

with matrix_path.open(newline="", encoding="utf-8") as handle:
    reader = csv.DictReader(handle)
    for row in reader:
        key = f"{row['case_id'].lower()}__{row['engine']}__{row['route_id']}"
        stdout_log = root / "reports/evaluation/common_core_v0/runs/sqlglot_same_engine_execution_canary_01/logs" / f"{key}.stdout.log"
        stderr_log = root / "reports/evaluation/common_core_v0/runs/sqlglot_same_engine_execution_canary_01/logs" / f"{key}.stderr.log"
        fields = [
            key,
            row["execution_row_status"],
            row["execution_command_kind"],
            row["case_id"],
            row["engine"],
            row["route_id"],
            row["source_sql_path"],
            row["generated_sql_path"],
            row["schema_path"],
            row["witness_data_path"],
            row["run_local_workspace"],
            str(stdout_log),
            str(stderr_log),
        ]
        print("\t".join(fields))
PY
  if [[ "$row_status" == "not_executed_generation_failed" ]]; then
    record_non_execution "$row_key" "$row_status" "Generation failed earlier; row remains explicit and is not executed."
    continue
  fi

  if [[ "$row_status" == "noop_generated" ]]; then
    record_non_execution "$row_key" "$row_status" "Generated SQL was an explicit no-op output; row remains explicit and is not executed."
    continue
  fi

  mkdir -p "$workspace_dir"

  case "$command_kind" in
    postgres_inline_cli)
      run_and_capture \
        "$row_key" \
        "executed" \
        "python - <<'PY' <postgres runner>" \
        "$stdout_log" \
        "$stderr_log" \
        python - "$REPO_ROOT" "$case_id" "$engine" "$route_id" "$source_sql" "$generated_sql" "$schema_path" "$witness_path" "$workspace_dir" <<'PY'
from pathlib import Path
import re
import shutil
import subprocess
import sys

root = Path(sys.argv[1])
case_id, engine, route_id = sys.argv[2:5]
source_sql = root / sys.argv[5]
generated_sql = root / sys.argv[6]
schema_path = root / sys.argv[7]
witness_path = root / sys.argv[8]
workspace = root / sys.argv[9]
workspace.mkdir(parents=True, exist_ok=True)

schema_sql = (workspace / "ddl_pg.sql")
witness_sql = (workspace / "pg_witness_data.sql")
source_copy = (workspace / "source.sql")
generated_copy = (workspace / "generated.sql")
shutil.copyfile(schema_path, schema_sql)
shutil.copyfile(witness_path, witness_sql)
shutil.copyfile(source_sql, source_copy)
shutil.copyfile(generated_sql, generated_copy)

schema_name = f"ccv0_sqlglot_{case_id.lower()}_{route_id.lower()}"
schema_name = re.sub(r"[^a-z0-9_]", "_", schema_name)[:55]

setup = f"DROP SCHEMA IF EXISTS {schema_name} CASCADE; CREATE SCHEMA {schema_name}; SET search_path TO {schema_name};"
for path in [schema_sql, witness_sql, source_copy, generated_copy]:
    subprocess.run(["psql", "-v", "ON_ERROR_STOP=1", "-c", setup if path == schema_sql else f"SET search_path TO {schema_name};", "-f", str(path)], check=True)
subprocess.run(["psql", "-v", "ON_ERROR_STOP=1", "-c", f"DROP SCHEMA IF EXISTS {schema_name} CASCADE;"], check=True)
PY
      ;;
    mysql_inline_cli)
      run_and_capture \
        "$row_key" \
        "executed" \
        "python - <<'PY' <mysql runner>" \
        "$stdout_log" \
        "$stderr_log" \
        python - "$REPO_ROOT" "$case_id" "$engine" "$route_id" "$source_sql" "$generated_sql" "$schema_path" "$witness_path" "$workspace_dir" <<'PY'
from pathlib import Path
import re
import shutil
import subprocess
import sys

root = Path(sys.argv[1])
case_id, engine, route_id = sys.argv[2:5]
source_sql = root / sys.argv[5]
generated_sql = root / sys.argv[6]
schema_path = root / sys.argv[7]
witness_path = root / sys.argv[8]
workspace = root / sys.argv[9]
workspace.mkdir(parents=True, exist_ok=True)

schema_sql = (workspace / "ddl_mysql.sql")
witness_sql = (workspace / "mysql_witness_data.sql")
source_copy = (workspace / "source.sql")
generated_copy = (workspace / "generated.sql")
shutil.copyfile(schema_path, schema_sql)
shutil.copyfile(witness_path, witness_sql)
shutil.copyfile(source_sql, source_copy)
shutil.copyfile(generated_sql, generated_copy)

db_name = f"ccv0_sqlglot_{case_id.lower()}_{route_id.lower()}"
db_name = re.sub(r"[^a-z0-9_]", "_", db_name)[:55]

subprocess.run(["mysql", "-e", f"DROP DATABASE IF EXISTS `{db_name}`; CREATE DATABASE `{db_name}`;"], check=True)
for path in [schema_sql, witness_sql, source_copy, generated_copy]:
    subprocess.run(["mysql", db_name, "-e", f"source {path};"], check=True)
subprocess.run(["mysql", "-e", f"DROP DATABASE IF EXISTS `{db_name}`;"], check=True)
PY
      ;;
    spark_inline_pyspark)
      run_and_capture \
        "$row_key" \
        "executed" \
        "python - <<'PY' <spark runner>" \
        "$stdout_log" \
        "$stderr_log" \
        python - "$REPO_ROOT" "$case_id" "$engine" "$route_id" "$source_sql" "$generated_sql" "$schema_path" "$witness_path" "$workspace_dir" <<'PY'
from pathlib import Path
import shutil
import sys
import tempfile

from pyspark.sql import SparkSession

root = Path(sys.argv[1])
case_id, engine, route_id = sys.argv[2:5]
source_sql = root / sys.argv[5]
generated_sql = root / sys.argv[6]
schema_path = root / sys.argv[7]
witness_path = root / sys.argv[8]
workspace = root / sys.argv[9]
workspace.mkdir(parents=True, exist_ok=True)

schema_sql = workspace / "ddl_spark.sql"
witness_sql = workspace / "spark_witness_data.sql"
source_copy = workspace / "source.sql"
generated_copy = workspace / "generated.sql"
shutil.copyfile(schema_path, schema_sql)
shutil.copyfile(witness_path, witness_sql)
shutil.copyfile(source_sql, source_copy)
shutil.copyfile(generated_sql, generated_copy)

warehouse_dir = tempfile.mkdtemp(prefix=f"ccv0_sqlglot_{case_id.lower()}_", dir=str(workspace))
spark = (
    SparkSession.builder
    .master("local[*]")
    .appName(f"ccv0_sqlglot_{case_id.lower()}_{route_id}")
    .config("spark.ui.enabled", "false")
    .config("spark.sql.shuffle.partitions", "1")
    .config("spark.sql.warehouse.dir", warehouse_dir)
    .getOrCreate()
)
try:
    for path in [schema_sql, witness_sql, source_copy, generated_copy]:
        text = path.read_text(encoding="utf-8")
        statements = [s.strip() for s in text.split(";") if s.strip()]
        for stmt in statements:
            spark.sql(stmt).collect()
finally:
    spark.stop()
PY
      ;;
    *)
      record_non_execution "$row_key" "script_error" "Unknown command kind: $command_kind"
      ;;
  esac
done

python - "$RECORDS_JSONL" "$RUN_RESULTS_JSON" <<'PY'
import json
import sys
from pathlib import Path

records_path = Path(sys.argv[1])
output_path = Path(sys.argv[2])
records = []
if records_path.exists():
    with records_path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                records.append(json.loads(line))
payload = {
    "run_id": "sqlglot_same_engine_execution_canary_01",
    "mode": "manual_human_execution",
    "repo_root": str(Path.cwd()),
    "case_scope": ["PERF_0006", "CONS_0007", "LONGTAIL_0011"],
    "engine_scope": ["pg", "mysql", "spark"],
    "route_scope": [
        "sqlglot_optimize_same_dialect",
        "sqlglot_transpile_same_dialect_noop",
    ],
    "records": records,
}
output_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
PY

exit 0
