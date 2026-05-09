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
RUN_EVENT_LONG_PATH="$PACKAGE_ROOT/run_event_long.csv"
RUN_RESULTS_PATH="$PACKAGE_ROOT/run_results.json"
LOG_ROOT="$PACKAGE_ROOT/logs"
TMP_RUNNER_ROOT="/tmp/rewritebench_rbot_llm4rewrite_pg40_expansion_runner"

export REPO_ROOT
export PACKAGE_ROOT
export FORMAL_PYTHON
export FORMAL_INDEX_DIR
export FORMAL_INDEX_IDENTIFIER
export FORMAL_RUNTIME_SNAPSHOT
export FORMAL_PARAMETER_FREEZE
export COMMAND_MATRIX
export RUN_EVENT_LONG_PATH
export RUN_RESULTS_PATH
export LOG_ROOT
export TMP_RUNNER_ROOT

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

mkdir -p "$PACKAGE_ROOT" "$LOG_ROOT"

"$FORMAL_PYTHON" - <<'PY'
from __future__ import annotations

import ast
import csv
import json
import os
import re
import shutil
import subprocess
import sys
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


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
RUN_EVENT_LONG_PATH = Path(os.environ["RUN_EVENT_LONG_PATH"])
RUN_RESULTS_PATH = Path(os.environ["RUN_RESULTS_PATH"])
LOG_ROOT = Path(os.environ["LOG_ROOT"])
TMP_RUNNER_ROOT = Path(os.environ["TMP_RUNNER_ROOT"])

RUN_ID = "r_bot_pg40_generation_expansion_02"
METHOD_ID = "r_bot"
ROUTE_ID = "r_bot_same_engine_rewrite"
SOURCE_DENOMINATOR_ID = "common_core_v0_40_same_engine_120"
PG_EXPANSION_DENOMINATOR_ID = "common_core_v0_40_pg40"
CLAIM_BOUNDARY = "formal_pg_generation_expansion_only_not_execution_timing_speedup_or_leaderboard_evidence"
UPSTREAM_ROOT = Path("/tmp/rewritebench_prior_method_audit/LLM4Rewrite")

with FORMAL_PARAMETER_FREEZE.open("r", encoding="utf-8") as handle:
    parameter_freeze = json.load(handle)
with FORMAL_INDEX_IDENTIFIER.open("r", encoding="utf-8") as handle:
    index_identifier = json.load(handle)
with FORMAL_RUNTIME_SNAPSHOT.open("r", encoding="utf-8") as handle:
    runtime_snapshot = json.load(handle)

benchmark_model_name = parameter_freeze["benchmark_common_config"]["model_config"]["model_name"]
provider_name = parameter_freeze["benchmark_common_config"]["model_config"]["provider_policy"]["provider_name"]
base_url = parameter_freeze["benchmark_common_config"]["model_config"]["provider_policy"]["base_url"]
retrieval_top_k = parameter_freeze["benchmark_common_config"]["retrieval_parameters"]["top_k"]
reranking_mode = parameter_freeze["benchmark_common_config"]["retrieval_parameters"]["reranking_mode"]
rrf_k = parameter_freeze["benchmark_common_config"]["retrieval_parameters"]["rrf_k"]
embedding_model = index_identifier["embedding_model"]
rule_vector_width = index_identifier["rule_vector_width"]
total_dimension = index_identifier["total_dimension"]
base_url_family = index_identifier["embedding_provider_base_url_family"]

PACKAGE_ROOT.mkdir(parents=True, exist_ok=True)
LOG_ROOT.mkdir(parents=True, exist_ok=True)
TMP_RUNNER_ROOT.mkdir(parents=True, exist_ok=True)

run_event_fieldnames = [
    "run_id",
    "case_id",
    "pool",
    "engine",
    "method_id",
    "route_id",
    "source_generation_denominator_id",
    "pg_expansion_denominator_id",
    "previous_generation_status_class",
    "row_status",
    "claim_boundary",
    "generated_sql_path",
    "prompt_path",
    "raw_response_path",
    "selected_rules_path",
    "retrieval_trace_path",
    "token_cost_path",
    "provider_metadata_path",
    "row_run_metadata_path",
    "failure_category",
    "blocker_reason",
]


def write_text(path_str: str, text: str) -> None:
    path = REPO_ROOT / path_str
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path_str: str, payload: dict[str, Any]) -> None:
    path = REPO_ROOT / path_str
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def replace_once(path: Path, old: str, new: str) -> bool:
    if not path.is_file():
        return False
    text = path.read_text(encoding="utf-8")
    if old not in text:
        return False
    path.write_text(text.replace(old, new, 1), encoding="utf-8")
    return True


def ensure_placeholder_artifacts(row: dict[str, str], row_status: str, reason: str) -> None:
    if not (REPO_ROOT / row["expected_prompt_path"]).exists():
        write_text(
            row["expected_prompt_path"],
            f"available=false\nrow_status={row_status}\nreason={reason}\n",
        )
    if not (REPO_ROOT / row["expected_raw_response_path"]).exists():
        write_text(
            row["expected_raw_response_path"],
            f"available=false\nrow_status={row_status}\nreason={reason}\n",
        )
    if not (REPO_ROOT / row["expected_selected_rules_path"]).exists():
        write_json(
            row["expected_selected_rules_path"],
            {
                "available": False,
                "row_status": row_status,
                "reason": reason,
                "selected_rules": [],
                "rule_vector_width": rule_vector_width,
            },
        )
    if not (REPO_ROOT / row["expected_retrieval_trace_path"]).exists():
        write_json(
            row["expected_retrieval_trace_path"],
            {
                "available": False,
                "row_status": row_status,
                "reason": reason,
                "retrieved_cases_log_excerpt": "",
                "retrieval_top_k": retrieval_top_k,
                "reranking_mode": reranking_mode,
                "rrf_k": rrf_k,
            },
        )
    if not (REPO_ROOT / row["expected_token_cost_path"]).exists():
        write_json(
            row["expected_token_cost_path"],
            {
                "available": False,
                "row_status": row_status,
                "reason": reason,
                "input_cost": None,
                "output_cost": None,
                "token_usage_available": False,
            },
        )


def extract_rewrite_payload(log_text: str) -> dict[str, Any] | None:
    matches = re.findall(r"Rewrite Execution Results: (\{.*?\})", log_text)
    if not matches:
        return None
    try:
        return ast.literal_eval(matches[-1])
    except Exception:
        return None


def parse_response_records(raw_response_path: Path) -> list[dict[str, Any]]:
    if not raw_response_path.is_file():
        return []
    records: list[dict[str, Any]] = []
    for line in raw_response_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return records


with COMMAND_MATRIX.open("r", encoding="utf-8", newline="") as handle:
    rows = list(csv.DictReader(handle))

counts_by_status: Counter[str] = Counter()
counts_by_pool: Counter[str] = Counter()
counts_by_previous_class: Counter[str] = Counter()
run_event_rows: list[dict[str, str]] = []

for row in rows:
    case_id = row["case_id"]
    pool = row["pool"]
    engine = row["engine"]
    previous_class = row["previous_generation_status_class"]
    counts_by_pool[pool] += 1
    counts_by_previous_class[previous_class] += 1

    expected_generated_sql_path = row["expected_generated_sql_path"]
    expected_prompt_path = row["expected_prompt_path"]
    expected_raw_response_path = row["expected_raw_response_path"]
    expected_selected_rules_path = row["expected_selected_rules_path"]
    expected_retrieval_trace_path = row["expected_retrieval_trace_path"]
    expected_token_cost_path = row["expected_token_cost_path"]
    expected_provider_metadata_path = row["expected_provider_metadata_path"]
    expected_row_metadata_path = row["expected_row_metadata_path"]

    row_log_dir = LOG_ROOT / case_id / engine
    row_log_dir.mkdir(parents=True, exist_ok=True)
    method_stdout_path = row_log_dir / "generation.stdout.log"
    method_stderr_path = row_log_dir / "generation.stderr.log"

    source_sql_path = REPO_ROOT / row["source_sql_path"]
    schema_path = REPO_ROOT / row["schema_path"]

    env_visibility = {
        "OPENAI_API_KEY": bool(os.environ.get("OPENAI_API_KEY")),
        "OPENAI_BASE_URL": bool(os.environ.get("OPENAI_BASE_URL") or os.environ.get("OPENAI_API_BASE")),
        "PGHOST": bool(os.environ.get("PGHOST")),
        "PGPORT": bool(os.environ.get("PGPORT")),
        "PGDATABASE": bool(os.environ.get("PGDATABASE")),
        "PGUSER": bool(os.environ.get("PGUSER")),
        "PGPASSWORD": bool(os.environ.get("PGPASSWORD")),
    }

    provider_metadata = {
        "method_id": METHOD_ID,
        "route_id": ROUTE_ID,
        "case_id": case_id,
        "engine": engine,
        "provider_name": provider_name,
        "base_url": base_url,
        "base_url_family": base_url_family,
        "openai_api_key_visible": env_visibility["OPENAI_API_KEY"],
        "base_url_env_visible": env_visibility["OPENAI_BASE_URL"],
        "model_name": benchmark_model_name,
        "embedding_model": embedding_model,
        "rule_vector_width": rule_vector_width,
        "total_dimension": total_dimension,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(expected_provider_metadata_path, provider_metadata)

    prerequisites = []
    if engine != "pg":
        prerequisites.append("engine_not_pg")
    if not source_sql_path.is_file():
        prerequisites.append("missing_source_sql")
    if not schema_path.is_file():
        prerequisites.append("missing_pg_schema")
    if not FORMAL_PYTHON.is_file():
        prerequisites.append("missing_formal_python")
    if not FORMAL_INDEX_DIR.is_dir():
        prerequisites.append("missing_formal_index_dir")
    if not FORMAL_INDEX_IDENTIFIER.is_file():
        prerequisites.append("missing_formal_index_identifier")
    if not UPSTREAM_ROOT.is_dir():
        prerequisites.append("missing_upstream_llm4rewrite_root")
    if not env_visibility["OPENAI_API_KEY"]:
        prerequisites.append("missing_OPENAI_API_KEY")

    row_status = "blocked"
    failure_category = ""
    blocker_reason = ""
    generation_status = "not_attempted"
    output_sql_extracted = False

    row_metadata: dict[str, Any] = {
        "run_id": RUN_ID,
        "case_id": case_id,
        "pool": pool,
        "engine": engine,
        "method_id": METHOD_ID,
        "route_id": ROUTE_ID,
        "source_generation_denominator_id": SOURCE_DENOMINATOR_ID,
        "pg_expansion_denominator_id": PG_EXPANSION_DENOMINATOR_ID,
        "previous_generation_status_class": previous_class,
        "generation_status_planned": row["generation_status_planned"],
        "claim_boundary": CLAIM_BOUNDARY,
        "runtime_python": str(FORMAL_PYTHON),
        "formal_index_dir": str(FORMAL_INDEX_DIR),
        "formal_index_identifier_path": str(FORMAL_INDEX_IDENTIFIER),
        "formal_runtime_snapshot_path": str(FORMAL_RUNTIME_SNAPSHOT),
        "parameter_freeze_path": str(FORMAL_PARAMETER_FREEZE),
        "openai_api_key_visible": env_visibility["OPENAI_API_KEY"],
        "source_sql_path": row["source_sql_path"],
        "schema_path": row["schema_path"],
        "witness_data_path": row["witness_data_path"],
        "provider_metadata_path": expected_provider_metadata_path,
        "notes": [
            "PG-only expansion attempt",
            "generation-only route",
            "no database or SQL execution in this package runner",
            "does not replace existing PG7 retained evidence",
        ],
    }

    if prerequisites:
        blocker_reason = ";".join(prerequisites)
        failure_category = prerequisites[0]
        row_metadata["row_status"] = "blocked"
        row_metadata["failure_category"] = failure_category
        row_metadata["blocker_reason"] = blocker_reason
        write_json(expected_row_metadata_path, row_metadata)
        ensure_placeholder_artifacts(row, "blocked", blocker_reason)
        counts_by_status["blocked"] += 1
        run_event_rows.append(
            {
                "run_id": RUN_ID,
                "case_id": case_id,
                "pool": pool,
                "engine": engine,
                "method_id": METHOD_ID,
                "route_id": ROUTE_ID,
                "source_generation_denominator_id": SOURCE_DENOMINATOR_ID,
                "pg_expansion_denominator_id": PG_EXPANSION_DENOMINATOR_ID,
                "previous_generation_status_class": previous_class,
                "row_status": "blocked",
                "claim_boundary": CLAIM_BOUNDARY,
                "generated_sql_path": expected_generated_sql_path,
                "prompt_path": expected_prompt_path,
                "raw_response_path": expected_raw_response_path,
                "selected_rules_path": expected_selected_rules_path,
                "retrieval_trace_path": expected_retrieval_trace_path,
                "token_cost_path": expected_token_cost_path,
                "provider_metadata_path": expected_provider_metadata_path,
                "row_run_metadata_path": expected_row_metadata_path,
                "failure_category": failure_category,
                "blocker_reason": blocker_reason,
            }
        )
        continue

    runner_dir = TMP_RUNNER_ROOT / case_id
    runtime_root = runner_dir / "runtime_patch_v4"
    prompt_log_path = runner_dir / "prompt_records.jsonl"
    raw_response_log_path = runner_dir / "raw_response_records.jsonl"
    upstream_log_path = runner_dir / f"rbot_{case_id.lower()}_{int(time.time() * 1000)}.log"

    runner_dir.mkdir(parents=True, exist_ok=True)
    if runtime_root.exists():
        shutil.rmtree(runtime_root)
    shutil.copytree(UPSTREAM_ROOT, runtime_root)

    runtime_chroma_dir = runtime_root / "rag" / "chroma_db"
    if runtime_chroma_dir.exists() or runtime_chroma_dir.is_symlink():
        if runtime_chroma_dir.is_dir() and not runtime_chroma_dir.is_symlink():
            shutil.rmtree(runtime_chroma_dir)
        else:
            runtime_chroma_dir.unlink()
    try:
        os.symlink(FORMAL_INDEX_DIR, runtime_chroma_dir, target_is_directory=True)
    except OSError:
        shutil.copytree(FORMAL_INDEX_DIR, runtime_chroma_dir)

    replace_once(
        runtime_root / "my_rewriter" / "config.py",
        '            Settings.llm = OpenAI(\n                model="gpt-4o"\n            )\n',
        f'            Settings.llm = OpenAI(\n                model="{benchmark_model_name}"\n            )\n',
    )

    for rel in ["knowledge-base/rule_cluster_funcs/24.py", "rag/gen_sql_templates.py"]:
        shim_path = runtime_root / rel
        if shim_path.is_file():
            shim_text = shim_path.read_text(encoding="utf-8")
            shim_text = shim_text.replace(
                "from sqlglot.optimizer.simplify import NONDETERMINISTIC",
                "from sqlglot.optimizer.simplify import Simplifier\nNONDETERMINISTIC = Simplifier.NONDETERMINISTIC",
            )
            shim_path.write_text(shim_text, encoding="utf-8")

    replace_once(
        runtime_root / "my_rewriter" / "test_utils.py",
        "    db = Database(pg_args)\n    input_cost = db.cost_estimation(query)\n    logging.info(f'Input Cost: {input_cost}')\n",
        "    input_cost = None\n    logging.info(f'Input Cost: {input_cost}')\n",
    )
    replace_once(
        runtime_root / "my_rewriter" / "db_utils.py",
        "    db = Database(db_args)\n    used_rules = [str(r) for r in res.rules]\n    output_sql = str(res.sql)\n    rewrite_time = int(res.time)\n    output_cost = -1\n    if output_sql != 'None':\n        output_cost = db.cost_estimation(output_sql)\n",
        "    used_rules = [str(r) for r in res.rules]\n    output_sql = str(res.sql)\n    rewrite_time = int(res.time)\n    output_cost = None\n",
    )

    runtime_query_fusion_path = runtime_root / "rag" / "my_query_fusion_retriver.py"
    if runtime_query_fusion_path.is_file():
        runtime_query_fusion_text = runtime_query_fusion_path.read_text(encoding="utf-8")
        original_block = (
            "        rules_one_hot: List[float] = []\n"
            "        rules_one_hot.extend(get_one_hot(NL_RULES, matched_rules['nl']))\n"
            "        rules_one_hot.extend(get_one_hot(NORMAL_RULES, matched_rules['calcite_normal']))\n"
            "        one_cnt = sum(rules_one_hot)\n"
            "        if one_cnt > 0:\n"
            "            rules_one_hot = [x / math.sqrt(one_cnt) for x in rules_one_hot]\n"
        )
        patched_block = (
            "        rules_one_hot: List[float] = []\n"
            "        rules_one_hot.extend(get_one_hot(NL_RULES, matched_rules['nl']))\n"
            "        rules_one_hot.extend(get_one_hot(NORMAL_RULES, matched_rules['calcite_normal']))\n"
            f"        target_rule_vector_dim = {rule_vector_width}\n"
            "        if len(rules_one_hot) < target_rule_vector_dim:\n"
            "            rules_one_hot.extend([0.0] * (target_rule_vector_dim - len(rules_one_hot)))\n"
            "        elif len(rules_one_hot) > target_rule_vector_dim:\n"
            "            rules_one_hot = rules_one_hot[:target_rule_vector_dim]\n"
            "        one_cnt = sum(rules_one_hot)\n"
            "        if one_cnt > 0:\n"
            "            rules_one_hot = [x / math.sqrt(one_cnt) for x in rules_one_hot]\n"
        )
        if original_block in runtime_query_fusion_text:
            runtime_query_fusion_path.write_text(
                runtime_query_fusion_text.replace(original_block, patched_block, 1),
                encoding="utf-8",
            )

    calcite_src_jar_dir = (
        UPSTREAM_ROOT / "CalciteRewrite" / "out" / "artifacts" / "LearnedRewrite_jar"
    )
    calcite_dst_jar_dir = (
        runtime_root / "my_rewriter" / "CalciteRewrite" / "out" / "artifacts" / "LearnedRewrite_jar"
    )
    calcite_dst_jar_dir.mkdir(parents=True, exist_ok=True)
    if calcite_src_jar_dir.is_dir():
        for jar_path in calcite_src_jar_dir.iterdir():
            if jar_path.is_file():
                shutil.copy2(jar_path, calcite_dst_jar_dir / jar_path.name)

    cache_dir = runtime_root / "my_rewriter" / "cache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_file = cache_dir / "common_core_v0_40_pg40_generation_only.jsonl"
    if not cache_file.exists():
        cache_file.write_text("", encoding="utf-8")

    if prompt_log_path.exists():
        prompt_log_path.unlink()
    if raw_response_log_path.exists():
        raw_response_log_path.unlink()

    runner_script = f"""
import json
from pathlib import Path
import my_rewriter.my_utils as my_utils
from my_rewriter.config import init_llms
from my_rewriter.database import DBArgs
from my_rewriter.rag_retrieve import init_docstore
from my_rewriter.test_utils import test

prompt_log_path = Path({str(prompt_log_path)!r})
raw_response_log_path = Path({str(raw_response_log_path)!r})
query_path = Path({str(source_sql_path)!r})
schema_path = Path({str(schema_path)!r})
runner_dir = Path({str(runner_dir)!r})
log_name = {upstream_log_path.stem!r}

def append_jsonl(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False) + "\\n")

orig_chat = my_utils.chat
orig_achat = my_utils.achat

def logged_chat(messages):
    response = orig_chat(messages)
    append_jsonl(prompt_log_path, {{"mode": "chat", "messages": messages}})
    append_jsonl(raw_response_log_path, {{"mode": "chat", "response": response}})
    return response

async def logged_achat(messages, model=None):
    response = await orig_achat(messages, model=model)
    append_jsonl(prompt_log_path, {{"mode": "achat", "messages": messages}})
    append_jsonl(raw_response_log_path, {{"mode": "achat", "response": response}})
    return response

my_utils.chat = logged_chat
my_utils.achat = logged_achat

model_args = init_llms("", load_model=True)
db_args = DBArgs({{
    "host": "",
    "port": 5432,
    "user": "",
    "password": "",
    "dbname": "common_core_v0_40_pg40_generation_only",
    "db": "postgresql",
}})
docstore = init_docstore()
test(
    log_name,
    query_path.read_text(encoding="utf-8"),
    schema_path.read_text(encoding="utf-8"),
    db_args,
    model_args,
    docstore,
    str(runner_dir),
    RETRIEVER_TOP_K={retrieval_top_k},
    CASE_BATCH=5,
    RULE_BATCH=10,
    REWRITE_ROUNDS=1,
    index="hybrid",
)
"""

    env = os.environ.copy()
    env["PYTHONPATH"] = str(runtime_root)
    if base_url:
        env["OPENAI_BASE_URL"] = base_url
        env["OPENAI_API_BASE"] = base_url

    with method_stdout_path.open("w", encoding="utf-8") as stdout_fh, method_stderr_path.open("w", encoding="utf-8") as stderr_fh:
        proc = subprocess.run(
            [str(FORMAL_PYTHON), "-c", runner_script],
            cwd=runtime_root / "my_rewriter",
            env=env,
            stdout=stdout_fh,
            stderr=stderr_fh,
            text=True,
        )

    log_text = ""
    if upstream_log_path.is_file():
        log_text = upstream_log_path.read_text(encoding="utf-8", errors="ignore")
    else:
        log_text = method_stdout_path.read_text(encoding="utf-8", errors="ignore")

    rewrite_payload = extract_rewrite_payload(log_text)
    response_records = parse_response_records(raw_response_log_path)

    selected_rules_payload = {
        "available": False,
        "selection_rounds": re.findall(r"Rules After the \\d+th Selection: ([^\\n]+)", log_text),
        "arranged_rule_sequence": "",
        "rearranged_rule_sequence": "",
    }
    arranged = re.findall(r"Arranged Rule Sequence: ([^\n]+)", log_text)
    rearranged = re.findall(r"Rearranged Rule Sequence: ([^\n]+)", log_text)
    if arranged:
        selected_rules_payload["arranged_rule_sequence"] = arranged[-1]
    if rearranged:
        selected_rules_payload["rearranged_rule_sequence"] = rearranged[-1]
    if rewrite_payload:
        selected_rules_payload["available"] = True
        selected_rules_payload["used_rules"] = rewrite_payload.get("used_rules", [])

    retrieval_line = re.search(r"Retrieved Rewrite Cases: ([^\n]+)", log_text)
    retrieval_trace_payload = {
        "available": retrieval_line is not None,
        "retrieved_cases_log_excerpt": retrieval_line.group(1)[:4000] if retrieval_line else "",
        "retrieval_top_k": retrieval_top_k,
        "reranking_mode": reranking_mode,
        "rrf_k": rrf_k,
        "index_id": index_identifier["index_id"],
        "collection_name": index_identifier["chroma_collection_name"],
    }

    token_cost_payload = {
        "available": bool(rewrite_payload),
        "input_cost": None,
        "output_cost": rewrite_payload.get("output_cost") if rewrite_payload else None,
        "rewrite_time_ms": rewrite_payload.get("time") if rewrite_payload else None,
        "token_usage_available": False,
        "response_record_count": len(response_records),
    }

    if rewrite_payload and str(rewrite_payload.get("output_sql", "")).strip() not in {"", "None"}:
        generated_sql = str(rewrite_payload.get("output_sql", "")).strip()
        write_text(expected_generated_sql_path, generated_sql.rstrip() + "\n")
        row_status = "generated"
        generation_status = "generation_success_with_output_sql"
        output_sql_extracted = True
    else:
        row_status = "failed"
        generation_status = "method_execution_failed" if proc.returncode != 0 else "method_executed_output_sql_missing"
        failure_category = "subprocess_nonzero_exit" if proc.returncode != 0 else "output_sql_missing"
        blocker_reason = f"subprocess exited with code {proc.returncode}" if proc.returncode != 0 else "method finished without extractable output_sql"

    if prompt_log_path.is_file():
        (REPO_ROOT / expected_prompt_path).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(prompt_log_path, REPO_ROOT / expected_prompt_path)
    else:
        write_text(
            expected_prompt_path,
            f"available=false\nrow_status={row_status}\nreason=prompt_log_missing\n",
        )
    if raw_response_log_path.is_file():
        (REPO_ROOT / expected_raw_response_path).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(raw_response_log_path, REPO_ROOT / expected_raw_response_path)
    else:
        write_text(
            expected_raw_response_path,
            f"available=false\nrow_status={row_status}\nreason=raw_response_log_missing\n",
        )

    write_json(expected_selected_rules_path, selected_rules_payload)
    write_json(expected_retrieval_trace_path, retrieval_trace_payload)
    write_json(expected_token_cost_path, token_cost_payload)

    row_metadata.update(
        {
            "row_status": row_status,
            "generation_status": generation_status,
            "failure_category": failure_category,
            "blocker_reason": blocker_reason,
            "output_sql_extracted": output_sql_extracted,
            "response_record_count": len(response_records),
            "method_stdout_path": str(method_stdout_path),
            "method_stderr_path": str(method_stderr_path),
            "upstream_log_path": str(upstream_log_path),
            "temp_runner_dir": str(runner_dir),
            "runtime_patch_root": str(runtime_root),
        }
    )
    write_json(expected_row_metadata_path, row_metadata)

    counts_by_status[row_status] += 1
    run_event_rows.append(
        {
            "run_id": RUN_ID,
            "case_id": case_id,
            "pool": pool,
            "engine": engine,
            "method_id": METHOD_ID,
            "route_id": ROUTE_ID,
            "source_generation_denominator_id": SOURCE_DENOMINATOR_ID,
            "pg_expansion_denominator_id": PG_EXPANSION_DENOMINATOR_ID,
            "previous_generation_status_class": previous_class,
            "row_status": row_status,
            "claim_boundary": CLAIM_BOUNDARY,
            "generated_sql_path": expected_generated_sql_path,
            "prompt_path": expected_prompt_path,
            "raw_response_path": expected_raw_response_path,
            "selected_rules_path": expected_selected_rules_path,
            "retrieval_trace_path": expected_retrieval_trace_path,
            "token_cost_path": expected_token_cost_path,
            "provider_metadata_path": expected_provider_metadata_path,
            "row_run_metadata_path": expected_row_metadata_path,
            "failure_category": failure_category,
            "blocker_reason": blocker_reason,
        }
    )

with RUN_EVENT_LONG_PATH.open("w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=run_event_fieldnames)
    writer.writeheader()
    writer.writerows(run_event_rows)

run_results_payload = {
    "run_id": RUN_ID,
    "method_id": METHOD_ID,
    "route_id": ROUTE_ID,
    "source_generation_denominator_id": SOURCE_DENOMINATOR_ID,
    "pg_expansion_denominator_id": PG_EXPANSION_DENOMINATOR_ID,
    "engine_scope": "pg_only",
    "planned_rows": len(rows),
    "status_counts": dict(sorted(counts_by_status.items())),
    "pool_counts": dict(sorted(counts_by_pool.items())),
    "previous_generation_status_class_counts": dict(sorted(counts_by_previous_class.items())),
    "claim_boundary": CLAIM_BOUNDARY,
    "current_benchmark_metric_evidence": False,
    "notes": [
        "PG-only expansion run",
        "generation-only route",
        "no database or SQL execution in package runner logic",
        "does not replace prior PG7 retained result card",
        "mysql and spark remain unsupported outside this package scope",
    ],
}
RUN_RESULTS_PATH.write_text(json.dumps(run_results_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
PY
