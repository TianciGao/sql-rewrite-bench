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
TMP_RUNNER_ROOT="/tmp/rewritebench_rbot_mysql_spark_canary_01_runtime"

FORMAL_PYTHON="/tmp/rewritebench_rbot_llm4rewrite_venv_smoke/bin/python"
FORMAL_INDEX_DIR="/tmp/rewritebench_rbot_formal_chroma_index_01"
FORMAL_INDEX_IDENTIFIER="$REPO_ROOT/reports/evaluation/common_core_v0/r_bot_formal_index_build_01/formal_chroma_index_identifier_v1.json"
FORMAL_PARAMETER_FREEZE="$REPO_ROOT/reports/evaluation/common_core_v0/r_bot_formal_protocol/r_bot_parameter_freeze_v2.json"
UPSTREAM_ROOT="/tmp/rewritebench_prior_method_audit/LLM4Rewrite"

mkdir -p "$RUN_ROOT"

if [[ ! -f "$FORMAL_PYTHON" ]]; then
  echo "missing formal runtime python: $FORMAL_PYTHON" >&2
  exit 1
fi

if [[ ! -f "$MATRIX_PATH" ]]; then
  echo "missing generation matrix: $MATRIX_PATH" >&2
  exit 1
fi

"$FORMAL_PYTHON" - <<'PY' \
  "$REPO_ROOT" \
  "$RUN_ROOT" \
  "$MATRIX_PATH" \
  "$RESULTS_PATH" \
  "$EVENTS_PATH" \
  "$FORMAL_INDEX_DIR" \
  "$FORMAL_INDEX_IDENTIFIER" \
  "$FORMAL_PARAMETER_FREEZE" \
  "$UPSTREAM_ROOT" \
  "$TMP_RUNNER_ROOT" \
  "$RUN_ID" \
  "$METHOD_ID" \
  "$ROUTE_ID" \
  "$SOURCE_DENOMINATOR_ID" \
  "$CANARY_DENOMINATOR_ID" \
  "$CLAIM_BOUNDARY"
import csv
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
import zipfile
from pathlib import Path
from typing import Any

REPO_ROOT = Path(sys.argv[1])
RUN_ROOT = Path(sys.argv[2])
MATRIX_PATH = Path(sys.argv[3])
RESULTS_PATH = Path(sys.argv[4])
EVENTS_PATH = Path(sys.argv[5])
FORMAL_INDEX_DIR = Path(sys.argv[6])
FORMAL_INDEX_IDENTIFIER = Path(sys.argv[7])
FORMAL_PARAMETER_FREEZE = Path(sys.argv[8])
UPSTREAM_ROOT = Path(sys.argv[9])
TMP_RUNNER_ROOT = Path(sys.argv[10])
RUN_ID = sys.argv[11]
METHOD_ID = sys.argv[12]
ROUTE_ID = sys.argv[13]
SOURCE_DENOMINATOR_ID = sys.argv[14]
CANARY_DENOMINATOR_ID = sys.argv[15]
CLAIM_BOUNDARY = sys.argv[16]

UPSTREAM_RAG_DIR = UPSTREAM_ROOT / "rag"
UPSTREAM_RAG_ZIP = UPSTREAM_RAG_DIR / "stackoverflow-rewrite-embed.zip"
REQUIRED_RAG_JSONL_FILES = [
    "stackoverflow-rewrite-query-optimization.jsonl",
    "stackoverflow-rewrite-rules-query-optimization.jsonl",
    "stackoverflow-rewrite-sql-templates-query-optimization.jsonl",
    "stackoverflow-rewrite-sql-templates-embed-query-optimization.jsonl",
]

ENGINE_RUNTIME = {
    "mysql": {
        "rewriter_database": "MySQL",
        "prompt_label": "MySQL",
    },
    "spark": {
        "rewriter_database": "Spark",
        "prompt_label": "Spark SQL",
    },
}

with FORMAL_PARAMETER_FREEZE.open("r", encoding="utf-8") as handle:
    parameter_freeze = json.load(handle)
with FORMAL_INDEX_IDENTIFIER.open("r", encoding="utf-8") as handle:
    index_identifier = json.load(handle)

benchmark_model_name = parameter_freeze["benchmark_common_config"]["model_config"]["model_name"]
provider_name = parameter_freeze["benchmark_common_config"]["model_config"]["provider_policy"]["provider_name"]
frozen_base_url = parameter_freeze["benchmark_common_config"]["model_config"]["provider_policy"]["base_url"]
retrieval_top_k = parameter_freeze["benchmark_common_config"]["retrieval_parameters"]["top_k"]
embedding_model = index_identifier["embedding_model"]
rule_vector_width = index_identifier["rule_vector_width"]
total_dimension = index_identifier["total_dimension"]
base_url_family = index_identifier["embedding_provider_base_url_family"]

base_url = os.environ.get("OPENAI_BASE_URL", "").strip() or frozen_base_url
api_key = os.environ.get("OPENAI_API_KEY", "")
api_key_visible = bool(api_key)

rows = list(csv.DictReader(MATRIX_PATH.open("r", encoding="utf-8")))

run_event_fieldnames = [
    "run_id",
    "row_key",
    "case_id",
    "pool",
    "engine",
    "method_id",
    "route_id",
    "source_denominator_id",
    "canary_denominator_id",
    "row_status",
    "claim_boundary",
    "generated_sql_path",
    "prompt_path",
    "raw_response_path",
    "selected_rules_path",
    "retrieval_trace_path",
    "token_cost_path",
    "provider_metadata_path",
    "row_metadata_path",
    "failure_category",
    "blocker_reason",
]


def write_text(path_str: str, text: str) -> None:
    path = REPO_ROOT / path_str
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path_str: str, payload: dict[str, Any]) -> None:
    write_text(path_str, json.dumps(payload, indent=2, sort_keys=True) + "\n")


def append_run_event(row: dict[str, Any]) -> None:
    write_header = not EVENTS_PATH.exists()
    with EVENTS_PATH.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=run_event_fieldnames)
        if write_header:
            writer.writeheader()
        writer.writerow(row)


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    if old not in text:
        raise RuntimeError(f"Patch anchor not found in {path}: {old[:120]}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def strip_runtime_jar_signatures(runtime_root: Path) -> dict[str, Any]:
    jar_path = runtime_root / "CalciteRewrite" / "out" / "artifacts" / "LearnedRewrite_jar" / "LearnedRewrite.jar"
    if not jar_path.is_file():
        raise RuntimeError(f"Missing runtime LearnedRewrite.jar at {jar_path}")
    removed: list[str] = []
    tmp_path = jar_path.with_suffix(".unsigned.tmp")
    with zipfile.ZipFile(jar_path, "r") as src, zipfile.ZipFile(tmp_path, "w") as dst:
        for info in src.infolist():
            upper = info.filename.upper()
            if upper.startswith("META-INF/") and (upper.endswith(".SF") or upper.endswith(".DSA") or upper.endswith(".RSA")):
                removed.append(info.filename)
                continue
            dst.writestr(info, src.read(info.filename))
    tmp_path.replace(jar_path)
    return {"jar_path": str(jar_path), "removed_signature_entries": removed}


def ensure_runtime_calcite_layout(runtime_root: Path) -> dict[str, Any]:
    calcite_root = runtime_root / "CalciteRewrite"
    expected_from_cwd = runtime_root / "my_rewriter" / "CalciteRewrite"
    expected_jar_dir = expected_from_cwd / "out" / "artifacts" / "LearnedRewrite_jar"
    expected_jar_path = expected_jar_dir / "LearnedRewrite.jar"

    if not calcite_root.is_dir():
        raise RuntimeError(f"Missing copied CalciteRewrite root at {calcite_root}")

    if expected_from_cwd.exists() or expected_from_cwd.is_symlink():
        if expected_from_cwd.is_symlink() or expected_from_cwd.is_file():
            expected_from_cwd.unlink()
        else:
            shutil.rmtree(expected_from_cwd)
    try:
        os.symlink("../CalciteRewrite", expected_from_cwd, target_is_directory=True)
        layout_mode = "symlinked_relative_into_my_rewriter"
    except OSError:
        shutil.copytree(calcite_root, expected_from_cwd)
        layout_mode = "copied_into_my_rewriter"

    return {
        "layout_mode": layout_mode,
        "calcite_root": str(calcite_root),
        "expected_from_cwd": str(expected_from_cwd),
        "expected_jar_dir": str(expected_jar_dir),
        "expected_jar_exists": expected_jar_path.is_file(),
    }


def provision_required_rag_jsonl(runtime_root: Path) -> dict[str, Any]:
    rag_dir = runtime_root / "rag"
    rag_dir.mkdir(parents=True, exist_ok=True)
    provisioning: dict[str, Any] = {"mode_by_file": {}}
    for filename in REQUIRED_RAG_JSONL_FILES:
        target = rag_dir / filename
        if target.is_file():
            provisioning["mode_by_file"][filename] = "already_present"
            continue
        upstream_file = UPSTREAM_RAG_DIR / filename
        if upstream_file.is_file():
            try:
                os.symlink(upstream_file, target)
                provisioning["mode_by_file"][filename] = "symlinked_upstream_file"
            except OSError:
                shutil.copy2(upstream_file, target)
                provisioning["mode_by_file"][filename] = "copied_upstream_file"
            continue
        if not UPSTREAM_RAG_ZIP.is_file():
            raise RuntimeError(f"Missing required RAG JSONL and retained ZIP fallback: {filename}")
        with zipfile.ZipFile(UPSTREAM_RAG_ZIP, "r") as zf:
            try:
                member = next(name for name in zf.namelist() if name.endswith(filename))
            except StopIteration as exc:
                raise RuntimeError(f"Required RAG JSONL member not found in ZIP: {filename}") from exc
            target.write_bytes(zf.read(member))
            provisioning["mode_by_file"][filename] = f"extracted_from_zip:{member}"
    return provisioning


def prepare_runtime_root(runtime_root: Path) -> dict[str, Any]:
    if runtime_root.exists():
        shutil.rmtree(runtime_root)
    shutil.copytree(UPSTREAM_ROOT, runtime_root)

    runtime_chroma_dir = runtime_root / "rag" / "chroma_db"
    if runtime_chroma_dir.exists() or runtime_chroma_dir.is_symlink():
        if runtime_chroma_dir.is_symlink() or runtime_chroma_dir.is_file():
            runtime_chroma_dir.unlink()
        else:
            shutil.rmtree(runtime_chroma_dir)
    try:
        os.symlink(FORMAL_INDEX_DIR, runtime_chroma_dir, target_is_directory=True)
        chroma_mode = "symlink"
    except OSError:
        shutil.copytree(FORMAL_INDEX_DIR, runtime_chroma_dir)
        chroma_mode = "copied_tree"

    rag_info = provision_required_rag_jsonl(runtime_root)
    jar_info = strip_runtime_jar_signatures(runtime_root)
    calcite_layout_info = ensure_runtime_calcite_layout(runtime_root)

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
        "    res = rewrite(query, create_tables, rule_seq, rounds)\n\n    db = Database(db_args)\n    used_rules = [str(r) for r in res.rules]\n    output_sql = str(res.sql)\n    rewrite_time = int(res.time)\n    output_cost = -1\n    if output_sql != 'None':\n        output_cost = db.cost_estimation(output_sql)\n",
        "    rewrite_database = getattr(db_args, 'rewriter_database', 'PostgreSQL')\n    res = rewrite(query, create_tables, rule_seq, rounds, rewrite_database)\n\n    used_rules = [str(r) for r in res.rules]\n    output_sql = str(res.sql)\n    rewrite_time = int(res.time)\n    output_cost = None\n",
    )

    database_py = runtime_root / "my_rewriter" / "database.py"
    database_py.write_text(
        "import typing as t\n\n"
        "class DBArgs(object):\n"
        "    def __init__(self, config: t.Dict[str, str]):\n"
        "        self.dbtype = config['db']\n"
        "        mapping = {'postgresql': 'PostgreSQL', 'mysql': 'MySQL', 'spark': 'Spark'}\n"
        "        self.rewriter_database = config.get('rewriter_database', mapping.get(self.dbtype, self.dbtype))\n"
        "        self.host = config.get('host', '')\n"
        "        self.port = config.get('port', '')\n"
        "        self.user = config.get('user', '')\n"
        "        self.password = config.get('password', '')\n"
        "        self.dbname = config.get('dbname', 'generation_only')\n"
        "        self.cache = {}\n\n"
        "class Database(object):\n"
        "    def __init__(self, args: DBArgs, timeout: int = -1, enable_indexscan: bool = False):\n"
        "        raise RuntimeError('Database execution adapter is disabled in generation-only canary runtime')\n\n"
        "    def cost_estimation(self, sql: str):\n"
        "        return None\n",
        encoding="utf-8",
    )

    rewrite_py = runtime_root / "my_rewriter" / "rewrite.py"
    rewrite_text = rewrite_py.read_text(encoding="utf-8")
    original_block = (
        "def match_normal_rules(query: str, create_tables: t.List[str], database: str = 'PostgreSQL', verbose: bool = True) -> t.List[t.Dict[str, str]]:\n"
        "    return to_python_list(Rewriter.matchNormalRules(to_java_string(query), to_java_list(create_tables), to_java_string(database), to_java_bool(verbose)))\n\n"
        "def match_explore_rules(query: str, create_tables: t.List[str], database: str = 'PostgreSQL', verbose: bool = True) -> t.List[t.Dict[str, str]]:\n"
        "    return to_python_list(Rewriter.matchExploreRules(to_java_string(query), to_java_list(create_tables), to_java_string(database), to_java_bool(verbose)))\n\n"
        "def match_all_rules(query: str, create_tables: t.List[str], database: str = 'PostgreSQL', verbose: bool = True) -> t.List[t.Dict[str, str]]:\n"
        "    return to_python_list(Rewriter.matchAllRules(to_java_string(query), to_java_list(create_tables), to_java_string(database), to_java_bool(verbose)))\n\n"
        "def rewrite(query: str, create_tables: t.List[str], rule_names: t.List[str], rounds: int, database: str = 'PostgreSQL') -> RewriteResult:\n"
        "    return Rewriter.rewrite(to_java_string(query), to_java_list(create_tables), to_java_list(rule_names), to_java_int(rounds), to_java_string(database))\n"
    )
    patched_block = (
        "def _runtime_database(database: str | None = None) -> str:\n"
        "    if database:\n"
        "        return database\n"
        "    return os.environ.get('RBOT_REWRITER_DATABASE', 'PostgreSQL')\n\n"
        "def match_normal_rules(query: str, create_tables: t.List[str], database: str | None = None, verbose: bool = True) -> t.List[t.Dict[str, str]]:\n"
        "    database = _runtime_database(database)\n"
        "    return to_python_list(Rewriter.matchNormalRules(to_java_string(query), to_java_list(create_tables), to_java_string(database), to_java_bool(verbose)))\n\n"
        "def match_explore_rules(query: str, create_tables: t.List[str], database: str | None = None, verbose: bool = True) -> t.List[t.Dict[str, str]]:\n"
        "    database = _runtime_database(database)\n"
        "    return to_python_list(Rewriter.matchExploreRules(to_java_string(query), to_java_list(create_tables), to_java_string(database), to_java_bool(verbose)))\n\n"
        "def match_all_rules(query: str, create_tables: t.List[str], database: str | None = None, verbose: bool = True) -> t.List[t.Dict[str, str]]:\n"
        "    database = _runtime_database(database)\n"
        "    return to_python_list(Rewriter.matchAllRules(to_java_string(query), to_java_list(create_tables), to_java_string(database), to_java_bool(verbose)))\n\n"
        "def rewrite(query: str, create_tables: t.List[str], rule_names: t.List[str], rounds: int, database: str | None = None) -> RewriteResult:\n"
        "    database = _runtime_database(database)\n"
        "    return Rewriter.rewrite(to_java_string(query), to_java_list(create_tables), to_java_list(rule_names), to_java_int(rounds), to_java_string(database))\n"
    )
    if original_block not in rewrite_text:
        raise RuntimeError("rewrite.py runtime database anchor not found")
    rewrite_py.write_text(rewrite_text.replace(original_block, patched_block, 1), encoding="utf-8")

    return {
        "chroma_mode": chroma_mode,
        "rag_jsonl": rag_info,
        "jar_patch": jar_info,
        "calcite_layout": calcite_layout_info,
    }


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


def extract_rewrite_payload(log_text: str) -> dict[str, Any] | None:
    matches = re.findall(r"Rewrite Execution Results: (\{.*?\})", log_text)
    if not matches:
        return None
    candidate = matches[-1]
    candidate_json = candidate.replace("'", '"').replace("None", "null")
    try:
        return json.loads(candidate_json)
    except json.JSONDecodeError:
        return None


def write_preflight_block(rows_to_block: list[dict[str, str]], failure_category: str, failure_reason: str) -> None:
    for row in rows_to_block:
        append_run_event({
            "run_id": RUN_ID,
            "row_key": row["row_key"],
            "case_id": row["case_id"],
            "pool": row["pool"],
            "engine": row["engine"],
            "method_id": METHOD_ID,
            "route_id": ROUTE_ID,
            "source_denominator_id": SOURCE_DENOMINATOR_ID,
            "canary_denominator_id": CANARY_DENOMINATOR_ID,
            "row_status": "preflight_blocked",
            "claim_boundary": CLAIM_BOUNDARY,
            "generated_sql_path": row["expected_generated_sql_path"],
            "prompt_path": row["expected_prompt_path"],
            "raw_response_path": row["expected_raw_response_path"],
            "selected_rules_path": row["expected_selected_rules_path"],
            "retrieval_trace_path": row["expected_retrieval_trace_path"],
            "token_cost_path": row["expected_token_cost_path"],
            "provider_metadata_path": row["expected_provider_metadata_path"],
            "row_metadata_path": row["expected_row_metadata_path"],
            "failure_category": failure_category,
            "blocker_reason": failure_reason,
        })
        write_json(row["expected_row_metadata_path"], {
            "run_id": RUN_ID,
            "case_id": row["case_id"],
            "engine": row["engine"],
            "method_id": METHOD_ID,
            "route_id": ROUTE_ID,
            "source_denominator_id": SOURCE_DENOMINATOR_ID,
            "canary_denominator_id": CANARY_DENOMINATOR_ID,
            "row_status": "preflight_blocked",
            "claim_boundary": CLAIM_BOUNDARY,
            "failure_category": failure_category,
            "failure_reason": failure_reason,
            "source_sql_path": row["source_sql_path"],
            "schema_path": row["schema_path"],
            "witness_data_path": row["witness_data_path"],
            "witness_data_used_for_generation": False,
        })


def run_optional_provider_preflight() -> tuple[bool, str]:
    if os.environ.get("RBOT_CANARY_ALLOW_PROVIDER_PREFLIGHT_CALL", "0") != "1":
        return True, ""
    if not base_url or not api_key:
        return False, "OPENAI_BASE_URL or OPENAI_API_KEY missing for optional provider preflight"
    candidates = [f"{base_url.rstrip('/')}/models"]
    if not base_url.rstrip("/").endswith("/v1"):
        candidates.append(f"{base_url.rstrip('/')}/v1/models")
    last_error = "provider preflight failed"
    for url in candidates:
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {api_key}"})
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                if 200 <= resp.status < 300:
                    return True, ""
                last_error = f"unexpected provider preflight status {resp.status} at {url}"
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as exc:
            last_error = f"{type(exc).__name__} at {url}: {exc}"
    return False, last_error


def run_engine_preflight(engine: str) -> tuple[bool, str, str]:
    runtime_root = TMP_RUNNER_ROOT / f"preflight_{engine}"
    try:
        runtime_info = prepare_runtime_root(runtime_root)
    except Exception as exc:
        return False, "runtime_patch_failed", str(exc)

    for filename in REQUIRED_RAG_JSONL_FILES:
        if not (runtime_root / "rag" / filename).is_file():
            return False, "missing_rag_jsonl", f"Required RAG JSONL missing after runtime prep: {filename}"

    actual_cwd = runtime_root / "my_rewriter"
    expected_jar_dir = actual_cwd / "CalciteRewrite" / "out" / "artifacts" / "LearnedRewrite_jar"
    expected_jar_path = expected_jar_dir / "LearnedRewrite.jar"
    jar_layout_info = {
        "actual_cwd": str(actual_cwd),
        "runtime_root": str(runtime_root),
        "expected_calcite_jar_dir": str(expected_jar_dir),
        "learned_rewrite_jar_exists": expected_jar_path.is_file(),
    }
    if not expected_jar_dir.is_dir() or not expected_jar_path.is_file():
        return False, "calcite_rewrite_jar_missing", json.dumps(jar_layout_info, sort_keys=True)

    preflight_script = f"""
from my_rewriter.database import DBArgs
from my_rewriter.rag_retrieve import init_docstore
from my_rewriter.rewrite import Rewriter, RewriteResult, MyRules
DBArgs({{"db": {engine!r}, "rewriter_database": {ENGINE_RUNTIME[engine]["rewriter_database"]!r}, "dbname": "generation_only"}})
init_docstore()
print("preflight_ok")
"""
    env = os.environ.copy()
    env["PYTHONPATH"] = str(runtime_root)
    env["RBOT_REWRITER_DATABASE"] = ENGINE_RUNTIME[engine]["rewriter_database"]
    if base_url:
        env["OPENAI_BASE_URL"] = base_url
        env["OPENAI_API_BASE"] = base_url
    proc = subprocess.run(
        [str(Path(sys.executable)), "-c", preflight_script],
        cwd=actual_cwd,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if proc.returncode != 0:
        failure_info = {
            **jar_layout_info,
            "runtime_info": runtime_info,
            "stderr": proc.stderr.strip(),
            "stdout": proc.stdout.strip(),
        }
        return False, "java_or_runtime_import_failed", json.dumps(failure_info, sort_keys=True)
    success_info = {
        **jar_layout_info,
        "runtime_info": runtime_info,
        "stdout": proc.stdout.strip(),
    }
    return True, "ok", json.dumps(success_info, sort_keys=True)


def generate_row(row: dict[str, str]) -> tuple[str, str]:
    engine = row["engine"]
    runtime_root = TMP_RUNNER_ROOT / row["case_id"] / engine
    runtime_info = prepare_runtime_root(runtime_root)

    method_stdout_path = REPO_ROOT / f"reports/evaluation/common_core_v0/runs/{RUN_ID}/logs/{row['case_id']}/{engine}/generation.stdout.log"
    method_stderr_path = REPO_ROOT / f"reports/evaluation/common_core_v0/runs/{RUN_ID}/logs/{row['case_id']}/{engine}/generation.stderr.log"
    prompt_log_path = REPO_ROOT / row["expected_prompt_path"]
    raw_response_log_path = REPO_ROOT / row["expected_raw_response_path"]
    generated_sql_path = row["expected_generated_sql_path"]
    selected_rules_path = row["expected_selected_rules_path"]
    retrieval_trace_path = row["expected_retrieval_trace_path"]
    token_cost_path = row["expected_token_cost_path"]
    provider_metadata_path = row["expected_provider_metadata_path"]
    row_metadata_path = row["expected_row_metadata_path"]

    for path in [method_stdout_path, method_stderr_path, prompt_log_path, raw_response_log_path]:
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists():
            path.unlink()

    source_sql_path = REPO_ROOT / row["source_sql_path"]
    schema_path = REPO_ROOT / row["schema_path"]
    runner_dir = runtime_root / "tmp_logs"
    runner_dir.mkdir(parents=True, exist_ok=True)
    upstream_log_path = runner_dir / f"{row['case_id']}_{engine}_{int(time.time() * 1000)}.log"
    engine_prompt_label = ENGINE_RUNTIME[engine]["prompt_label"]
    rewriter_database = ENGINE_RUNTIME[engine]["rewriter_database"]

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
engine_prompt_label = {engine_prompt_label!r}

def append_jsonl(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False) + "\\n")

def decorate_messages(messages):
    preface = {{
        "role": "system",
        "content": f"Target SQL engine: {{engine_prompt_label}}. Preserve this engine's dialect and syntax. Do not rewrite into PostgreSQL unless the target engine is PostgreSQL."
    }}
    return [preface] + list(messages)

orig_chat = my_utils.chat
orig_achat = my_utils.achat

def logged_chat(messages):
    decorated = decorate_messages(messages)
    response = orig_chat(decorated)
    append_jsonl(prompt_log_path, {{"mode": "chat", "target_engine": engine_prompt_label, "messages": decorated}})
    append_jsonl(raw_response_log_path, {{"mode": "chat", "target_engine": engine_prompt_label, "response": response}})
    return response

async def logged_achat(messages, model=None):
    decorated = decorate_messages(messages)
    response = await orig_achat(decorated, model=model)
    append_jsonl(prompt_log_path, {{"mode": "achat", "target_engine": engine_prompt_label, "messages": decorated}})
    append_jsonl(raw_response_log_path, {{"mode": "achat", "target_engine": engine_prompt_label, "response": response}})
    return response

my_utils.chat = logged_chat
my_utils.achat = logged_achat

model_args = init_llms("", load_model=True)
db_args = DBArgs({{
    "host": "",
    "port": "",
    "user": "",
    "password": "",
    "dbname": "generation_only",
    "db": {engine!r},
    "rewriter_database": {rewriter_database!r},
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
    env["RBOT_REWRITER_DATABASE"] = rewriter_database
    if base_url:
        env["OPENAI_BASE_URL"] = base_url
        env["OPENAI_API_BASE"] = base_url

    with method_stdout_path.open("w", encoding="utf-8") as stdout_fh, method_stderr_path.open("w", encoding="utf-8") as stderr_fh:
        proc = subprocess.run(
            [str(Path(sys.executable)), "-c", runner_script],
            cwd=runtime_root / "my_rewriter",
            env=env,
            stdout=stdout_fh,
            stderr=stderr_fh,
            text=True,
        )

    if upstream_log_path.is_file():
        log_text = upstream_log_path.read_text(encoding="utf-8", errors="ignore")
    else:
        log_text = method_stdout_path.read_text(encoding="utf-8", errors="ignore")

    rewrite_payload = extract_rewrite_payload(log_text)
    response_records = parse_response_records(raw_response_log_path)
    arranged = re.findall(r"Arranged Rule Sequence: ([^\n]+)", log_text)
    rearranged = re.findall(r"Rearranged Rule Sequence: ([^\n]+)", log_text)
    selection_rounds = re.findall(r"Rules After the \d+th Selection: ([^\n]+)", log_text)
    retrieval_line = re.search(r"Retrieved Rewrite Cases: ([^\n]+)", log_text)

    selected_rules_payload = {
        "available": bool(rewrite_payload),
        "selection_rounds": selection_rounds,
        "arranged_rule_sequence": arranged[-1] if arranged else "",
        "rearranged_rule_sequence": rearranged[-1] if rearranged else "",
        "used_rules": rewrite_payload.get("used_rules", []) if rewrite_payload else [],
    }
    retrieval_trace_payload = {
        "available": retrieval_line is not None,
        "retrieved_cases_log_excerpt": retrieval_line.group(1)[:4000] if retrieval_line else "",
    }
    token_cost_payload = {
        "available": False,
        "input_token_count": None,
        "output_token_count": None,
        "estimated_total_cost_usd": None,
    }
    provider_metadata = {
        "provider_name": provider_name,
        "openai_api_key_visible": api_key_visible,
        "openai_base_url_visible": bool(base_url),
        "openai_base_url_family": base_url_family,
        "base_url": base_url,
        "benchmark_model_name": benchmark_model_name,
        "embedding_model": embedding_model,
        "rule_vector_width": rule_vector_width,
        "total_dimension": total_dimension,
        "target_engine": engine,
        "target_engine_prompt_label": engine_prompt_label,
        "rewriter_database": rewriter_database,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    row_metadata = {
        "run_id": RUN_ID,
        "case_id": row["case_id"],
        "pool": row["pool"],
        "engine": engine,
        "method_id": METHOD_ID,
        "route_id": ROUTE_ID,
        "source_denominator_id": SOURCE_DENOMINATOR_ID,
        "canary_denominator_id": CANARY_DENOMINATOR_ID,
        "claim_boundary": CLAIM_BOUNDARY,
        "generation_only": True,
        "source_sql_path": row["source_sql_path"],
        "schema_path": row["schema_path"],
        "witness_data_path": row["witness_data_path"],
        "witness_data_used_for_generation": False,
        "runtime_patch_info": runtime_info,
        "target_engine_prompt_label": engine_prompt_label,
        "rewriter_database": rewriter_database,
    }

    write_json(selected_rules_path, selected_rules_payload)
    write_json(retrieval_trace_path, retrieval_trace_payload)
    write_json(token_cost_path, token_cost_payload)
    write_json(provider_metadata_path, provider_metadata)

    if proc.returncode != 0:
        row_metadata["row_status"] = "failed"
        row_metadata["failure_category"] = "subprocess_nonzero_exit"
        row_metadata["failure_reason"] = f"subprocess exited with code {proc.returncode}"
        write_json(row_metadata_path, row_metadata)
        return "failed", row_metadata["failure_reason"]

    if not rewrite_payload or not rewrite_payload.get("output_sql") or rewrite_payload.get("output_sql") == "None":
        row_metadata["row_status"] = "failed"
        row_metadata["failure_category"] = "output_sql_missing"
        row_metadata["failure_reason"] = "method finished without extractable output_sql"
        write_json(row_metadata_path, row_metadata)
        return "failed", row_metadata["failure_reason"]

    write_text(generated_sql_path, rewrite_payload["output_sql"].strip() + "\n")
    row_metadata["row_status"] = "generated"
    row_metadata["rewrite_payload"] = rewrite_payload
    row_metadata["raw_response_record_count"] = len(response_records)
    write_json(row_metadata_path, row_metadata)
    return "generated", ""


if EVENTS_PATH.exists():
    EVENTS_PATH.unlink()

package_failures: list[tuple[str, str]] = []
if not api_key_visible:
    package_failures.append(("missing_env_visibility", "OPENAI_API_KEY is not visible in the current shell"))
if not base_url:
    package_failures.append(("missing_env_visibility", "OPENAI_BASE_URL is not visible in the current shell and no frozen base_url was available"))
if not FORMAL_INDEX_DIR.is_dir():
    package_failures.append(("missing_formal_index_dir", "Formal Chroma index directory is not visible"))
if not FORMAL_INDEX_IDENTIFIER.is_file():
    package_failures.append(("missing_formal_index_identifier", "Formal Chroma index identifier is not visible"))
if not FORMAL_PARAMETER_FREEZE.is_file():
    package_failures.append(("missing_formal_parameter_freeze", "Formal parameter freeze JSON is not visible"))
if not UPSTREAM_ROOT.is_dir():
    package_failures.append(("missing_upstream_llm4rewrite_root", "Visible upstream LLM4Rewrite tree is not available"))

missing_artifacts = []
for row in rows:
    for key in ("source_sql_path", "schema_path", "witness_data_path"):
        rel = row[key]
        if not (REPO_ROOT / rel).is_file():
            missing_artifacts.append(f"{row['row_key']}:{key}:{rel}")
if missing_artifacts:
    package_failures.append(("missing_case_artifact", "; ".join(missing_artifacts)))

provider_ok, provider_reason = run_optional_provider_preflight()
if not provider_ok:
    package_failures.append(("provider_preflight_failed", provider_reason))

engine_preflight: dict[str, tuple[bool, str, str]] = {}
if not package_failures:
    for engine in sorted({row["engine"] for row in rows}):
        engine_preflight[engine] = run_engine_preflight(engine)

status_counts = {
    "generated": 0,
    "failed": 0,
    "preflight_blocked": 0,
}

if package_failures:
    failure_category, failure_reason = package_failures[0]
    write_preflight_block(rows, failure_category, failure_reason)
    status_counts["preflight_blocked"] = len(rows)
    results = {
        "run_id": RUN_ID,
        "method_id": METHOD_ID,
        "route_id": ROUTE_ID,
        "source_denominator_id": SOURCE_DENOMINATOR_ID,
        "canary_denominator_id": CANARY_DENOMINATOR_ID,
        "claim_boundary": CLAIM_BOUNDARY,
        "status": "preflight_failed",
        "failure_category": failure_category,
        "failure_reason": failure_reason,
        "planned_rows": len(rows),
        "status_counts": status_counts,
        "engine_scope": "mysql_and_spark_canary_only",
        "current_benchmark_metric_evidence": False,
        "notes": [
            "human-run only package",
            "generation-only canary",
            "no SQL execution in this runner",
            "no timing or speedup evidence",
        ],
    }
else:
    generated_rows: list[str] = []
    failed_rows: list[str] = []
    blocked_rows: list[str] = []
    for row in rows:
        engine = row["engine"]
        ok, category, reason = engine_preflight[engine]
        if not ok:
            write_preflight_block([row], category, reason)
            status_counts["preflight_blocked"] += 1
            blocked_rows.append(row["row_key"])
            continue
        row_status, reason = generate_row(row)
        event_failure_category = ""
        event_blocker_reason = ""
        if row_status == "generated":
            generated_rows.append(row["row_key"])
            status_counts["generated"] += 1
        else:
            failed_rows.append(row["row_key"])
            status_counts["failed"] += 1
            event_failure_category = "generation_failed"
            event_blocker_reason = reason
        append_run_event({
            "run_id": RUN_ID,
            "row_key": row["row_key"],
            "case_id": row["case_id"],
            "pool": row["pool"],
            "engine": row["engine"],
            "method_id": METHOD_ID,
            "route_id": ROUTE_ID,
            "source_denominator_id": SOURCE_DENOMINATOR_ID,
            "canary_denominator_id": CANARY_DENOMINATOR_ID,
            "row_status": row_status,
            "claim_boundary": CLAIM_BOUNDARY,
            "generated_sql_path": row["expected_generated_sql_path"],
            "prompt_path": row["expected_prompt_path"],
            "raw_response_path": row["expected_raw_response_path"],
            "selected_rules_path": row["expected_selected_rules_path"],
            "retrieval_trace_path": row["expected_retrieval_trace_path"],
            "token_cost_path": row["expected_token_cost_path"],
            "provider_metadata_path": row["expected_provider_metadata_path"],
            "row_metadata_path": row["expected_row_metadata_path"],
            "failure_category": event_failure_category,
            "blocker_reason": event_blocker_reason,
        })

    status = "completed"
    if status_counts["generated"] == 0 and status_counts["failed"] == 0 and status_counts["preflight_blocked"] == len(rows):
        status = "preflight_failed"
    elif status_counts["failed"] > 0 or status_counts["preflight_blocked"] > 0:
        status = "completed_with_failures"

    results = {
        "run_id": RUN_ID,
        "method_id": METHOD_ID,
        "route_id": ROUTE_ID,
        "source_denominator_id": SOURCE_DENOMINATOR_ID,
        "canary_denominator_id": CANARY_DENOMINATOR_ID,
        "claim_boundary": CLAIM_BOUNDARY,
        "status": status,
        "planned_rows": len(rows),
        "status_counts": status_counts,
        "engine_scope": "mysql_and_spark_canary_only",
        "generated_rows": generated_rows,
        "failed_rows": failed_rows,
        "preflight_blocked_rows": blocked_rows,
        "engine_preflight": {
            engine: {
                "ok": ok,
                "category": category,
                "reason": reason,
            }
            for engine, (ok, category, reason) in engine_preflight.items()
        },
        "current_benchmark_metric_evidence": False,
        "notes": [
            "human-run only package",
            "generation-only canary",
            "uses non-PostgreSQL generation-only adapter recovery in temp runtime",
            "does not execute SQL or witness data",
            "does not produce timing or speedup evidence",
        ],
    }

RESULTS_PATH.write_text(json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8")
PY
