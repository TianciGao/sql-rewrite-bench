#!/usr/bin/env bash
set -uo pipefail

PACKAGE_ROOT="$(cd -- "$(dirname -- "$0")" && pwd)"

discover_repo_root() {
  local current="$1"
  while [[ "$current" != "/" ]]; do
    if [[ -d "$current/.git" ]] || [[ -f "$current/reports/curation/common_core_v0_final_denominator.csv" ]] || [[ -f "$current/reports/evaluation/common_core_v0/r_bot_formal_protocol/r_bot_common_core_v0_40_same_engine_candidate_matrix.csv" ]]; then
      printf '%s\n' "$current"
      return 0
    fi
    current="$(dirname -- "$current")"
  done
  return 1
}

REPO_ROOT="$(discover_repo_root "$PACKAGE_ROOT")" || {
  echo "failed to discover repo root from package root: $PACKAGE_ROOT" >&2
  exit 1
}

FORMAL_PYTHON="/tmp/rewritebench_rbot_llm4rewrite_venv_smoke/bin/python"
FORMAL_INDEX_DIR="/tmp/rewritebench_rbot_formal_chroma_index_01"
FORMAL_INDEX_IDENTIFIER="$REPO_ROOT/reports/evaluation/common_core_v0/r_bot_formal_index_build_01/formal_chroma_index_identifier_v1.json"
FORMAL_RUNTIME_SNAPSHOT="$REPO_ROOT/reports/evaluation/common_core_v0/r_bot_formal_runtime_lock_01/runtime_environment_snapshot_v1.json"
FORMAL_PARAMETER_FREEZE="$REPO_ROOT/reports/evaluation/common_core_v0/r_bot_formal_protocol/r_bot_parameter_freeze_v2.json"
COMMAND_MATRIX="$PACKAGE_ROOT/generation_command_matrix.csv"

OUTPUT_RUN_ROOT="$REPO_ROOT/reports/evaluation/common_core_v0/runs/r_bot_common_core_v0_40_same_engine_generation_01"
RUN_EVENT_LONG_PATH="$OUTPUT_RUN_ROOT/run_event_long.csv"
RUN_RESULTS_PATH="$OUTPUT_RUN_ROOT/run_results.json"
GENERATION_SUMMARY_PATH="$OUTPUT_RUN_ROOT/generation_summary.csv"
LOG_ROOT="$OUTPUT_RUN_ROOT/logs"

export REPO_ROOT
export PACKAGE_ROOT
export FORMAL_PYTHON
export FORMAL_INDEX_DIR
export FORMAL_INDEX_IDENTIFIER
export FORMAL_RUNTIME_SNAPSHOT
export FORMAL_PARAMETER_FREEZE
export COMMAND_MATRIX
export OUTPUT_RUN_ROOT
export RUN_EVENT_LONG_PATH
export RUN_RESULTS_PATH
export GENERATION_SUMMARY_PATH
export LOG_ROOT

if [[ ! -x "$FORMAL_PYTHON" ]]; then
  echo "missing formal python: $FORMAL_PYTHON" >&2
  exit 1
fi

if [[ ! -f "$COMMAND_MATRIX" ]]; then
  echo "missing command matrix: $COMMAND_MATRIX" >&2
  exit 1
fi

if [[ ! -f "$FORMAL_INDEX_IDENTIFIER" ]]; then
  echo "missing formal index identifier: $FORMAL_INDEX_IDENTIFIER" >&2
  exit 1
fi

if [[ ! -d "$FORMAL_INDEX_DIR" ]]; then
  echo "missing formal index directory: $FORMAL_INDEX_DIR" >&2
  exit 1
fi

if [[ -z "${OPENAI_API_KEY:-}" ]]; then
  echo "OPENAI_API_KEY must be visible in the environment for human-run generation." >&2
  exit 1
fi

mkdir -p "$OUTPUT_RUN_ROOT" "$LOG_ROOT"

"$FORMAL_PYTHON" - <<'PY'
from __future__ import annotations

import csv
import json
import os
import shutil
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


REPO_ROOT = Path(os.environ["REPO_ROOT"])
PACKAGE_ROOT = Path(os.environ["PACKAGE_ROOT"])
FORMAL_PYTHON = Path(os.environ["FORMAL_PYTHON"])
FORMAL_INDEX_DIR = Path(os.environ["FORMAL_INDEX_DIR"])
FORMAL_INDEX_IDENTIFIER = Path(os.environ["FORMAL_INDEX_IDENTIFIER"])
FORMAL_RUNTIME_SNAPSHOT = Path(os.environ["FORMAL_RUNTIME_SNAPSHOT"])
FORMAL_PARAMETER_FREEZE = Path(os.environ["FORMAL_PARAMETER_FREEZE"])
COMMAND_MATRIX = Path(os.environ["COMMAND_MATRIX"])
OUTPUT_RUN_ROOT = Path(os.environ["OUTPUT_RUN_ROOT"])
RUN_EVENT_LONG_PATH = Path(os.environ["RUN_EVENT_LONG_PATH"])
RUN_RESULTS_PATH = Path(os.environ["RUN_RESULTS_PATH"])
GENERATION_SUMMARY_PATH = Path(os.environ["GENERATION_SUMMARY_PATH"])
LOG_ROOT = Path(os.environ["LOG_ROOT"])

RUN_ID = "r_bot_same_engine_generation_01"
METHOD_ID = "r_bot"
ROUTE_ID = "r_bot_same_engine_rewrite"
DENOMINATOR_ID = "common_core_v0_40_same_engine_120"
CLAIM_BOUNDARY = "formal_same_engine_generation_only_not_execution_timing_speedup_or_leaderboard_evidence"
SUPPORTED_PG_CASES = {
    "PERF_0006", "PERF_0008", "PERF_0013", "PERF_0017", "PERF_0019",
    "PERF_0024", "PERF_0033", "PERF_0052", "PERF_0054", "PERF_0063",
}
RUNNER_ROOT = Path("/tmp/rewritebench_rbot_llm4rewrite_single_case_runner")

with FORMAL_PARAMETER_FREEZE.open("r", encoding="utf-8") as handle:
    parameter_freeze = json.load(handle)
with FORMAL_INDEX_IDENTIFIER.open("r", encoding="utf-8") as handle:
    index_identifier = json.load(handle)
with FORMAL_RUNTIME_SNAPSHOT.open("r", encoding="utf-8") as handle:
    runtime_snapshot = json.load(handle)

model_name = parameter_freeze["benchmark_common_config"]["model_config"]["model_name"]
provider_name = parameter_freeze["benchmark_common_config"]["model_config"]["provider_policy"]["provider_name"]
base_url = parameter_freeze["benchmark_common_config"]["model_config"]["provider_policy"]["base_url"]
base_url_family = index_identifier["embedding_provider_base_url_family"]
retrieval_top_k = parameter_freeze["benchmark_common_config"]["retrieval_parameters"]["top_k"]
reranking_mode = parameter_freeze["benchmark_common_config"]["retrieval_parameters"]["reranking_mode"]
rrf_k = parameter_freeze["benchmark_common_config"]["retrieval_parameters"]["rrf_k"]
similarity_threshold_policy = index_identifier["similarity_threshold_policy"]
embedding_model = index_identifier["embedding_model"]
rule_vector_width = index_identifier["rule_vector_width"]
total_dimension = index_identifier["total_dimension"]

env_visibility = {
    "OPENAI_API_KEY": bool(os.environ.get("OPENAI_API_KEY")),
    "PGHOST": bool(os.environ.get("PGHOST")),
    "PGPORT": bool(os.environ.get("PGPORT")),
    "PGDATABASE": bool(os.environ.get("PGDATABASE")),
    "PGUSER": bool(os.environ.get("PGUSER")),
    "PGPASSWORD": bool(os.environ.get("PGPASSWORD")),
}

OUTPUT_RUN_ROOT.mkdir(parents=True, exist_ok=True)
LOG_ROOT.mkdir(parents=True, exist_ok=True)

run_event_fieldnames = [
    "run_id",
    "case_id",
    "pool",
    "engine",
    "method_id",
    "route_id",
    "git_commit",
    "denominator_id",
    "row_status",
    "claim_boundary",
    "generated_sql_path",
    "selected_rules_path",
    "retrieval_trace_path",
    "prompt_path",
    "raw_response_path",
    "token_cost_provider_path",
    "environment_snapshot_path",
    "row_run_metadata_path",
    "failure_category",
    "blocker_reason",
    "unsupported_reason",
    "speedup_exclusion_reason",
]

run_event_rows: list[dict[str, str]] = []
counts_by_status: Counter[str] = Counter()
counts_by_engine: Counter[str] = Counter()
counts_by_pool: Counter[str] = Counter()


def write_text(path_str: str, text: str) -> None:
    path = REPO_ROOT / path_str
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path_str: str, payload: dict) -> None:
    path = REPO_ROOT / path_str
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def read_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def copy_if_exists(src: Path, dest_str: str) -> bool:
    dest = REPO_ROOT / dest_str
    if not src.is_file():
        return False
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)
    return True


def placeholder_json(row: dict[str, str], kind: str, status: str, reason: str) -> dict:
    payload = {
        "available": False,
        "artifact_kind": kind,
        "case_id": row["case_id"],
        "engine": row["engine"],
        "method_id": row["method_id"],
        "route_id": row["route_id"],
        "row_status": status,
        "reason": reason,
    }
    if kind == "selected_rules":
        payload.update(
            {
                "rule_selection_status": status,
                "selected_rules": [],
                "rule_vector_width": rule_vector_width,
                "rule_catalog_path": "reports/evaluation/common_core_v0/r_bot_formal_index_build_01/formal_rule_vector_catalog_v1.json",
            }
        )
    elif kind == "retrieval_trace":
        payload.update(
            {
                "retrieval_status": status,
                "index_id": index_identifier["index_id"],
                "collection_name": index_identifier["chroma_collection_name"],
                "retrieved_examples": [],
            }
        )
    return payload


with COMMAND_MATRIX.open("r", encoding="utf-8", newline="") as handle:
    rows = list(csv.DictReader(handle))

for row in rows:
    counts_by_engine[row["engine"]] += 1
    counts_by_pool[row["pool"]] += 1
    row_key = row["row_key"]
    case_id = row["case_id"]
    engine = row["engine"]
    row_log_dir = LOG_ROOT / case_id / engine
    row_log_dir.mkdir(parents=True, exist_ok=True)

    expected_generated_sql_path = row["expected_generated_sql_path"]
    expected_prompt_path = row["expected_prompt_path"]
    expected_raw_response_path = row["expected_raw_response_path"]
    expected_selected_rules_path = row["expected_selected_rules_path"]
    expected_retrieval_trace_path = row["expected_retrieval_trace_path"]
    expected_token_cost_path = row["expected_token_cost_path"]
    expected_row_metadata_path = row["expected_row_metadata_path"]
    environment_snapshot_path = expected_row_metadata_path.replace("row_run_metadata.json", "environment_snapshot.json")

    environment_snapshot_payload = {
        "case_id": case_id,
        "engine": engine,
        "method_id": METHOD_ID,
        "route_id": ROUTE_ID,
        "python_version": runtime_snapshot.get("python_version"),
        "platform": runtime_snapshot.get("platform"),
        "python_executable": str(FORMAL_PYTHON),
        "requirements_lock_path": "reports/evaluation/common_core_v0/r_bot_formal_runtime_lock_01/r_bot_formal_requirements_lock.txt",
        "runtime_snapshot_path": "reports/evaluation/common_core_v0/r_bot_formal_runtime_lock_01/runtime_environment_snapshot_v1.json",
        "formal_chroma_index_identifier_path": "reports/evaluation/common_core_v0/r_bot_formal_index_build_01/formal_chroma_index_identifier_v1.json",
        "openai_api_key_visible": env_visibility["OPENAI_API_KEY"],
        "provider_family": provider_name,
        "base_url_family": base_url_family,
        "provider_name": provider_name,
        "base_url_visible": bool(base_url),
        "index_directory": str(FORMAL_INDEX_DIR),
        "index_id": index_identifier["index_id"],
        "rule_vector_width": rule_vector_width,
        "total_dimension": total_dimension,
        "contamination_guard_attested_at_generation_time": None,
    }
    write_json(environment_snapshot_path, environment_snapshot_payload)

    planned_status = row["generation_status_planned"]
    row_status = "blocked"
    failure_category = ""
    blocker_reason = ""
    unsupported_reason = ""

    if planned_status == "blocked_or_unsupported":
        if engine == "pg":
            row_status = "blocked"
            blocker_reason = row["blocker_or_caveat"]
        else:
            row_status = "unsupported"
            unsupported_reason = row["blocker_or_caveat"]

        write_text(expected_prompt_path, f"generation_not_attempted\nrow_status={row_status}\nreason={row['blocker_or_caveat']}\n")
        write_text(expected_raw_response_path, f"raw_response_not_available\nrow_status={row_status}\nreason={row['blocker_or_caveat']}\n")
        write_json(expected_selected_rules_path, placeholder_json(row, "selected_rules", row_status, row["blocker_or_caveat"]))
        write_json(expected_retrieval_trace_path, placeholder_json(row, "retrieval_trace", row_status, row["blocker_or_caveat"]))
        write_json(
            expected_token_cost_path,
            {
                "available": False,
                "case_id": case_id,
                "engine": engine,
                "method_id": METHOD_ID,
                "route_id": ROUTE_ID,
                "provider_name": provider_name,
                "provider_family": provider_name,
                "embedding_provider_family": base_url_family,
                "model_name": model_name,
                "base_url_family": base_url_family,
                "prompt_tokens": None,
                "completion_tokens": None,
                "total_tokens": None,
                "cost_fields": {},
                "retry_count": 0,
                "row_status": row_status,
                "reason": row["blocker_or_caveat"],
            },
        )
    else:
        command = [
            str(FORMAL_PYTHON),
            "-m",
            "scripts.cli",
            "formal-rbot-llm4rewrite-single-case-smoke-run",
            "--case",
            case_id,
            "--fresh-run-name",
            "--align-rule-vector-dim",
            "100",
        ]
        stdout_path = row_log_dir / "generation.stdout.log"
        stderr_path = row_log_dir / "generation.stderr.log"
        completed = subprocess.run(
            command,
            cwd=REPO_ROOT,
            env=os.environ.copy(),
            stdout=stdout_path.open("w", encoding="utf-8"),
            stderr=stderr_path.open("w", encoding="utf-8"),
            text=True,
        )
        artifact_root = RUNNER_ROOT / case_id
        smoke_result_path = artifact_root / "smoke_result_v3.json"
        smoke_payload = read_json(smoke_result_path) if smoke_result_path.is_file() else {}

        generated_ok = copy_if_exists(artifact_root / "generated_sql_v3.sql", expected_generated_sql_path)
        selected_rules_ok = copy_if_exists(artifact_root / "selected_rules_v3.json", expected_selected_rules_path)
        retrieval_trace_ok = copy_if_exists(artifact_root / "retrieval_trace_v3.json", expected_retrieval_trace_path)
        token_cost_ok = copy_if_exists(artifact_root / "token_cost_log_v3.json", expected_token_cost_path)

        if generated_ok and completed.returncode == 0:
            row_status = "generated"
        else:
            row_status = "failed"
            failure_category = smoke_payload.get("failure_category") or "generation_failed_or_missing_sql"
            failure_summary = smoke_payload.get("failure_summary") or "Recovered runner did not produce contract-complete generated SQL."
            blocker_reason = failure_summary

        prompt_reason = "prompt_not_captured_by_recovered_runner_use_method_stdout_log"
        raw_response_reason = "raw_response_not_captured_by_recovered_runner_use_method_stdout_log"
        write_text(
            expected_prompt_path,
            "\n".join(
                [
                    f"capture_status={prompt_reason}",
                    f"case_id={case_id}",
                    f"engine={engine}",
                    f"runner_log={stdout_path}",
                    f"row_status={row_status}",
                    "",
                ]
            ),
        )
        write_text(
            expected_raw_response_path,
            "\n".join(
                [
                    f"capture_status={raw_response_reason}",
                    f"case_id={case_id}",
                    f"engine={engine}",
                    f"runner_log={stdout_path}",
                    f"row_status={row_status}",
                    "",
                ]
            ),
        )
        if not selected_rules_ok:
            write_json(expected_selected_rules_path, placeholder_json(row, "selected_rules", row_status, "selected_rules_not_captured"))
        if not retrieval_trace_ok:
            write_json(expected_retrieval_trace_path, placeholder_json(row, "retrieval_trace", row_status, "retrieval_trace_not_captured"))
        if not token_cost_ok:
            write_json(
                expected_token_cost_path,
                {
                    "available": False,
                    "case_id": case_id,
                    "engine": engine,
                    "method_id": METHOD_ID,
                    "route_id": ROUTE_ID,
                    "provider_name": provider_name,
                    "provider_family": provider_name,
                    "embedding_provider_family": base_url_family,
                    "model_name": model_name,
                    "base_url_family": base_url_family,
                    "prompt_tokens": None,
                    "completion_tokens": None,
                    "total_tokens": None,
                    "cost_fields": {},
                    "retry_count": 0,
                    "row_status": row_status,
                    "reason": "token_cost_or_provider_metadata_not_captured_by_recovered_runner",
                },
            )
        if failure_category:
            blocker_reason = blocker_reason or failure_category

    row_metadata_payload = {
        "run_id": RUN_ID,
        "case_id": case_id,
        "pool": row["pool"],
        "engine": engine,
        "method_id": METHOD_ID,
        "route_id": ROUTE_ID,
        "denominator_id": DENOMINATOR_ID,
        "row_status": row_status,
        "claim_boundary": CLAIM_BOUNDARY,
        "generated_sql_path": expected_generated_sql_path,
        "selected_rules_path": expected_selected_rules_path,
        "retrieval_trace_path": expected_retrieval_trace_path,
        "prompt_path": expected_prompt_path,
        "raw_response_path": expected_raw_response_path,
        "token_cost_provider_path": expected_token_cost_path,
        "environment_snapshot_path": environment_snapshot_path,
        "failure_category": failure_category,
        "failure_summary": blocker_reason if row_status == "failed" else "",
        "blocker_reason": blocker_reason,
        "unsupported_reason": unsupported_reason,
    }
    write_json(expected_row_metadata_path, row_metadata_payload)

    counts_by_status[row_status] += 1
    run_event_rows.append(
        {
            "run_id": RUN_ID,
            "case_id": case_id,
            "pool": row["pool"],
            "engine": engine,
            "method_id": METHOD_ID,
            "route_id": ROUTE_ID,
            "git_commit": "",
            "denominator_id": DENOMINATOR_ID,
            "row_status": row_status,
            "claim_boundary": CLAIM_BOUNDARY,
            "generated_sql_path": expected_generated_sql_path,
            "selected_rules_path": expected_selected_rules_path,
            "retrieval_trace_path": expected_retrieval_trace_path,
            "prompt_path": expected_prompt_path,
            "raw_response_path": expected_raw_response_path,
            "token_cost_provider_path": expected_token_cost_path,
            "environment_snapshot_path": environment_snapshot_path,
            "row_run_metadata_path": expected_row_metadata_path,
            "failure_category": failure_category,
            "blocker_reason": blocker_reason,
            "unsupported_reason": unsupported_reason,
            "speedup_exclusion_reason": "generation_phase_only_no_speedup_computation",
        }
    )

with RUN_EVENT_LONG_PATH.open("w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=run_event_fieldnames)
    writer.writeheader()
    writer.writerows(run_event_rows)

with GENERATION_SUMMARY_PATH.open("w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(
        handle,
        fieldnames=[
            "run_id",
            "method_id",
            "route_id",
            "denominator_id",
            "planned_rows",
            "rows_generated",
            "rows_failed",
            "rows_blocked",
            "rows_unsupported",
            "rows_skipped",
            "claim_boundary",
        ],
    )
    writer.writeheader()
    writer.writerow(
        {
            "run_id": RUN_ID,
            "method_id": METHOD_ID,
            "route_id": ROUTE_ID,
            "denominator_id": DENOMINATOR_ID,
            "planned_rows": len(rows),
            "rows_generated": counts_by_status.get("generated", 0),
            "rows_failed": counts_by_status.get("failed", 0),
            "rows_blocked": counts_by_status.get("blocked", 0),
            "rows_unsupported": counts_by_status.get("unsupported", 0),
            "rows_skipped": counts_by_status.get("skipped", 0),
            "claim_boundary": CLAIM_BOUNDARY,
        }
    )

run_results_payload = {
    "run_id": RUN_ID,
    "method_id": METHOD_ID,
    "route_id": ROUTE_ID,
    "denominator_id": DENOMINATOR_ID,
    "planned_rows": len(rows),
    "git_commit": "",
    "claim_boundary": CLAIM_BOUNDARY,
    "current_benchmark_gate_ready": False,
    "counts_by_status": dict(counts_by_status),
    "counts_by_engine": dict(counts_by_engine),
    "counts_by_pool": dict(counts_by_pool),
    "run_event_long_path": str(RUN_EVENT_LONG_PATH.relative_to(REPO_ROOT)),
    "generation_summary_path": str(GENERATION_SUMMARY_PATH.relative_to(REPO_ROOT)),
    "formal_runtime_python": str(FORMAL_PYTHON),
    "formal_index_identifier_path": str(FORMAL_INDEX_IDENTIFIER.relative_to(REPO_ROOT)),
    "formal_index_directory": str(FORMAL_INDEX_DIR),
    "parameter_freeze_path": str(FORMAL_PARAMETER_FREEZE.relative_to(REPO_ROOT)),
    "model_name": model_name,
    "provider_name": provider_name,
    "base_url_family": base_url_family,
    "retrieval_top_k": retrieval_top_k,
    "reranking_mode": reranking_mode,
    "rrf_k": rrf_k,
    "similarity_threshold_policy": similarity_threshold_policy,
    "current_benchmark_metric_evidence": False,
    "notes": [
        "generation package only",
        "no execution, validity, timing, speedup, or leaderboard evidence is produced by this package alone",
        "rows remain denominator-aware and explicit for blocked, unsupported, failed, and generated statuses",
    ],
}
RUN_RESULTS_PATH.write_text(json.dumps(run_results_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps({"run_id": RUN_ID, "planned_rows": len(rows), "counts_by_status": dict(counts_by_status)}, sort_keys=True))
PY
