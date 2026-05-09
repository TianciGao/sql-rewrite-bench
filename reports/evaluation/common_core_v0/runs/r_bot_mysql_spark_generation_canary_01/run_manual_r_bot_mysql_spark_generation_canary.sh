#!/usr/bin/env bash
set -euo pipefail

discover_repo_root() {
  local start_dir="$1"
  local current="$start_dir"
  while [[ "$current" != "/" ]]; do
    if [[ -d "$current/.git" ]] || \
       [[ -f "$current/reports/curation/common_core_v0_final_denominator.csv" ]] || \
       [[ -f "$current/reports/evaluation/common_core_v0/r_bot_formal_protocol/r_bot_common_core_v0_40_same_engine_candidate_matrix.csv" ]]; then
      printf '%s\n' "$current"
      return 0
    fi
    current="$(dirname "$current")"
  done
  return 1
}

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(discover_repo_root "$SCRIPT_DIR")"
if [[ -z "${REPO_ROOT:-}" ]]; then
  echo "unable to discover repo root" >&2
  exit 1
fi

RUN_ID="r_bot_mysql_spark_generation_canary_01"
METHOD_ID="r_bot"
ROUTE_ID="r_bot_same_engine_rewrite"
SOURCE_DENOMINATOR_ID="common_core_v0_40_same_engine_120"
CANARY_DENOMINATOR_ID="r_bot_mysql_spark_generation_canary_01"
CLAIM_BOUNDARY="mysql_spark_generation_canary_only_not_execution_timing_speedup_or_leaderboard_evidence"

RUN_ROOT="$REPO_ROOT/reports/evaluation/common_core_v0/runs/$RUN_ID"
MATRIX_PATH="$RUN_ROOT/generation_command_matrix.csv"
RESULTS_PATH="$RUN_ROOT/run_results.json"
EVENTS_PATH="$RUN_ROOT/run_event_long.csv"

FORMAL_PYTHON="/tmp/rewritebench_rbot_llm4rewrite_venv_smoke/bin/python"
FORMAL_INDEX_DIR="/tmp/rewritebench_rbot_formal_chroma_index_01"
FORMAL_INDEX_IDENTIFIER="$REPO_ROOT/reports/evaluation/common_core_v0/r_bot_formal_index_build_01/formal_chroma_index_identifier_v1.json"
FORMAL_PARAMETER_FREEZE="$REPO_ROOT/reports/evaluation/common_core_v0/r_bot_formal_protocol/r_bot_parameter_freeze_v2.json"
UPSTREAM_ROOT="/tmp/rewritebench_prior_method_audit/LLM4Rewrite"

mkdir -p "$RUN_ROOT"

python_write_preflight_failure() {
  "$FORMAL_PYTHON" - <<'PY' "$RESULTS_PATH" "$EVENTS_PATH" "$MATRIX_PATH" "$RUN_ID" "$METHOD_ID" "$ROUTE_ID" "$SOURCE_DENOMINATOR_ID" "$CANARY_DENOMINATOR_ID" "$CLAIM_BOUNDARY" "$1" "$2"
import csv
import json
import sys
from pathlib import Path

results_path = Path(sys.argv[1])
events_path = Path(sys.argv[2])
matrix_path = Path(sys.argv[3])
run_id, method_id, route_id = sys.argv[4], sys.argv[5], sys.argv[6]
source_denominator_id, canary_denominator_id = sys.argv[7], sys.argv[8]
claim_boundary = sys.argv[9]
failure_category, failure_reason = sys.argv[10], sys.argv[11]

rows = list(csv.DictReader(matrix_path.open()))
event_fields = [
    "row_key", "case_id", "pool", "engine", "row_status", "failure_category",
    "failure_reason", "generated_sql_exists", "prompt_exists", "raw_response_exists",
    "selected_rules_exists", "retrieval_trace_exists", "token_cost_exists",
    "provider_metadata_exists", "row_metadata_exists"
]

with events_path.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=event_fields)
    writer.writeheader()
    for row in rows:
        writer.writerow({
            "row_key": row["row_key"],
            "case_id": row["case_id"],
            "pool": row["pool"],
            "engine": row["engine"],
            "row_status": "preflight_blocked",
            "failure_category": failure_category,
            "failure_reason": failure_reason,
            "generated_sql_exists": "no",
            "prompt_exists": "no",
            "raw_response_exists": "no",
            "selected_rules_exists": "no",
            "retrieval_trace_exists": "no",
            "token_cost_exists": "no",
            "provider_metadata_exists": "no",
            "row_metadata_exists": "no",
        })

payload = {
    "run_id": run_id,
    "method_id": method_id,
    "route_id": route_id,
    "source_denominator_id": source_denominator_id,
    "canary_denominator_id": canary_denominator_id,
    "claim_boundary": claim_boundary,
    "status": "preflight_failed",
    "failure_category": failure_category,
    "failure_reason": failure_reason,
    "planned_rows": len(rows),
    "status_counts": {"preflight_blocked": len(rows)},
    "engine_scope": "mysql_and_spark_canary_only",
    "current_benchmark_metric_evidence": False,
    "notes": [
        "human-run only package",
        "generation-only canary",
        "no SQL execution in this runner",
        "no timing or speedup evidence",
    ],
}
results_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
PY
}

if [[ ! -f "$FORMAL_PYTHON" ]]; then
  echo "missing formal runtime python: $FORMAL_PYTHON" >&2
  exit 1
fi

if [[ ! -f "$MATRIX_PATH" ]]; then
  echo "missing generation matrix: $MATRIX_PATH" >&2
  exit 1
fi

if [[ -z "${OPENAI_API_KEY:-}" ]]; then
  python_write_preflight_failure "missing_env_visibility" "OPENAI_API_KEY is not visible in the current shell"
  exit 0
fi

if [[ -z "${OPENAI_BASE_URL:-}" ]]; then
  python_write_preflight_failure "missing_env_visibility" "OPENAI_BASE_URL is not visible in the current shell"
  exit 0
fi

if [[ ! -d "$FORMAL_INDEX_DIR" ]]; then
  python_write_preflight_failure "missing_formal_index_dir" "Formal Chroma index directory is not visible"
  exit 0
fi

if [[ ! -f "$FORMAL_INDEX_IDENTIFIER" ]]; then
  python_write_preflight_failure "missing_formal_index_identifier" "Formal Chroma index identifier is not visible"
  exit 0
fi

if [[ ! -f "$FORMAL_PARAMETER_FREEZE" ]]; then
  python_write_preflight_failure "missing_formal_parameter_freeze" "Formal parameter freeze JSON is not visible"
  exit 0
fi

if [[ ! -d "$UPSTREAM_ROOT" ]]; then
  python_write_preflight_failure "missing_upstream_llm4rewrite_root" "Visible upstream LLM4Rewrite tree is not available"
  exit 0
fi

if [[ "${RBOT_CANARY_ALLOW_PROVIDER_PREFLIGHT_CALL:-0}" == "1" ]]; then
  "$FORMAL_PYTHON" - <<'PY' "$RESULTS_PATH" "$EVENTS_PATH" "$MATRIX_PATH" "$RUN_ID" "$METHOD_ID" "$ROUTE_ID" "$SOURCE_DENOMINATOR_ID" "$CANARY_DENOMINATOR_ID" "$CLAIM_BOUNDARY"
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

results_path = Path(sys.argv[1])
events_path = Path(sys.argv[2])
matrix_path = Path(sys.argv[3])
run_id, method_id, route_id = sys.argv[4], sys.argv[5], sys.argv[6]
source_denominator_id, canary_denominator_id = sys.argv[7], sys.argv[8]
claim_boundary = sys.argv[9]

base_url = os.environ.get("OPENAI_BASE_URL", "").rstrip("/")
api_key = os.environ.get("OPENAI_API_KEY", "")

def write_failure(reason: str) -> None:
    import csv
    rows = list(csv.DictReader(matrix_path.open()))
    event_fields = [
        "row_key", "case_id", "pool", "engine", "row_status", "failure_category",
        "failure_reason", "generated_sql_exists", "prompt_exists", "raw_response_exists",
        "selected_rules_exists", "retrieval_trace_exists", "token_cost_exists",
        "provider_metadata_exists", "row_metadata_exists"
    ]
    with events_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=event_fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({
                "row_key": row["row_key"],
                "case_id": row["case_id"],
                "pool": row["pool"],
                "engine": row["engine"],
                "row_status": "preflight_blocked",
                "failure_category": "provider_preflight_failed",
                "failure_reason": reason,
                "generated_sql_exists": "no",
                "prompt_exists": "no",
                "raw_response_exists": "no",
                "selected_rules_exists": "no",
                "retrieval_trace_exists": "no",
                "token_cost_exists": "no",
                "provider_metadata_exists": "no",
                "row_metadata_exists": "no",
            })
    payload = {
        "run_id": run_id,
        "method_id": method_id,
        "route_id": route_id,
        "source_denominator_id": source_denominator_id,
        "canary_denominator_id": canary_denominator_id,
        "claim_boundary": claim_boundary,
        "status": "preflight_failed",
        "failure_category": "provider_preflight_failed",
        "failure_reason": reason,
        "planned_rows": len(rows),
        "status_counts": {"preflight_blocked": len(rows)},
        "engine_scope": "mysql_and_spark_canary_only",
        "current_benchmark_metric_evidence": False,
        "notes": [
            "human-run only package",
            "generation-only canary",
            "optional provider auth preflight was enabled",
            "no SQL execution in this runner",
        ],
    }
    results_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

if not base_url or not api_key:
    write_failure("OPENAI_BASE_URL or OPENAI_API_KEY is missing for optional provider preflight")
    raise SystemExit(4)

candidates = [f"{base_url}/models"]
if not base_url.endswith("/v1"):
    candidates.append(f"{base_url}/v1/models")

last_error = None
for url in candidates:
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {api_key}"})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            if 200 <= resp.status < 300:
                raise SystemExit(0)
            last_error = f"unexpected provider preflight status {resp.status} at {url}"
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as exc:
        last_error = f"{type(exc).__name__} at {url}: {exc}"

write_failure(last_error or "provider preflight failed")
raise SystemExit(4)
PY
  status_code=$?
  if [[ $status_code -ne 0 ]]; then
    echo "provider preflight failed; see $RESULTS_PATH"
    exit 0
  fi
fi

"$FORMAL_PYTHON" - <<'PY' "$REPO_ROOT" "$MATRIX_PATH" "$UPSTREAM_ROOT" "$RESULTS_PATH" "$EVENTS_PATH" "$RUN_ID" "$METHOD_ID" "$ROUTE_ID" "$SOURCE_DENOMINATOR_ID" "$CANARY_DENOMINATOR_ID" "$CLAIM_BOUNDARY"
import csv
import json
import sys
from pathlib import Path

repo_root = Path(sys.argv[1])
matrix_path = Path(sys.argv[2])
upstream_root = Path(sys.argv[3])
results_path = Path(sys.argv[4])
events_path = Path(sys.argv[5])
run_id, method_id, route_id = sys.argv[6], sys.argv[7], sys.argv[8]
source_denominator_id, canary_denominator_id = sys.argv[9], sys.argv[10]
claim_boundary = sys.argv[11]

rows = list(csv.DictReader(matrix_path.open()))
db_adapter_path = upstream_root / "my_rewriter" / "database.py"

missing_artifacts = []
for row in rows:
    for key in ("source_sql_path", "schema_path", "witness_data_path"):
        rel = row[key]
        if not (repo_root / rel).is_file():
            missing_artifacts.append(f"{row['row_key']}:{key}:{rel}")

failure_category = None
failure_reason = None
if not db_adapter_path.is_file():
    failure_category = "missing_upstream_database_adapter"
    failure_reason = f"Missing upstream database adapter: {db_adapter_path}"
else:
    text = db_adapter_path.read_text(encoding="utf-8", errors="ignore")
    if "if self.dbtype == 'postgresql':" in text and "raise NotImplementedError" in text:
        failure_category = "engine_adapter_not_implemented_mysql_spark"
        failure_reason = "Visible upstream my_rewriter/database.py still only implements db=postgresql"

if not failure_category and missing_artifacts:
    failure_category = "missing_case_artifact"
    failure_reason = "; ".join(missing_artifacts)

event_fields = [
    "row_key", "case_id", "pool", "engine", "row_status", "failure_category",
    "failure_reason", "generated_sql_exists", "prompt_exists", "raw_response_exists",
    "selected_rules_exists", "retrieval_trace_exists", "token_cost_exists",
    "provider_metadata_exists", "row_metadata_exists"
]

if failure_category:
    with events_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=event_fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({
                "row_key": row["row_key"],
                "case_id": row["case_id"],
                "pool": row["pool"],
                "engine": row["engine"],
                "row_status": "preflight_blocked",
                "failure_category": failure_category,
                "failure_reason": failure_reason,
                "generated_sql_exists": "no",
                "prompt_exists": "no",
                "raw_response_exists": "no",
                "selected_rules_exists": "no",
                "retrieval_trace_exists": "no",
                "token_cost_exists": "no",
                "provider_metadata_exists": "no",
                "row_metadata_exists": "no",
            })
    payload = {
        "run_id": run_id,
        "method_id": method_id,
        "route_id": route_id,
        "source_denominator_id": source_denominator_id,
        "canary_denominator_id": canary_denominator_id,
        "claim_boundary": claim_boundary,
        "status": "preflight_failed",
        "failure_category": failure_category,
        "failure_reason": failure_reason,
        "planned_rows": len(rows),
        "status_counts": {"preflight_blocked": len(rows)},
        "engine_scope": "mysql_and_spark_canary_only",
        "current_benchmark_metric_evidence": False,
        "notes": [
            "human-run only package",
            "generation-only canary",
            "no SQL execution in this runner",
            "no timing or speedup evidence",
            "rows remain explicit even when preflight blocks route execution",
        ],
    }
    results_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    sys.exit(3)

# Safe fallback: if future adapter work removes the preflight blocker,
# this package should be replaced by an engine-specific generation runner.
payload = {
    "run_id": run_id,
    "method_id": method_id,
    "route_id": route_id,
    "source_denominator_id": source_denominator_id,
    "canary_denominator_id": canary_denominator_id,
    "claim_boundary": claim_boundary,
    "status": "preflight_passed_but_generation_route_not_materialized_in_this_package",
    "planned_rows": len(rows),
    "status_counts": {"planned_canary_attempt": len(rows)},
    "engine_scope": "mysql_and_spark_canary_only",
    "current_benchmark_metric_evidence": False,
    "notes": [
        "This package is intentionally fail-closed.",
        "If adapter recovery happens later, create a dedicated apply task to materialize the actual mysql/spark generation runner.",
    ],
}
results_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
with events_path.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=event_fields)
    writer.writeheader()
    for row in rows:
        writer.writerow({
            "row_key": row["row_key"],
            "case_id": row["case_id"],
            "pool": row["pool"],
            "engine": row["engine"],
            "row_status": "planned_canary_attempt",
            "failure_category": "",
            "failure_reason": "",
            "generated_sql_exists": "no",
            "prompt_exists": "no",
            "raw_response_exists": "no",
            "selected_rules_exists": "no",
            "retrieval_trace_exists": "no",
            "token_cost_exists": "no",
            "provider_metadata_exists": "no",
            "row_metadata_exists": "no",
        })
PY

status_code=$?
if [[ $status_code -eq 3 ]]; then
  echo "preflight blocked mysql/spark canary route; see $RESULTS_PATH"
  exit 0
fi

echo "canary package preflight passed, but no mysql/spark generation route is materialized in this package without a follow-up adapter-recovery patch."
exit 0
