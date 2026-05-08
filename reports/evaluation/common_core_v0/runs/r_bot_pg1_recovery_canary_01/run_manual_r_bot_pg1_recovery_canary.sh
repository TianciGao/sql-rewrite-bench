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
RBOT_SMOKE_PYTHON="/tmp/rewritebench_rbot_llm4rewrite_venv_smoke/bin/python"

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

python - "$REPO_ROOT" "$RUN_DIR" "$RUN_RESULTS_JSON" "$MATRIX_CSV" "$RBOT_SMOKE_PYTHON" <<'PY'
from __future__ import annotations

import csv
import json
import os
import shlex
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(sys.argv[1])
RUN_DIR = Path(sys.argv[2])
RUN_RESULTS_JSON = Path(sys.argv[3])
MATRIX_CSV = Path(sys.argv[4])
RBOT_SMOKE_PYTHON = Path(sys.argv[5])

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


def read_json_file(path: Path, parse_error: str) -> dict[str, Any]:
    if not path.is_file():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {"parse_error": parse_error}
    return payload if isinstance(payload, dict) else {"parse_error": parse_error}


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


def rewrite_to_smoke_python(cmd: str) -> str:
    prefixes = [
        "python -m scripts.cli ",
        "python3 -m scripts.cli ",
    ]
    for prefix in prefixes:
        if cmd.startswith(prefix):
            suffix = cmd[len(prefix):]
            return f"{shlex.quote(str(RBOT_SMOKE_PYTHON))} -m scripts.cli {suffix}"
    return cmd


def append_align_rule_vector_dim(cmd: str, target_dim: int) -> str:
    return f"{cmd} --align-rule-vector-dim {shlex.quote(str(target_dim))}"


def run_command(cmd: str, stdout_name: str, stderr_name: str) -> dict[str, Any]:
    stdout_path = LOG_DIR / stdout_name
    stderr_path = LOG_DIR / stderr_name
    effective_cmd = rewrite_to_smoke_python(cmd)
    with stdout_path.open("w", encoding="utf-8") as stdout_handle, stderr_path.open("w", encoding="utf-8") as stderr_handle:
        proc = subprocess.run(
            effective_cmd,
            cwd=REPO_ROOT,
            shell=True,
            text=True,
            stdout=stdout_handle,
            stderr=stderr_handle,
        )
    return {
        "command": effective_cmd,
        "requested_command": cmd,
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


def materialize_actual_outputs(
    payload: dict[str, Any],
    smoke_actual_exit_code: int,
) -> tuple[bool, str, str]:
    generated_sql_copied = False
    upstream_generated_sql_path = str(payload.get("generated_sql_path", "")).strip()
    output_sql_extracted = bool(payload.get("output_sql_extracted"))
    upstream_generated_sql = Path(upstream_generated_sql_path) if upstream_generated_sql_path else TMP_GENERATED_SQL

    if (
        smoke_actual_exit_code == 0
        and output_sql_extracted
        and upstream_generated_sql.is_file()
    ):
        generated_sql_copied = copy_if_exists(upstream_generated_sql, GENERATED_SQL_PATH)
        payload["generation_status"] = "exploratory_generation_success"
        payload["generated_sql_path"] = str(GENERATED_SQL_PATH.relative_to(REPO_ROOT))
        payload["upstream_generated_sql_path"] = str(upstream_generated_sql)
        payload["generated_sql_copied"] = generated_sql_copied
    elif smoke_actual_exit_code == 0:
        payload["generation_status"] = "exploratory_generation_failed_output_missing"
        payload["generated_sql_copied"] = False
    else:
        payload["generation_status"] = "generation_failed"
        payload["generated_sql_copied"] = False

    checker_candidate_sql_repo_path = ""
    checker_candidate_sql_path = str(payload.get("checker_candidate_sql_path", "")).strip()
    if checker_candidate_sql_path:
        checker_candidate_sql_repo_target = ARTIFACTS_DIR / "PERF_0006_checker_candidate_sql.sql"
        if copy_if_exists(Path(checker_candidate_sql_path), checker_candidate_sql_repo_target):
            checker_candidate_sql_repo_path = str(checker_candidate_sql_repo_target.relative_to(REPO_ROOT))
            payload["checker_candidate_sql_repo_path"] = checker_candidate_sql_repo_path

    return generated_sql_copied, upstream_generated_sql_path, checker_candidate_sql_repo_path


row = load_matrix_row()
allow_actual_run = os.environ.get("RBOT_CANARY_ALLOW_ACTUAL_RUN", "") == "1"
allow_exploratory_unfrozen_policy = os.environ.get("RBOT_CANARY_ALLOW_EXPLORATORY_UNFROZEN_POLICY", "") == "1"
materialize_last_actual = os.environ.get("RBOT_CANARY_MATERIALIZE_LAST_ACTUAL", "") == "1"
retrieval_vector_patch_requested = False
retrieval_vector_patch_target_dim: int | None = None

align_rule_vector_dim_raw = os.environ.get("RBOT_CANARY_ALIGN_RULE_VECTOR_DIM", "").strip()
if align_rule_vector_dim_raw:
    retrieval_vector_patch_requested = True
    retrieval_vector_patch_target_dim = int(align_rule_vector_dim_raw)

env_visibility = {
    name: bool(os.environ.get(name))
    for name in ["OPENAI_API_KEY", "PGHOST", "PGPORT", "PGDATABASE", "PGUSER", "PGPASSWORD"]
}
tmp_visibility = {
    "llm4rewrite_clone_visible": TMP_UPSTREAM_ROOT.is_dir(),
    "rag_index_visible": TMP_RAG_INDEX.is_dir(),
    "smoke_venv_visible": TMP_VENV.is_dir(),
    "smoke_python_visible": RBOT_SMOKE_PYTHON.is_file(),
}

steps: list[dict[str, Any]] = []

dry_run_payload: dict[str, Any] = {}
if not materialize_last_actual and TMP_DRY_RUN_JSON.is_file():
    try:
        dry_run_payload = json.loads(TMP_DRY_RUN_JSON.read_text(encoding="utf-8"))
    except Exception:
        dry_run_payload = {"parse_error": "failed_to_parse_tmp_dry_run_summary"}

if materialize_last_actual:
    technical_dry_run_ready = False
else:
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
    step_exit_codes = {step["step"]: int(step["exit_code"]) for step in steps}
    technical_dry_run_ready = (
        step_exit_codes.get("adapter_preflight") == 0
        and step_exit_codes.get("smoke_preflight") == 0
        and step_exit_codes.get("smoke_dry_run") == 0
        and tmp_visibility["smoke_python_visible"]
        and env_visibility["OPENAI_API_KEY"]
    )

current_benchmark_gate_ready = False
exploratory_actual_run_allowed = (
    not materialize_last_actual
    and
    technical_dry_run_ready
    and allow_actual_run
    and allow_exploratory_unfrozen_policy
)
exploratory_actual_run_claim_boundary = (
    "exploratory_smoke_only_not_current_common_core_metric_evidence"
    if exploratory_actual_run_allowed
    else ""
)
current_benchmark_metric_evidence = False
can_execute_smoke_next = technical_dry_run_ready

actual_run_attempted = False
actual_run_payload: dict[str, Any] = {}
generated_sql_copied = False
upstream_generated_sql_path = ""
checker_candidate_sql_repo_path = ""
materialized_from_existing_actual = False

if materialize_last_actual:
    materialized_from_existing_actual = True
    smoke_actual_log_path = LOG_DIR / "smoke_actual.stdout.log"
    actual_run_payload = read_json_file(
        smoke_actual_log_path,
        "failed_to_parse_smoke_actual_stdout_json",
    )
    steps.append(
        {
            "step": "materialize_last_actual",
            "command": "materialize-from-existing-smoke-actual-log",
            "requested_command": "",
            "exit_code": 0 if smoke_actual_log_path.is_file() and "parse_error" not in actual_run_payload else 1,
            "stdout_log": str(smoke_actual_log_path.relative_to(REPO_ROOT)),
            "stderr_log": "",
        }
    )
    generated_sql_copied, upstream_generated_sql_path, checker_candidate_sql_repo_path = materialize_actual_outputs(
        actual_run_payload,
        0,
    )
    if actual_run_payload.get("retrieval_vector_patch_applied") is True:
        retrieval_vector_patch_requested = True
        if retrieval_vector_patch_target_dim is None:
            expected_dim = actual_run_payload.get("retrieval_vector_expected_dim")
            if isinstance(expected_dim, int):
                retrieval_vector_patch_target_dim = expected_dim
    exploratory_actual_run_claim_boundary = (
        "exploratory_smoke_only_not_current_common_core_metric_evidence"
    )

if exploratory_actual_run_allowed:
    actual_run_attempted = True
    smoke_actual_command = row["repo_command_smoke_actual"]
    if retrieval_vector_patch_target_dim is not None:
        smoke_actual_command = append_align_rule_vector_dim(
            smoke_actual_command,
            retrieval_vector_patch_target_dim,
        )
    steps.append(
        {
            "step": "smoke_actual",
            **run_command(
                smoke_actual_command,
                "smoke_actual.stdout.log",
                "smoke_actual.stderr.log",
            ),
        }
    )
    actual_run_payload = read_json_file(
        LOG_DIR / "smoke_actual.stdout.log",
        "failed_to_parse_smoke_actual_stdout_json",
    )
    if not actual_run_payload:
        actual_run_payload = read_json_file(
            TMP_SMOKE_RESULT_JSON,
            "failed_to_parse_tmp_smoke_result",
        )

    generated_sql_copied, upstream_generated_sql_path, checker_candidate_sql_repo_path = materialize_actual_outputs(
        actual_run_payload,
        int(steps[-1]["exit_code"]),
    )

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
if not tmp_visibility["smoke_python_visible"]:
    blocked_reasons.append("blocked_runner_missing_tmp_smoke_python")
if not materialize_last_actual and not allow_actual_run:
    blocked_reasons.append("actual_run_not_permitted_without_RBOT_CANARY_ALLOW_ACTUAL_RUN=1")
if not materialize_last_actual and allow_actual_run and not allow_exploratory_unfrozen_policy:
    blocked_reasons.append("actual_run_not_permitted_without_RBOT_CANARY_ALLOW_EXPLORATORY_UNFROZEN_POLICY=1")
if not materialize_last_actual and allow_actual_run and not technical_dry_run_ready:
    blocked_reasons.append("actual_run_refused_dry_run_not_ready")
if row["prompt_demo_policy_state"] != "frozen":
    blocked_reasons.append("blocked_policy_missing_prompt_demo_not_frozen")
if row["contamination_guard_state"] != "available":
    blocked_reasons.append("blocked_policy_missing_contamination_guard")
blocked_reasons.append("blocked_current_benchmark_gate_retrieval_corpus_not_frozen")
blocked_reasons.append("blocked_current_benchmark_gate_index_not_frozen")
blocked_reasons.append("blocked_current_benchmark_gate_artifact_contract_not_satisfied")

if generated_sql_copied:
    generation_status = "exploratory_generation_success"
    feasibility_status = "exploratory_canary_generation_succeeded"
    blocker_reason = ""
elif materialized_from_existing_actual:
    generation_status = actual_run_payload.get("generation_status", "exploratory_generation_failed_output_missing")
    feasibility_status = "exploratory_canary_materialization_from_existing_actual"
    blocker_reason = actual_run_payload.get("failure_category", "materialization_failed_output_missing")
elif technical_dry_run_ready and exploratory_actual_run_allowed and actual_run_attempted:
    smoke_actual_exit_code = int(steps[-1]["exit_code"])
    if smoke_actual_exit_code == 0:
        generation_status = "exploratory_generation_failed_output_missing"
    else:
        generation_status = "generation_failed"
    feasibility_status = "exploratory_canary_generation_failed_after_ready_check"
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
    "runner_scaffold": f"{RBOT_SMOKE_PYTHON} -m scripts.cli formal-rbot-llm4rewrite-single-case-smoke-run --case PERF_0006",
    "python_executable_used_for_rbot_scaffolds": str(RBOT_SMOKE_PYTHON),
    "retrieval_stack_status": row["retrieval_stack_state"],
    "retrieval_corpus_status": row["retrieval_corpus_state"],
    "prompt_demo_policy_status": row["prompt_demo_policy_state"],
    "contamination_guard_status": row["contamination_guard_state"],
    "env_visibility": env_visibility,
    "tmp_visibility": tmp_visibility,
    "dry_run_summary_path": str(TMP_DRY_RUN_JSON) if TMP_DRY_RUN_JSON.exists() else "",
    "smoke_result_tmp_path": str(TMP_SMOKE_RESULT_JSON) if TMP_SMOKE_RESULT_JSON.exists() else "",
    "allow_actual_run": allow_actual_run,
    "allow_exploratory_unfrozen_policy": allow_exploratory_unfrozen_policy,
    "materialized_from_existing_actual": materialized_from_existing_actual,
    "retrieval_vector_patch_requested": retrieval_vector_patch_requested,
    "retrieval_vector_patch_target_dim": retrieval_vector_patch_target_dim,
    "retrieval_vector_patch_claim_boundary": (
        "exploratory_smoke_only_not_current_metric"
        if retrieval_vector_patch_requested
        else ""
    ),
    "technical_dry_run_ready": technical_dry_run_ready,
    "current_benchmark_gate_ready": current_benchmark_gate_ready,
    "exploratory_actual_run_allowed": exploratory_actual_run_allowed,
    "exploratory_actual_run_claim_boundary": exploratory_actual_run_claim_boundary,
    "current_benchmark_metric_evidence": current_benchmark_metric_evidence,
    "dry_run_can_execute_next": technical_dry_run_ready,
    "actual_run_attempted": actual_run_attempted,
    "generation_status": generation_status,
    "feasibility_status": feasibility_status,
    "blocker_reason": blocker_reason,
    "generated_sql_path": str(GENERATED_SQL_PATH.relative_to(REPO_ROOT)) if generated_sql_copied else row["expected_generated_sql_path"],
    "upstream_generated_sql_path": upstream_generated_sql_path,
    "generated_sql_copied": generated_sql_copied,
    "checker_candidate_sql_repo_path": checker_candidate_sql_repo_path,
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
