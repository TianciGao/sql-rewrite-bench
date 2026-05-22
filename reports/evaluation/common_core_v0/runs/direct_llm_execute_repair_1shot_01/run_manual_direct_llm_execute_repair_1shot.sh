#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../../../../.." && pwd)"

if [[ "$(pwd)" != "${REPO_ROOT}" ]]; then
  echo "This script must be run from the repository root: ${REPO_ROOT}" >&2
  exit 1
fi

echo "Direct LLM + Execute-and-Repair-1"
echo "This run uses only the 21 repair-ready rows from the retained preflight manifest."
echo "It does not modify the original Direct LLM artifacts."

source "${REPO_ROOT}/scripts/env_postgres.sh"
source "${REPO_ROOT}/scripts/env_mysql.sh"
source "${REPO_ROOT}/scripts/env_spark.sh"

python "${SCRIPT_DIR}/run_direct_llm_execute_repair_1shot.py"
