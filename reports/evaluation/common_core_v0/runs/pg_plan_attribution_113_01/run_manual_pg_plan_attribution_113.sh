#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../../.." && pwd)"
cd "${repo_root}"

# shellcheck disable=SC1091
source scripts/env_postgres.sh

python -B reports/evaluation/common_core_v0/runs/pg_plan_attribution_113_01/run_pg_plan_attribution_113.py
