#!/usr/bin/env bash
set -euo pipefail

# Human-run only.
# Environment recovery only.
# Do not use this script as benchmark evidence.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}"/../../../../.. && pwd)"
RUN_DIR="${ROOT_DIR}/reports/evaluation/common_core_v0/runs/r_bot_pg1_recovery_canary_01"
REQUIREMENTS_PATH="${RUN_DIR}/r_bot_recovery_requirements.txt"
SMOKE_VENV_PATH="/tmp/rewritebench_rbot_llm4rewrite_venv_smoke"
PACKAGE_SNAPSHOT_PATH="${RUN_DIR}/smoke_env_package_snapshot.txt"

if [[ "${PWD}" != "${ROOT_DIR}" ]]; then
  echo "run from repo root: ${ROOT_DIR}" >&2
  exit 1
fi

if [[ ! -f "${REQUIREMENTS_PATH}" ]]; then
  echo "missing requirements file: ${REQUIREMENTS_PATH}" >&2
  exit 1
fi

mkdir -p "${RUN_DIR}"

if [[ ! -d "${SMOKE_VENV_PATH}" ]]; then
  python3 -m venv "${SMOKE_VENV_PATH}"
fi

source "${SMOKE_VENV_PATH}/bin/activate"

python -m pip install --upgrade pip
python -m pip install -r "${REQUIREMENTS_PATH}"
python -m pip freeze | sort > "${PACKAGE_SNAPSHOT_PATH}"

cat <<EOF
smoke venv ready
venv_path=${SMOKE_VENV_PATH}
requirements_path=${REQUIREMENTS_PATH}
package_snapshot_path=${PACKAGE_SNAPSHOT_PATH}
EOF
