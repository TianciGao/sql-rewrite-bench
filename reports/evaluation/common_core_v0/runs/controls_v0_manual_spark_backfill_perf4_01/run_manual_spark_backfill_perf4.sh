#!/usr/bin/env bash
set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../../../../" && pwd)"
LOG_DIR="$SCRIPT_DIR/logs"
RESULTS_JSON="$SCRIPT_DIR/run_results.json"
RECORDS_TMP_JSONL="$SCRIPT_DIR/records.tmp.jsonl"

if [[ "$(pwd)" != "$REPO_ROOT" ]]; then
  echo "This script must be run from the repository root."
  echo "Expected: $REPO_ROOT"
  echo "Current:  $(pwd)"
  exit 2
fi

mkdir -p "$LOG_DIR"
: >"$RECORDS_TMP_JSONL"

echo "Manual Spark backfill run: PERF_0006 PERF_0007 PERF_0008 PERF_0013"
echo "This script is intended for a human to run from the real repo root."
echo "Warning: case-local Spark artifacts under cases/PERF/<case>/runs/spark may be regenerated."
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

run_and_record "env_check" python -m scripts.cli env-check
run_and_record "perf_0006_spark_validation" bash cases/PERF/PERF_0006/validation/run_spark_validation.sh
run_and_record "perf_0007_spark_validation" bash cases/PERF/PERF_0007/validation/run_spark_validation.sh
run_and_record "perf_0008_spark_validation" bash cases/PERF/PERF_0008/validation/run_spark_validation.sh
run_and_record "perf_0013_spark_validation" bash cases/PERF/PERF_0013/validation/run_spark_validation.sh

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
            "run_id": "controls_v0_manual_spark_backfill_perf4_01",
            "mode": "manual_human_execution",
            "repo_root": os.environ["REPO_ROOT"],
            "case_scope": [
                "PERF_0006",
                "PERF_0007",
                "PERF_0008",
                "PERF_0013"
            ],
            "engine_scope": ["spark"],
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
  printf '  %-36s status=%-14s exit=%s\n' \
    "${RECORD_KEYS[$idx]}" \
    "${RECORD_STATUSES[$idx]}" \
    "${RECORD_EXIT_CODES[$idx]:-}"
done

echo
echo "Manual Spark PERF backfill run complete. Review logs and run_results.json before any follow-on materialization."
exit 0
