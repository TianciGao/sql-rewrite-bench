#!/usr/bin/env bash
set -euo pipefail

# Human-run only.
# Verification only.
# Does not run R-Bot, does not call an API, does not execute SQL.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}"/../../../../.. && pwd)"
RUN_DIR="${ROOT_DIR}/reports/evaluation/common_core_v0/runs/r_bot_pg1_recovery_canary_01"
SMOKE_VENV_PATH="/tmp/rewritebench_rbot_llm4rewrite_venv_smoke"
VERIFY_JSON_PATH="${RUN_DIR}/smoke_env_verify.json"
PACKAGE_SNAPSHOT_PATH="${RUN_DIR}/smoke_env_package_snapshot.txt"

if [[ "${PWD}" != "${ROOT_DIR}" ]]; then
  echo "run from repo root: ${ROOT_DIR}" >&2
  exit 1
fi

if [[ ! -x "${SMOKE_VENV_PATH}/bin/python" ]]; then
  echo "missing smoke venv python: ${SMOKE_VENV_PATH}/bin/python" >&2
  exit 1
fi

mkdir -p "${RUN_DIR}"
source "${SMOKE_VENV_PATH}/bin/activate"

VERIFY_JSON_PATH="${VERIFY_JSON_PATH}" \
PACKAGE_SNAPSHOT_PATH="${PACKAGE_SNAPSHOT_PATH}" \
SMOKE_VENV_PATH="${SMOKE_VENV_PATH}" \
python - <<'PY'
import importlib
import json
import os
import sys
from pathlib import Path

modules = [
    "chromadb",
    "jpype",
    "jsonlines",
    "llama_index",
    "psycopg2",
    "openai",
    "sqlglot",
]

results = {}
all_imports_ok = True
for name in modules:
    try:
        module = importlib.import_module(name)
        results[name] = {
            "import_ok": True,
            "version": getattr(module, "__version__", None),
            "error": None,
        }
    except Exception as exc:  # noqa: BLE001
        all_imports_ok = False
        results[name] = {
            "import_ok": False,
            "version": None,
            "error": f"{type(exc).__name__}: {exc}",
        }

payload = {
    "probe": "r_bot_smoke_env_verify",
    "claim_boundary": "smoke_environment_verification_only_not_rbot_result",
    "smoke_venv_path": os.environ["SMOKE_VENV_PATH"],
    "python_executable": sys.executable,
    "package_snapshot_exists": Path(os.environ["PACKAGE_SNAPSHOT_PATH"]).is_file(),
    "required_imports": results,
    "all_required_imports_ok": all_imports_ok,
    "env_visibility": {
        "OPENAI_API_KEY": bool(os.environ.get("OPENAI_API_KEY")),
        "OPENAI_BASE_URL": bool(os.environ.get("OPENAI_BASE_URL")),
        "OPENAI_API_BASE": bool(os.environ.get("OPENAI_API_BASE")),
    },
}

Path(os.environ["VERIFY_JSON_PATH"]).write_text(
    json.dumps(payload, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
)
print(json.dumps(payload, indent=2, sort_keys=True))
PY
