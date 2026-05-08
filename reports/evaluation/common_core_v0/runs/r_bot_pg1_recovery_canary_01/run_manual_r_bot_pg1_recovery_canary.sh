#!/usr/bin/env bash
set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../../../../.." && pwd)"
RUN_DIR="${SCRIPT_DIR}"
LOG_DIR="${RUN_DIR}/logs"
GENERATED_DIR="${RUN_DIR}/generated/PERF_0006/pg"
ARTIFACTS_DIR="${RUN_DIR}/artifacts"
RUN_RESULTS_JSON="${RUN_DIR}/run_results.json"
MATRIX_CSV="${RUN_DIR}/recovery_command_matrix.csv"

if [[ "$(pwd)" != "${REPO_ROOT}" ]]; then
  echo "This script must be run from the repository root: ${REPO_ROOT}" >&2
  exit 1
fi

mkdir -p "${LOG_DIR}" "${GENERATED_DIR}" "${ARTIFACTS_DIR}"

echo "Human-run only."
echo "Codex must not execute this script."
echo "This is an R-Bot recovery canary package for PERF_0006 on PostgreSQL."
echo "It does not compute timing, speedup, or leaderboard artifacts."
echo "By default it performs preflight and dry-run checks only."
echo "To allow the actual bounded generation attempt, set RBOT_CANARY_ALLOW_ACTUAL_RUN=1 in the shell."

python - "$REPO_ROOT" "$RUN_DIR" "$RUN_RESULTS_JSON" "$MATRIX_CSV" <<'PY'
from __future__ import annotations

import csv
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(sys.argv[1])
RUN_DIR = Path(sys.argv[2])
RUN_RESULTS_JSON = Path(sys.argv[3])
MATRIX_CSV = Path(sys.argv[4])

CASE_ID = "PERF_0006"
METHOD_ID = "r_bot"
ROUTE_ID = "r_bot_pg_rewrite"
DENOMINATOR_ID = "common_core_v0_40_pg40"
CANARY_DENOMINATOR_ID = "common_core_v0_40_perf_pg1_r_bot_recovery_canary"

LOG_DIR = RUN_DIR / "logs"
GENERATED_SQL_PATH = RUN_DIR / "generated" / "PERF_0006" / "pg" / "r_bot_pg_rewrite.sql"
ARTIFACTS_DIR = RUN_DIR / "artifacts"

TMP_DRY_RUN_JSON = Path("/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0006/dry_run_summary_v1.json")
TMP_SMOKE_RESULT_JSON = Path("/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0006/smoke_result_v1.json")
TMP_GENERATED_SQL = Path("/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0006/generated_sql.sql")
TMP_SELECTED_RULES = Path("/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0006/selected_rules.json")
TMP_RETRIEVAL_TRACE = Path("/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0006/retrieval_trace.json")
TMP_TOKEN_COST = Path("/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0006/token_cost_log.json")
TMP_METHOD_STDOUT = Path("/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0006/method_stdout.log")
TMP_METHOD_STDERR = Path("/tmp/rewritebench_rbot_llm4rewrite_single_case_runner/PERF_0006/method_stderr.log")

TMP_UPSTREAM_ROOT = Path("/tmp/rewritebench_prior_method_audit/LLM4Rewrite")
TMP_RAG_INDEX = Path("/tmp/rewritebench_rbot_llm4rewrite_rag_build_openai_like/rag/chroma_db")
TMP_VENV = Path("/tmp/rewritebench_rbot_llm4rewrite_venv_smoke")


def load_matrix_row() -> dict[str, str]:
    with MATRIX_CSV.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 1:
        raise RuntimeError(f"expected exactly 1 matrix row, found {len(rows)}")
    return rows[0]


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def git_commit() -> str:
    try:
        proc = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=REPO_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        return proc.stdout.strip()
    except Exception:
        return ""


def run_command(cmd: str, stdout_name: str, stderr_name: str) -> dict[str, Any]:
    stdout_path = LOG_DIR / stdout_name
    stderr_path = LOG_DIR / stderr_name
    with stdout_path.open("w", encoding="utf-8") as stdout_handle, stderr_path.open("w", encoding="utf-8") as stderr_handle:
        proc = subprocess.run(
            cmd,
            cwd=REPO_ROOT,
            shell=True,
            text=True,
            stdout=stdout_handle,
            stderr=stderr_handle,
        )
    return {
        "command": cmd,
        "exit_code": proc.returncode,
        "stdout_log": str(stdout_path.relative_to(REPO_ROOT)),
        "stderr_log": str(stderr_path.relative_to(REPO_ROOT)),
    }


def copy_if_exists(src: Path, dst: Path) -> bool:
    if not src.is_file():
        return False
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return True


row = load_matrix_row()
allow_actual_run = os.environ.get("RBOT_CANARY_ALLOW_ACTUAL_RUN", "") == "1"

env_visibility = {
    name: bool(os.environ.get(name))
    for name in ["OPENAI_API_KEY", "PGHOST", "PGPORT", "PGDATABASE", "PGUSER", "PGPASSWORD"]
}
tmp_visibility = {
    "llm4rewrite_clone_visible": TMP_UPSTREAM_ROOT.is_dir(),
    "rag_index_visible": TMP_RAG_INDEX.is_dir(),
    "smoke_venv_visible": TMP_VENV.is_dir(),
}

steps: list[dict[str, Any]] = []

steps.append(
    {
        "step": "adapter_preflight",
        **run_command(
            row["repo_command_adapter_preflight"],
            "adapter_preflight.stdout.log",
            "adapter_preflight.stderr.log",
        ),
    }
)
steps.append(
    {
        "step": "smoke_preflight",
        **run_command(
            row["repo_command_smoke_preflight"],
            "smoke_preflight.stdout.log",
            "smoke_preflight.stderr.log",
        ),
    }
)
steps.append(
    {
        "step": "smoke_dry_run",
        **run_command(
            row["repo_command_smoke_dry_run"],
            "smoke_dry_run.stdout.log",
            "smoke_dry_run.stderr.log",
        ),
    }
)

dry_run_payload: dict[str, Any] = {}
if TMP_DRY_RUN_JSON.is_file():
    try:
        dry_run_payload = json.loads(TMP_DRY_RUN_JSON.read_text(encoding="utf-8"))
    except Exception:
        dry_run_payload = {"parse_error": "failed_to_parse_tmp_dry_run_summary"}

can_execute_smoke_next = bool(dry_run_payload.get("can_execute_smoke_next"))

actual_run_attempted = False
actual_run_payload: dict[str, Any] = {}
generated_sql_copied = False

if allow_actual_run and can_execute_smoke_next:
    actual_run_attempted = True
    steps.append(
        {
            "step": "smoke_actual",
            **run_command(
                row["repo_command_smoke_actual"],
                "smoke_actual.stdout.log",
                "smoke_actual.stderr.log",
            ),
        }
    )
    if TMP_SMOKE_RESULT_JSON.is_file():
        try:
            actual_run_payload = json.loads(TMP_SMOKE_RESULT_JSON.read_text(encoding="utf-8"))
        except Exception:
            actual_run_payload = {"parse_error": "failed_to_parse_tmp_smoke_result"}
    generated_sql_copied = copy_if_exists(TMP_GENERATED_SQL, GENERATED_SQL_PATH)
    copy_if_exists(TMP_SELECTED_RULES, ARTIFACTS_DIR / "PERF_0006_selected_rules.json")
    copy_if_exists(TMP_RETRIEVAL_TRACE, ARTIFACTS_DIR / "PERF_0006_retrieval_trace.json")
    copy_if_exists(TMP_TOKEN_COST, ARTIFACTS_DIR / "PERF_0006_token_cost_log.json")
    copy_if_exists(TMP_METHOD_STDOUT, ARTIFACTS_DIR / "PERF_0006_method_stdout.log")
    copy_if_exists(TMP_METHOD_STDERR, ARTIFACTS_DIR / "PERF_0006_method_stderr.log")

blocked_reasons: list[str] = []
if not tmp_visibility["llm4rewrite_clone_visible"]:
    blocked_reasons.append("blocked_runner_missing_tmp_llm4rewrite_clone")
if not tmp_visibility["rag_index_visible"]:
    blocked_reasons.append("blocked_retrieval_stack_missing_tmp_rag_index")
if not tmp_visibility["smoke_venv_visible"]:
    blocked_reasons.append("blocked_runner_missing_tmp_smoke_venv")
if row["prompt_demo_policy_state"] != "frozen":
    blocked_reasons.append("blocked_policy_missing_prompt_demo_not_frozen")
if row["contamination_guard_state"] != "available":
    blocked_reasons.append("blocked_policy_missing_contamination_guard")
if not allow_actual_run:
    blocked_reasons.append("actual_run_not_permitted_without_RBOT_CANARY_ALLOW_ACTUAL_RUN=1")
if allow_actual_run and not can_execute_smoke_next:
    blocked_reasons.append("actual_run_refused_dry_run_not_ready")

if generated_sql_copied:
    generation_status = "generation_success"
    feasibility_status = "canary_generation_succeeded"
    blocker_reason = ""
elif can_execute_smoke_next and allow_actual_run and actual_run_attempted:
    generation_status = "generation_failed"
    feasibility_status = "canary_generation_failed_after_ready_check"
    blocker_reason = actual_run_payload.get("failure_category", "generation_failed_after_actual_run")
else:
    generation_status = "blocked"
    feasibility_status = row["feasibility_status"]
    blocker_reason = "; ".join(blocked_reasons) if blocked_reasons else row["blocker_reason"]

payload = {
    "run_id": "r_bot_pg1_recovery_canary_01",
    "method_id": METHOD_ID,
    "route_id": ROUTE_ID,
    "denominator_id": DENOMINATOR_ID,
    "canary_denominator_id": CANARY_DENOMINATOR_ID,
    "planned_rows": 1,
    "git_commit": git_commit(),
    "case_id": CASE_ID,
    "pool": "performance",
    "engine": "pg",
    "runner_scaffold": "python -m scripts.cli formal-rbot-llm4rewrite-single-case-smoke-run --case PERF_0006",
    "retrieval_stack_status": row["retrieval_stack_state"],
    "retrieval_corpus_status": row["retrieval_corpus_state"],
    "prompt_demo_policy_status": row["prompt_demo_policy_state"],
    "contamination_guard_status": row["contamination_guard_state"],
    "env_visibility": env_visibility,
    "tmp_visibility": tmp_visibility,
    "dry_run_summary_path": str(TMP_DRY_RUN_JSON) if TMP_DRY_RUN_JSON.exists() else "",
    "smoke_result_tmp_path": str(TMP_SMOKE_RESULT_JSON) if TMP_SMOKE_RESULT_JSON.exists() else "",
    "allow_actual_run": allow_actual_run,
    "dry_run_can_execute_next": can_execute_smoke_next,
    "actual_run_attempted": actual_run_attempted,
    "generation_status": generation_status,
    "feasibility_status": feasibility_status,
    "blocker_reason": blocker_reason,
    "generated_sql_path": str(GENERATED_SQL_PATH.relative_to(REPO_ROOT)) if generated_sql_copied else row["expected_generated_sql_path"],
    "generated_sql_copied": generated_sql_copied,
    "steps": steps,
    "dry_run_payload": dry_run_payload,
    "actual_run_payload": actual_run_payload,
    "notes": [
        "old_r_bot_numeric_results_are_historical_only_not_current_metrics",
        "this_canary_is_pg_only_and_one_case_only",
        "actual_generation_depends_on_tmp_substrate_and_unfrozen_policy_state",
    ],
}
write_json(RUN_RESULTS_JSON, payload)
print(f"wrote {RUN_RESULTS_JSON}")
PY
