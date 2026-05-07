#!/usr/bin/env bash
set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../../../../" && pwd)"
LOG_DIR="$SCRIPT_DIR/logs"
RESULTS_JSON="$SCRIPT_DIR/run_results.json"
RECORDS_TMP_JSONL="$SCRIPT_DIR/records.tmp.jsonl"
DENOMINATOR_CSV="$REPO_ROOT/reports/curation/common_core_v0_final_denominator.csv"

if [[ "$(pwd)" != "$REPO_ROOT" ]]; then
  echo "This script must be run from the repository root."
  echo "Expected: $REPO_ROOT"
  echo "Current:  $(pwd)"
  exit 2
fi

if [[ ! -f "$DENOMINATOR_CSV" ]]; then
  echo "Missing denominator CSV: $DENOMINATOR_CSV"
  exit 2
fi

mkdir -p "$LOG_DIR"
: >"$RECORDS_TMP_JSONL"

echo "Manual controls run: full frozen Common-core v0 denominator, PG/MySQL validation only"
echo "This script is intended for a human to run from the real repo root."
echo "Warning: case-local files under cases/.../runs may be regenerated."
echo "Do not git add anything from this run until the results are reviewed."
echo

source scripts/env_postgres.sh
source scripts/env_mysql.sh
source scripts/env_spark.sh

declare -a RECORD_KEYS=()
declare -a RECORD_STATUSES=()
declare -a RECORD_COMMANDS=()
declare -a RECORD_EXIT_CODES=()
declare -a RECORD_STDOUT_LOGS=()
declare -a RECORD_STDERR_LOGS=()
declare -a RECORD_NOTES=()

append_record() {
  local key="$1"
  local status="$2"
  local command="$3"
  local exit_code="$4"
  local stdout_log="$5"
  local stderr_log="$6"
  local notes="$7"

  RECORD_KEYS+=( "$key" )
  RECORD_STATUSES+=( "$status" )
  RECORD_COMMANDS+=( "$command" )
  RECORD_EXIT_CODES+=( "$exit_code" )
  RECORD_STDOUT_LOGS+=( "$stdout_log" )
  RECORD_STDERR_LOGS+=( "$stderr_log" )
  RECORD_NOTES+=( "$notes" )

  python - "$RECORDS_TMP_JSONL" "$key" "$status" "$command" "$exit_code" "$stdout_log" "$stderr_log" "$notes" <<'PY'
import json
import sys
from pathlib import Path

path = Path(sys.argv[1])
record = {
    "key": sys.argv[2],
    "status": sys.argv[3],
    "command": sys.argv[4],
    "exit_code": None if sys.argv[5] == "" else int(sys.argv[5]),
    "stdout_log": sys.argv[6],
    "stderr_log": sys.argv[7],
    "notes": sys.argv[8],
}
with path.open("a", encoding="utf-8") as fh:
    fh.write(json.dumps(record, ensure_ascii=False) + "\n")
PY
}

run_and_record() {
  local key="$1"
  shift
  local cmd=( "$@" )
  local stdout_log="$LOG_DIR/${key}.stdout.log"
  local stderr_log="$LOG_DIR/${key}.stderr.log"
  local exit_code=0
  local command_str

  command_str="$(printf '%q ' "${cmd[@]}")"

  echo "==> Running [$key]"
  printf 'Command: %s\n' "$command_str"

  if "${cmd[@]}" >"$stdout_log" 2>"$stderr_log"; then
    exit_code=0
  else
    exit_code=$?
  fi

  append_record \
    "$key" \
    "executed" \
    "${command_str% }" \
    "$exit_code" \
    "${stdout_log#$REPO_ROOT/}" \
    "${stderr_log#$REPO_ROOT/}" \
    ""

  echo "Exit code: $exit_code"
  echo "stdout: ${stdout_log#$REPO_ROOT/}"
  echo "stderr: ${stderr_log#$REPO_ROOT/}"
  echo
}

record_missing_script() {
  local key="$1"
  local command_str="$2"
  local stdout_log="$LOG_DIR/${key}.stdout.log"
  local stderr_log="$LOG_DIR/${key}.stderr.log"
  local note="missing_script"

  : >"$stdout_log"
  printf '%s\n' "$note" >"$stderr_log"

  append_record \
    "$key" \
    "missing_script" \
    "$command_str" \
    "" \
    "${stdout_log#$REPO_ROOT/}" \
    "${stderr_log#$REPO_ROOT/}" \
    "$note"

  echo "==> Skipping [$key]"
  echo "Reason: missing script"
  echo "Expected command: $command_str"
  echo
}

maybe_run_validation() {
  local pool_dir="$1"
  local case_id="$2"
  local engine="$3"
  local script_path="cases/${pool_dir}/${case_id}/validation/run_${engine}_validation.sh"
  local key="${case_id,,}_${engine}_validation"
  local command_str="bash ${script_path}"

  if [[ -f "$script_path" ]]; then
    run_and_record "$key" bash "$script_path"
  else
    record_missing_script "$key" "$command_str"
  fi
}

run_and_record "env_check" python -m scripts.cli env-check

while IFS=$'\t' read -r case_id pool_dir; do
  maybe_run_validation "$pool_dir" "$case_id" "pg"
  maybe_run_validation "$pool_dir" "$case_id" "mysql"
done < <(
  python - "$DENOMINATOR_CSV" <<'PY'
import csv
import sys
from pathlib import Path

path = Path(sys.argv[1])
pool_to_dir = {
    "performance": "PERF",
    "consistency": "CONS",
    "portability": "PORT",
    "longtail": "LONGTAIL",
}

with path.open(newline="", encoding="utf-8") as fh:
    rows = list(csv.DictReader(fh))

if len(rows) != 40:
    raise SystemExit(f"Expected 40 denominator rows, found {len(rows)}")

for row in rows:
    case_id = row["case_id"].strip()
    pool = row["pool"].strip()
    pool_dir = pool_to_dir.get(pool)
    if not pool_dir:
      raise SystemExit(f"Unknown pool {pool!r} for case {case_id}")
    print(f"{case_id}\t{pool_dir}")
PY
)

export RESULTS_JSON
export REPO_ROOT
export RECORDS_TMP_JSONL

python - <<'PY'
import json
import os
from pathlib import Path

records_tmp = Path(os.environ["RECORDS_TMP_JSONL"])
records = []
if records_tmp.exists():
    for line in records_tmp.read_text(encoding="utf-8").splitlines():
        if line.strip():
            records.append(json.loads(line))

Path(os.environ["RESULTS_JSON"]).write_text(
    json.dumps(
        {
            "run_id": "controls_v0_manual_pg_mysql_40_01",
            "mode": "manual_human_execution",
            "repo_root": os.environ["REPO_ROOT"],
            "denominator_id": "common_core_v0_40",
            "case_scope": "full_frozen_common_core_v0_40",
            "engine_scope": ["pg", "mysql"],
            "records": records,
        },
        indent=2,
    )
    + "\n",
    encoding="utf-8",
)
PY

echo "Summary"
printf '  %s\n' "run_results.json: ${RESULTS_JSON#$REPO_ROOT/}"
for idx in "${!RECORD_KEYS[@]}"; do
  printf '  %-40s status=%-14s exit=%s\n' \
    "${RECORD_KEYS[$idx]}" \
    "${RECORD_STATUSES[$idx]}" \
    "${RECORD_EXIT_CODES[$idx]:-}"
done

echo
echo "Manual PG/MySQL controls run complete. Review logs and run_results.json before any follow-on materialization."
exit 0
