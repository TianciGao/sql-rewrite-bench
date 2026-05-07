#!/usr/bin/env bash
set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../../../../.." && pwd)"
RUN_DIR="${SCRIPT_DIR}"
LOG_DIR="${RUN_DIR}/logs"
WORKSPACE_DIR="${RUN_DIR}/workspaces"
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
echo "This retry only targets PORT_0003 and PORT_0005 PostgreSQL optimize rows."
echo "This script does not compute timing, speedup, leaderboard metrics, or plan artifacts."

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

ENV_STDOUT="${LOG_DIR}/env_check.stdout.log"
ENV_STDERR="${LOG_DIR}/env_check.stderr.log"
run_and_capture \
  "env_check" \
  "executed" \
  "python -m scripts.cli env-check" \
  "$ENV_STDOUT" \
  "$ENV_STDERR" \
  python -m scripts.cli env-check

run_postgres_row() {
  local case_id="$1"
  local source_sql="$2"
  local generated_sql="$3"
  local schema_path="$4"
  local witness_path="$5"
  local key="${case_id,,}__pg__sqlglot_optimize_same_dialect"
  local workspace_dir="${WORKSPACE_DIR}/${case_id}/pg/sqlglot_optimize_same_dialect"
  local stdout_log="${LOG_DIR}/${key}.stdout.log"
  local stderr_log="${LOG_DIR}/${key}.stderr.log"

  mkdir -p "${workspace_dir}"

  run_and_capture \
    "$key" \
    "executed" \
    "python - <<'PY' <postgres runner>" \
    "$stdout_log" \
    "$stderr_log" \
    python - "$REPO_ROOT" "$case_id" "$source_sql" "$generated_sql" "$schema_path" "$witness_path" "$workspace_dir" <<'PY'
from pathlib import Path
import re
import shutil
import subprocess
import sys

root = Path(sys.argv[1])
case_id = sys.argv[2]
source_sql = root / sys.argv[3]
generated_sql = root / sys.argv[4]
schema_path = root / sys.argv[5]
witness_path = root / sys.argv[6]
workspace = root / sys.argv[7]
workspace.mkdir(parents=True, exist_ok=True)

schema_sql = workspace / "ddl_pg.sql"
witness_sql = workspace / "pg_witness_data.sql"
source_copy = workspace / "source.sql"
generated_copy = workspace / "generated.sql"
shutil.copyfile(schema_path, schema_sql)
shutil.copyfile(witness_path, witness_sql)
shutil.copyfile(source_sql, source_copy)
shutil.copyfile(generated_sql, generated_copy)

schema_name = f"ccv0_sqlglot_{case_id.lower()}_sqlglot_optimize_same_dialect"
schema_name = re.sub(r"[^a-z0-9_]", "_", schema_name)[:55]

setup = f"DROP SCHEMA IF EXISTS {schema_name} CASCADE; CREATE SCHEMA {schema_name}; SET search_path TO {schema_name};"
for path in [schema_sql, witness_sql, source_copy, generated_copy]:
    subprocess.run(
        ["psql", "-v", "ON_ERROR_STOP=1", "-c", setup if path == schema_sql else f"SET search_path TO {schema_name};", "-f", str(path)],
        check=True,
    )
subprocess.run(["psql", "-v", "ON_ERROR_STOP=1", "-c", f"DROP SCHEMA IF EXISTS {schema_name} CASCADE;"], check=True)
PY
}

run_postgres_row \
  "PORT_0003" \
  "cases/PORT/PORT_0003/source.sql" \
  "reports/evaluation/common_core_v0/runs/sqlglot_same_engine_generation_01/generated/PORT_0003/pg/sqlglot_optimize_same_dialect.sql" \
  "cases/PORT/PORT_0003/schema/ddl_pg.sql" \
  "cases/PORT/PORT_0003/validation/pg_witness_data.sql"

run_postgres_row \
  "PORT_0005" \
  "cases/PORT/PORT_0005/source.sql" \
  "reports/evaluation/common_core_v0/runs/sqlglot_same_engine_generation_01/generated/PORT_0005/pg/sqlglot_optimize_same_dialect.sql" \
  "cases/PORT/PORT_0005/schema/ddl_pg.sql" \
  "cases/PORT/PORT_0005/validation/pg_witness_data.sql"

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
    "run_id": "sqlglot_same_engine_port_retry_pg_witness_01",
    "mode": "manual_human_execution_retry",
    "denominator_id": "common_core_v0_40",
    "retry_scope": "port_0003_port_0005_pg_sqlglot_optimize_only",
    "records": records,
}
out_path.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
PY

echo "Wrote ${RUN_RESULTS_JSON}"
exit 0
