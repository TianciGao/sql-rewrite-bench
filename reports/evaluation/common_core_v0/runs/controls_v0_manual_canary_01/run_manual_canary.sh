#!/usr/bin/env bash
set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../../../../" && pwd)"
LOG_DIR="$SCRIPT_DIR/logs"
RESULTS_JSON="$SCRIPT_DIR/run_results.json"

if [[ "$(pwd)" != "$REPO_ROOT" ]]; then
  echo "This script must be run from the repository root."
  echo "Expected: $REPO_ROOT"
  echo "Current:  $(pwd)"
  exit 2
fi

mkdir -p "$LOG_DIR"

echo "Manual controls canary: PERF_0006 PG/MySQL validation only"
echo "This script is intended for a human to run from the real repo root."
echo "Warning: case-local files under cases/PERF/PERF_0006/runs may be regenerated."
echo "Do not git add anything from this run until the results are reviewed."
echo

source scripts/env_postgres.sh
source scripts/env_mysql.sh
source scripts/env_spark.sh

declare -a COMMAND_KEYS=()
declare -a COMMAND_STRINGS=()
declare -a EXIT_CODES=()
declare -a STDOUT_LOGS=()
declare -a STDERR_LOGS=()

run_and_record() {
  local key="$1"
  shift
  local cmd=( "$@" )
  local stdout_log="$LOG_DIR/${key}.stdout.log"
  local stderr_log="$LOG_DIR/${key}.stderr.log"
  local exit_code=0

  COMMAND_KEYS+=( "$key" )
  COMMAND_STRINGS+=( "$(printf '%q ' "${cmd[@]}")" )
  STDOUT_LOGS+=( "${stdout_log#$REPO_ROOT/}" )
  STDERR_LOGS+=( "${stderr_log#$REPO_ROOT/}" )

  echo "==> Running [$key]"
  printf 'Command:'
  printf ' %q' "${cmd[@]}"
  printf '\n'

  if "${cmd[@]}" >"$stdout_log" 2>"$stderr_log"; then
    exit_code=0
  else
    exit_code=$?
  fi

  EXIT_CODES+=( "$exit_code" )
  echo "Exit code: $exit_code"
  echo "stdout: ${stdout_log#$REPO_ROOT/}"
  echo "stderr: ${stderr_log#$REPO_ROOT/}"
  echo
}

run_and_record "env_check" python -m scripts.cli env-check
run_and_record "perf_0006_pg_validation" bash cases/PERF/PERF_0006/validation/run_pg_validation.sh
run_and_record "perf_0006_mysql_validation" bash cases/PERF/PERF_0006/validation/run_mysql_validation.sh

export RESULTS_JSON
export REPO_ROOT
export COMMAND_KEYS_JOINED
export COMMAND_STRINGS_JOINED
export EXIT_CODES_JOINED
export STDOUT_LOGS_JOINED
export STDERR_LOGS_JOINED

COMMAND_KEYS_JOINED="$(printf '%s\n' "${COMMAND_KEYS[@]}")"
COMMAND_STRINGS_JOINED="$(printf '%s\n' "${COMMAND_STRINGS[@]}")"
EXIT_CODES_JOINED="$(printf '%s\n' "${EXIT_CODES[@]}")"
STDOUT_LOGS_JOINED="$(printf '%s\n' "${STDOUT_LOGS[@]}")"
STDERR_LOGS_JOINED="$(printf '%s\n' "${STDERR_LOGS[@]}")"

python - <<'PY'
import json
import os
from pathlib import Path

def split_lines(name: str) -> list[str]:
    value = os.environ.get(name, "")
    return [line for line in value.splitlines() if line]

keys = split_lines("COMMAND_KEYS_JOINED")
commands = split_lines("COMMAND_STRINGS_JOINED")
exit_codes = [int(x) for x in split_lines("EXIT_CODES_JOINED")]
stdout_logs = split_lines("STDOUT_LOGS_JOINED")
stderr_logs = split_lines("STDERR_LOGS_JOINED")

records = []
for idx, key in enumerate(keys):
    records.append(
        {
            "key": key,
            "command": commands[idx].strip(),
            "exit_code": exit_codes[idx],
            "stdout_log": stdout_logs[idx],
            "stderr_log": stderr_logs[idx],
        }
    )

Path(os.environ["RESULTS_JSON"]).write_text(
    json.dumps(
        {
            "run_id": "controls_v0_manual_canary_01",
            "mode": "manual_human_execution",
            "repo_root": os.environ["REPO_ROOT"],
            "case_scope": ["PERF_0006"],
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
for idx in "${!COMMAND_KEYS[@]}"; do
  printf '  %-28s exit=%s\n' "${COMMAND_KEYS[$idx]}" "${EXIT_CODES[$idx]}"
done

echo
echo "Manual canary complete. Review logs and run_results.json before any follow-on materialization."
