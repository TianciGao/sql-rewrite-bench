#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../../.." && pwd)"
cd "${repo_root}"

# shellcheck disable=SC1091
source scripts/env_postgres.sh
# shellcheck disable=SC1091
source scripts/env_spark.sh

python reports/evaluation/common_core_v0/runs/selected_plan_observability_01/run_selected_plan_observability.py
