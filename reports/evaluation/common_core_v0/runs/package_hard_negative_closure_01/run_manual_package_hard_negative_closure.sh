#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../../.." && pwd)"
cd "${REPO_ROOT}"

source scripts/env_postgres.sh
source scripts/env_mysql.sh
source scripts/env_spark.sh

.venv/bin/python reports/evaluation/common_core_v0/runs/package_hard_negative_closure_01/run_package_hard_negative_closure.py
