#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import math
import os
import re
import shutil
import statistics
import subprocess
import sys
import time
import traceback
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit, urlunsplit

from openai import OpenAI


REPO_ROOT = Path(__file__).resolve().parents[5]
RUN_ROOT = Path(__file__).resolve().parent
FREEZE_ROOT = REPO_ROOT / "reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1"
PREFLIGHT_RUN_ROOT = REPO_ROOT / "reports/evaluation/common_core_v0/runs/direct_llm_execute_repair_preflight_01"
ORIG_GEN_RUN = REPO_ROOT / "reports/evaluation/common_core_v0/runs/direct_llm_same_engine_generation_01"
ORIG_EXEC_RUN = REPO_ROOT / "reports/evaluation/common_core_v0/runs/direct_llm_same_engine_execution_01"

CANDIDATE_SET_CSV = FREEZE_ROOT / "direct_llm_execute_repair_candidate_set_v1.csv"
PROMPT_MANIFEST_CSV = FREEZE_ROOT / "direct_llm_execute_repair_prompt_input_manifest_v1.csv"
PREFLIGHT_SUMMARY_CSV = FREEZE_ROOT / "direct_llm_execute_repair_preflight_summary_v1.csv"
PRELIGHT_PROTOCOL_MD = FREEZE_ROOT / "direct_llm_execute_repair_protocol_v1.md"
MODEL_AUDIT_CSV = FREEZE_ROOT / "direct_llm_original_model_metadata_audit_v1.csv"
MODEL_RECOMMENDATION_MD = FREEZE_ROOT / "direct_llm_execute_repair_model_policy_recommendation_v1.md"
ORIG_GEN_RESULTS_JSON = ORIG_GEN_RUN / "run_results.json"
ORIG_EXEC_RESULTS_JSON = ORIG_EXEC_RUN / "run_results.json"
ORIG_EXEC_TRIAGE_CSV = ORIG_EXEC_RUN / "execution_triage.csv"
ORIG_TIMING_CASE_LEVEL_CSV = FREEZE_ROOT / "method_timing_case_level_v1.csv"

README_PATH = RUN_ROOT / "README.md"
REPAIR_POLICY_MD = RUN_ROOT / "repair_policy_v1.md"
REPAIR_PROMPT_TEMPLATE_MD = RUN_ROOT / "repair_prompt_template_v1.md"
REPAIR_GENERATION_CSV = RUN_ROOT / "repair_generation_event_long.csv"
REPAIR_EXECUTION_CSV = RUN_ROOT / "repair_execution_event_long.csv"
FINAL_OUTCOME_CSV = RUN_ROOT / "final_outcome_long.csv"
REPAIR_TIMING_CSV = RUN_ROOT / "repair_timing_event_long.csv"
FINAL_TIMING_SUMMARY_CSV = RUN_ROOT / "final_timing_summary.csv"
FINAL_TIMING_SUMMARY_MD = RUN_ROOT / "final_timing_summary.md"
REPAIR_RESULT_SUMMARY_CSV = RUN_ROOT / "repair_result_summary.csv"
REPAIR_RESULT_SUMMARY_MD = RUN_ROOT / "repair_result_summary.md"
REPAIR_FAILURES_CSV = RUN_ROOT / "repair_failures.csv"
REPAIRED_SQL_MANIFEST_CSV = RUN_ROOT / "repaired_sql_manifest.csv"
RUN_RESULTS_JSON = RUN_ROOT / "run_results.json"
VALIDATION_REPORT_JSON = RUN_ROOT / "validation_report.json"
RAW_RESPONSES_DIR = RUN_ROOT / "raw_responses"
REPAIRED_SQL_DIR = RUN_ROOT / "repaired_sql"
PROMPTS_DIR = RUN_ROOT / "prompts"
LOGS_DIR = RUN_ROOT / "logs"
WORKSPACES_DIR = RUN_ROOT / "workspaces"
TIMINGS_DIR = RUN_ROOT / "timings"

RESULT_CARD_CSV = FREEZE_ROOT / "direct_llm_execute_repair_1shot_result_card_v1.csv"
RESULT_CARD_MD = FREEZE_ROOT / "direct_llm_execute_repair_1shot_result_card_v1.md"

METHOD_ID = "direct_llm"
ROUTE_ID = "direct_llm_execute_repair_1shot"
ORIGINAL_ROUTE_ID = "direct_llm_same_engine_rewrite"
DENOMINATOR_ID = "common_core_v0_40_same_engine_120"
MODEL_NAME = "gpt-4o-mini"
TEMPERATURE = 0
TOP_P = 1
MAX_TOKENS = 2048
PROVIDER_FAMILY = "api.gptsapi.net"
REPAIR_ATTEMPTS = 1
EXPECTED_PLANNED_ROWS = 120
EXPECTED_ORIGINAL_EXACT_ROWS = 94
EXPECTED_READY_ROWS = 21
EXPECTED_BLOCKED_ROWS = 5
WARMUP_COUNT = 1
REPEAT_COUNT = 3

REQUIRED_ENV_VARS = ("OPENAI_API_KEY",)
SQL_START_KEYWORDS = ("select", "with", "values", "(")
PROSE_MARKERS = (
    "here is",
    "here's",
    "the repaired",
    "the sql",
    "explanation",
    "i fixed",
    "i repaired",
    "below is",
)


@dataclass
class CandidateRow:
    repair_row_id: str
    case_id: str
    pool: str
    engine: str
    denominator_id: str
    original_outcome_class: str
    original_generated: bool
    original_ready: bool
    original_executed: bool
    original_exact: bool
    original_timing_success: bool
    failure_category: str
    failure_detail_available: bool
    source_sql_artifact: str
    schema_artifact: str
    first_candidate_sql_artifact: str
    result_check_artifact: str
    execution_error_artifact: str
    checker_feedback_artifact: str
    repair_candidate_status: str
    repair_block_reason: str
    source_artifacts: str
    notes: str


@dataclass
class ManifestRow:
    repair_row_id: str
    case_id: str
    engine: str
    prompt_input_json: str
    ready_for_llm_call: bool
    blocked_reason: str
    notes: str


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def write_text(path: Path, content: str) -> None:
    ensure_parent(path)
    path.write_text(content, encoding="utf-8")


def write_json(path: Path, payload: Any) -> None:
    write_text(path, json.dumps(payload, indent=2) + "\n")


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, Any]]) -> None:
    ensure_parent(path)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({name: row.get(name, "") for name in fieldnames})


def render_markdown_table(fieldnames: list[str], rows: list[dict[str, Any]]) -> str:
    header = "| " + " | ".join(fieldnames) + " |"
    sep = "| " + " | ".join(["---"] * len(fieldnames)) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(name, "")) for name in fieldnames) + " |")
    return "\n".join([header, sep, *body]) + "\n"


def parse_bool(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "yes", "1"}


def load_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def load_candidates() -> dict[str, CandidateRow]:
    rows = {}
    for row in load_csv_rows(CANDIDATE_SET_CSV):
        rows[row["repair_row_id"]] = CandidateRow(
            repair_row_id=row["repair_row_id"],
            case_id=row["case_id"],
            pool=row["pool"],
            engine=row["engine"],
            denominator_id=row["denominator_id"],
            original_outcome_class=row["original_outcome_class"],
            original_generated=parse_bool(row["original_generated"]),
            original_ready=parse_bool(row["original_ready"]),
            original_executed=parse_bool(row["original_executed"]),
            original_exact=parse_bool(row["original_exact"]),
            original_timing_success=parse_bool(row["original_timing_success"]),
            failure_category=row["failure_category"],
            failure_detail_available=parse_bool(row["failure_detail_available"]),
            source_sql_artifact=row["source_sql_artifact"],
            schema_artifact=row["schema_artifact"],
            first_candidate_sql_artifact=row["first_candidate_sql_artifact"],
            result_check_artifact=row["result_check_artifact"],
            execution_error_artifact=row["execution_error_artifact"],
            checker_feedback_artifact=row["checker_feedback_artifact"],
            repair_candidate_status=row["repair_candidate_status"],
            repair_block_reason=row["repair_block_reason"],
            source_artifacts=row["source_artifacts"],
            notes=row["notes"],
        )
    return rows


def load_manifest() -> dict[str, ManifestRow]:
    rows = {}
    for row in load_csv_rows(PROMPT_MANIFEST_CSV):
        rows[row["repair_row_id"]] = ManifestRow(
            repair_row_id=row["repair_row_id"],
            case_id=row["case_id"],
            engine=row["engine"],
            prompt_input_json=row["prompt_input_json"],
            ready_for_llm_call=parse_bool(row["ready_for_llm_call"]),
            blocked_reason=row["blocked_reason"],
            notes=row["notes"],
        )
    return rows


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def read_text_rel(path_str: str) -> str:
    return (REPO_ROOT / path_str).read_text(encoding="utf-8").strip()


def require_env() -> dict[str, str]:
    missing = [name for name in REQUIRED_ENV_VARS if not os.environ.get(name)]
    if not (os.environ.get("OPENAI_BASE_URL") or os.environ.get("OPENAI_API_BASE")):
        missing.append("OPENAI_BASE_URL")
    if missing:
        raise RuntimeError("Missing required environment variables: " + ", ".join(missing))
    base_url = os.environ.get("OPENAI_BASE_URL") or os.environ.get("OPENAI_API_BASE") or ""
    return {"api_key": os.environ["OPENAI_API_KEY"], "base_url": base_url}


def sanitize_base_url(raw_url: str) -> str:
    parts = urlsplit(raw_url)
    netloc = parts.hostname or parts.netloc
    if parts.port:
        netloc = f"{netloc}:{parts.port}"
    return urlunsplit((parts.scheme, netloc, parts.path, "", ""))


def provider_from_base_url(base_url: str) -> str:
    parts = urlsplit(base_url)
    return parts.hostname or "openai_compatible"


def build_prompt(payload: dict[str, Any]) -> str:
    return (
        "You are repairing a SQL rewrite.\n\n"
        "Goal:\n"
        "Return one complete SQL statement that is semantically equivalent to the source SQL and executable on the target engine.\n\n"
        f"Target engine:\n{payload['engine']}\n\n"
        f"Schema:\n{payload['schema_or_ddl']}\n\n"
        f"Source SQL:\n{payload['source_sql']}\n\n"
        f"Previous candidate SQL:\n{payload['first_candidate_sql']}\n\n"
        f"Observed failure:\n{payload['observed_failure']}\n\n"
        f"Checker or execution context:\n{payload['checker_or_execution_context']}\n\n"
        "Rules:\n"
        "- Return exactly one complete SQL statement.\n"
        "- Do not include markdown.\n"
        "- Do not include explanation.\n"
        "- Do not include comments unless required by SQL syntax.\n"
        "- Preserve source semantics.\n"
        "- Use only tables and columns from the schema.\n"
        "- Use syntax supported by the target engine.\n"
    )


def classify_output(text: str) -> tuple[bool, str, str]:
    stripped = text.strip()
    if not stripped:
        return False, "extraction_failed", "empty_output"
    if "```" in stripped:
        return False, "extraction_failed", "markdown_fence_detected"
    lowered = stripped.lower()
    if any(marker in lowered for marker in PROSE_MARKERS):
        return False, "extraction_failed", "obvious_prose_marker_detected"
    first = ""
    for raw_line in stripped.splitlines():
        line = raw_line.strip()
        if line:
            first = line
            break
    if not first:
        return False, "extraction_failed", "empty_output"
    if not any(first.lower().startswith(keyword) for keyword in SQL_START_KEYWORDS):
        return False, "extraction_failed", "first_line_not_sql_like"
    return True, "accepted", ""


def extract_response_text(response: Any) -> str:
    if not getattr(response, "choices", None):
        return ""
    message = response.choices[0].message
    content = getattr(message, "content", "")
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: list[str] = []
        for item in content:
            text = getattr(item, "text", None)
            if text:
                parts.append(text)
            elif isinstance(item, dict) and item.get("text"):
                parts.append(str(item["text"]))
        return "\n".join(parts)
    return ""


def normalize_query_text(text: str) -> str:
    return text.strip().rstrip(";").strip()


def compare_tsv_outputs(source_path: Path, generated_path: Path) -> dict[str, Any]:
    source_text = source_path.read_text(encoding="utf-8")
    generated_text = generated_path.read_text(encoding="utf-8")
    exact_match = source_text == generated_text
    sorted_match = sorted(line.rstrip("\n") for line in source_text.splitlines()) == sorted(
        line.rstrip("\n") for line in generated_text.splitlines()
    )
    if exact_match:
        status = "match_exact"
    elif sorted_match:
        status = "match_after_sort_normalization"
    else:
        status = "mismatch"
    return {
        "exact_match": exact_match,
        "sorted_match": sorted_match,
        "consistency_check_status": status,
        "source_output_path": str(source_path.relative_to(REPO_ROOT)),
        "generated_output_path": str(generated_path.relative_to(REPO_ROOT)),
    }


def mysql_args() -> list[str]:
    args = ["mysql"]
    if os.environ.get("MYSQL_HOST"):
        args.extend(["--host", os.environ["MYSQL_HOST"]])
    if os.environ.get("MYSQL_PORT"):
        args.extend(["--port", os.environ["MYSQL_PORT"]])
    if os.environ.get("MYSQL_USER"):
        args.extend(["--user", os.environ["MYSQL_USER"]])
    if os.environ.get("MYSQL_PASSWORD"):
        args.append(f"--password={os.environ['MYSQL_PASSWORD']}")
    return args


def extract_table_names(ddl_text: str) -> list[str]:
    pattern = re.compile(
        r"CREATE\\s+TABLE\\s+(?:IF\\s+NOT\\s+EXISTS\\s+)?(?:`([^`]+)`|([A-Za-z_][A-Za-z0-9_]*))",
        re.IGNORECASE,
    )
    tables: list[str] = []
    for match in pattern.finditer(ddl_text):
        table_name = match.group(1) or match.group(2)
        if table_name and table_name not in tables:
            tables.append(table_name)
    return tables


def spark_read_statements(text: str) -> list[str]:
    return [stmt.strip() for stmt in text.split(";") if stmt.strip()]


def spark_write_df(df: Any, output_path: Path) -> None:
    rows = df.collect()
    with output_path.open("w", encoding="utf-8") as handle:
        for row in rows:
            vals = []
            for value in row:
                vals.append("NULL" if value is None else str(value))
            handle.write("\t".join(vals) + "\n")


def run_postgres_row(paths: dict[str, Path], stdout_log: Path, stderr_log: Path, row_key: str) -> dict[str, Any]:
    source_out = paths["workspace"] / "source.tsv"
    generated_out = paths["workspace"] / "generated.tsv"
    result_check = paths["workspace"] / "result_check.json"
    schema_name = re.sub(r"[^a-z0-9_]", "_", f"ccv0_llm_repair_{row_key}")[:55]
    psql_base = ["psql", "-v", "ON_ERROR_STOP=1", "-X", "-q"]
    with stdout_log.open("w", encoding="utf-8") as stdout_handle, stderr_log.open("w", encoding="utf-8") as stderr_handle:
        try:
            subprocess.run(
                psql_base + ["-c", f"DROP SCHEMA IF EXISTS {schema_name} CASCADE; CREATE SCHEMA {schema_name};"],
                cwd=REPO_ROOT,
                check=True,
                stdout=stdout_handle,
                stderr=stderr_handle,
                text=True,
            )
            for artifact in [paths["schema"], paths["witness"]]:
                subprocess.run(
                    psql_base + ["-c", f"SET search_path TO {schema_name};", "-f", str(artifact)],
                    cwd=REPO_ROOT,
                    check=True,
                    stdout=stdout_handle,
                    stderr=stderr_handle,
                    text=True,
                )
            source_query = normalize_query_text(paths["source"].read_text(encoding="utf-8"))
            repaired_query = normalize_query_text(paths["repaired"].read_text(encoding="utf-8"))
            source_copy_sql = f"COPY ({source_query}) TO STDOUT WITH (FORMAT CSV, DELIMITER E'\\t', NULL 'NULL');"
            repaired_copy_sql = f"COPY ({repaired_query}) TO STDOUT WITH (FORMAT CSV, DELIMITER E'\\t', NULL 'NULL');"
            with source_out.open("w", encoding="utf-8") as handle:
                subprocess.run(
                    psql_base + ["-c", f"SET search_path TO {schema_name};", "-c", source_copy_sql],
                    cwd=REPO_ROOT,
                    check=True,
                    stdout=handle,
                    stderr=stderr_handle,
                    text=True,
                )
            with generated_out.open("w", encoding="utf-8") as handle:
                subprocess.run(
                    psql_base + ["-c", f"SET search_path TO {schema_name};", "-c", repaired_copy_sql],
                    cwd=REPO_ROOT,
                    check=True,
                    stdout=handle,
                    stderr=stderr_handle,
                    text=True,
                )
            compare = compare_tsv_outputs(source_out, generated_out)
            payload = {
                "execution_status_observed": "executed",
                **compare,
                "result_check_path": str(result_check.relative_to(REPO_ROOT)),
            }
            write_json(result_check, payload)
            return payload
        except Exception as exc:
            traceback.print_exc(file=stderr_handle)
            payload = {
                "execution_status_observed": "execution_failed",
                "consistency_check_status": "not_checked_execution_failed",
                "error_type": type(exc).__name__,
                "error_message": str(exc),
                "result_check_path": str(result_check.relative_to(REPO_ROOT)),
            }
            write_json(result_check, payload)
            return payload
        finally:
            subprocess.run(
                ["psql", "-v", "ON_ERROR_STOP=0", "-X", "-q", "-c", f"DROP SCHEMA IF EXISTS {schema_name} CASCADE;"],
                cwd=REPO_ROOT,
                stdout=stdout_handle,
                stderr=stderr_handle,
                text=True,
            )


def run_mysql_row(paths: dict[str, Path], stdout_log: Path, stderr_log: Path) -> dict[str, Any]:
    source_out = paths["workspace"] / "source.tsv"
    generated_out = paths["workspace"] / "generated.tsv"
    result_check = paths["workspace"] / "result_check.json"
    db_name = os.environ.get("MYSQL_DATABASE", "")
    mysql_base = mysql_args()
    if not db_name:
        payload = {
            "execution_status_observed": "execution_failed",
            "consistency_check_status": "not_checked_execution_failed",
            "error_type": "MissingEnvironment",
            "error_message": "MYSQL_DATABASE is not set",
            "result_check_path": str(result_check.relative_to(REPO_ROOT)),
        }
        write_json(result_check, payload)
        return payload
    ddl_text = paths["schema"].read_text(encoding="utf-8")
    table_names = extract_table_names(ddl_text)
    drop_sql = ""
    if table_names:
        drop_sql = "DROP TABLE IF EXISTS " + ", ".join(f"`{name}`" for name in table_names) + ";"
    with stdout_log.open("w", encoding="utf-8") as stdout_handle, stderr_log.open("w", encoding="utf-8") as stderr_handle:
        def mysql_exec(sql: str, output_path: Path | None = None) -> None:
            cmd = mysql_base + [db_name, "--batch", "--raw", "--skip-column-names", "-e", sql]
            if output_path is None:
                subprocess.run(cmd, cwd=REPO_ROOT, check=True, stdout=stdout_handle, stderr=stderr_handle, text=True)
            else:
                with output_path.open("w", encoding="utf-8") as handle:
                    subprocess.run(cmd, cwd=REPO_ROOT, check=True, stdout=handle, stderr=stderr_handle, text=True)
        try:
            if drop_sql:
                mysql_exec(drop_sql)
            mysql_exec(f"source {paths['schema']};")
            mysql_exec(f"source {paths['witness']};")
            mysql_exec(normalize_query_text(paths["source"].read_text(encoding="utf-8")), source_out)
            mysql_exec(normalize_query_text(paths["repaired"].read_text(encoding="utf-8")), generated_out)
            compare = compare_tsv_outputs(source_out, generated_out)
            payload = {
                "execution_status_observed": "executed",
                **compare,
                "result_check_path": str(result_check.relative_to(REPO_ROOT)),
            }
            write_json(result_check, payload)
            return payload
        except Exception as exc:
            traceback.print_exc(file=stderr_handle)
            payload = {
                "execution_status_observed": "execution_failed",
                "consistency_check_status": "not_checked_execution_failed",
                "error_type": type(exc).__name__,
                "error_message": str(exc),
                "result_check_path": str(result_check.relative_to(REPO_ROOT)),
            }
            write_json(result_check, payload)
            return payload
        finally:
            if drop_sql:
                try:
                    mysql_exec(drop_sql)
                except Exception:
                    traceback.print_exc(file=stderr_handle)


def run_spark_row(paths: dict[str, Path], stdout_log: Path, stderr_log: Path, app_name: str) -> dict[str, Any]:
    source_out = paths["workspace"] / "source.tsv"
    generated_out = paths["workspace"] / "generated.tsv"
    result_check = paths["workspace"] / "result_check.json"
    warehouse_dir = paths["workspace"] / "warehouse"
    warehouse_dir.mkdir(parents=True, exist_ok=True)
    with stdout_log.open("w", encoding="utf-8") as stdout_handle, stderr_log.open("w", encoding="utf-8") as stderr_handle:
        spark = None
        try:
            from pyspark.sql import SparkSession

            spark = (
                SparkSession.builder
                .master("local[*]")
                .appName(app_name)
                .config("spark.ui.enabled", "false")
                .config("spark.sql.shuffle.partitions", "1")
                .config("spark.sql.warehouse.dir", str(warehouse_dir))
                .getOrCreate()
            )
            for artifact in [paths["schema"], paths["witness"]]:
                for stmt in spark_read_statements(artifact.read_text(encoding="utf-8")):
                    spark.sql(stmt).collect()
            source_df = spark.sql(normalize_query_text(paths["source"].read_text(encoding="utf-8")))
            repaired_df = spark.sql(normalize_query_text(paths["repaired"].read_text(encoding="utf-8")))
            spark_write_df(source_df, source_out)
            spark_write_df(repaired_df, generated_out)
            compare = compare_tsv_outputs(source_out, generated_out)
            payload = {
                "execution_status_observed": "executed",
                **compare,
                "result_check_path": str(result_check.relative_to(REPO_ROOT)),
            }
            write_json(result_check, payload)
            return payload
        except Exception as exc:
            traceback.print_exc(file=stderr_handle)
            payload = {
                "execution_status_observed": "execution_failed",
                "consistency_check_status": "not_checked_execution_failed",
                "error_type": type(exc).__name__,
                "error_message": str(exc),
                "result_check_path": str(result_check.relative_to(REPO_ROOT)),
            }
            write_json(result_check, payload)
            return payload
        finally:
            if spark is not None:
                try:
                    spark.stop()
                except Exception:
                    traceback.print_exc(file=stderr_handle)


def build_execution_paths(candidate: CandidateRow, repair_sql_path: Path, original_row_key: str) -> dict[str, Path]:
    workspace = WORKSPACES_DIR / candidate.case_id / candidate.engine / ROUTE_ID
    workspace.mkdir(parents=True, exist_ok=True)
    schema_copy = workspace / Path(candidate.schema_artifact).name
    witness_src = original_execution_map()[original_row_key]["witness_data_path"]
    witness_copy = workspace / Path(witness_src).name
    source_copy = workspace / "source.sql"
    repaired_copy = workspace / "repaired.sql"
    shutil.copyfile(REPO_ROOT / candidate.schema_artifact, schema_copy)
    shutil.copyfile(REPO_ROOT / witness_src, witness_copy)
    shutil.copyfile(REPO_ROOT / candidate.source_sql_artifact, source_copy)
    shutil.copyfile(repair_sql_path, repaired_copy)
    return {
        "workspace": workspace,
        "schema": schema_copy,
        "witness": witness_copy,
        "source": source_copy,
        "repaired": repaired_copy,
    }


_ORIGINAL_EXECUTION_MAP: dict[str, dict[str, Any]] | None = None


def original_execution_map() -> dict[str, dict[str, Any]]:
    global _ORIGINAL_EXECUTION_MAP
    if _ORIGINAL_EXECUTION_MAP is None:
        payload = load_json(ORIG_EXEC_RESULTS_JSON)
        _ORIGINAL_EXECUTION_MAP = {
            record["row_key"]: record
            for record in payload["records"]
            if record["row_key"] != "env_check"
        }
    return _ORIGINAL_EXECUTION_MAP


def load_original_generation_map() -> dict[str, dict[str, Any]]:
    payload = load_json(ORIG_GEN_RESULTS_JSON)
    rows = {}
    for row in payload["rows"]:
        row_key = f"{row['case_id'].lower()}__{row['engine']}__{row['route_id']}"
        rows[row_key] = row
    return rows


def load_original_triage_map() -> dict[str, dict[str, str]]:
    rows = {}
    for row in load_csv_rows(ORIG_EXEC_TRIAGE_CSV):
        if row.get("case_id") and row.get("engine"):
            rows[f"{row['case_id'].lower()}__{row['engine']}"] = row
    return rows


def load_original_timing_rows() -> list[dict[str, Any]]:
    rows = []
    for row in load_csv_rows(ORIG_TIMING_CASE_LEVEL_CSV):
        if row["method_id"] == METHOD_ID and row["route_id"] == ORIGINAL_ROUTE_ID:
            rows.append(row)
    return rows


def geometric_mean(values: list[float]) -> float:
    if not values:
        return float("nan")
    return math.exp(sum(math.log(v) for v in values) / len(values))


def summarize_speedups(rows: list[dict[str, Any]]) -> dict[str, Any]:
    speeds = [float(r["speedup_ratio"]) for r in rows if parse_bool(r["timing_success"])]
    if not speeds:
        return {
            "timing_success_rows": 0,
            "median_speedup": "NA_not_computed",
            "gm_speedup": "NA_not_computed",
            "win_count": 0,
            "tie_count": 0,
            "loss_count": 0,
            "regression_20pct_count": 0,
            "regression_rate_20pct": "NA_not_computed",
            "best_case_id": "NA_not_computed",
            "best_case_engine": "NA_not_computed",
            "best_case_speedup": "NA_not_computed",
            "worst_case_id": "NA_not_computed",
            "worst_case_engine": "NA_not_computed",
            "worst_case_speedup": "NA_not_computed",
        }
    win = sum(1 for s in speeds if s > 1.05)
    tie = sum(1 for s in speeds if 0.95 <= s <= 1.05)
    loss = sum(1 for s in speeds if s < 0.95)
    reg20 = sum(1 for s in speeds if s < 0.8)
    best_row = max(rows, key=lambda r: float(r["speedup_ratio"]) if parse_bool(r["timing_success"]) else float("-inf"))
    worst_row = min(rows, key=lambda r: float(r["speedup_ratio"]) if parse_bool(r["timing_success"]) else float("inf"))
    return {
        "timing_success_rows": len(speeds),
        "median_speedup": statistics.median(speeds),
        "gm_speedup": geometric_mean(speeds),
        "win_count": win,
        "tie_count": tie,
        "loss_count": loss,
        "regression_20pct_count": reg20,
        "regression_rate_20pct": reg20 / len(speeds),
        "best_case_id": best_row["case_id"],
        "best_case_engine": best_row["engine"],
        "best_case_speedup": float(best_row["speedup_ratio"]),
        "worst_case_id": worst_row["case_id"],
        "worst_case_engine": worst_row["engine"],
        "worst_case_speedup": float(worst_row["speedup_ratio"]),
    }


def time_postgres_row(paths: dict[str, Path], row_key: str) -> dict[str, Any]:
    schema_name = re.sub(r"[^a-z0-9_]", "_", f"ccv0_llm_repair_timing_{row_key}")[:55]
    psql_base = ["psql", "-v", "ON_ERROR_STOP=1", "-X", "-q"]
    source_query = normalize_query_text(paths["source"].read_text(encoding="utf-8"))
    repaired_query = normalize_query_text(paths["repaired"].read_text(encoding="utf-8"))
    source_copy_sql = f"COPY ({source_query}) TO STDOUT WITH (FORMAT CSV, DELIMITER E'\\t', NULL 'NULL');"
    repaired_copy_sql = f"COPY ({repaired_query}) TO STDOUT WITH (FORMAT CSV, DELIMITER E'\\t', NULL 'NULL');"

    def run_once(sql: str) -> float:
        start = time.perf_counter()
        try:
            subprocess.run(
                psql_base + ["-c", f"DROP SCHEMA IF EXISTS {schema_name} CASCADE; CREATE SCHEMA {schema_name};"],
                cwd=REPO_ROOT,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                text=True,
            )
            for artifact in [paths["schema"], paths["witness"]]:
                subprocess.run(
                    psql_base + ["-c", f"SET search_path TO {schema_name};", "-f", str(artifact)],
                    cwd=REPO_ROOT,
                    check=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    text=True,
                )
            subprocess.run(
                psql_base + ["-c", f"SET search_path TO {schema_name};", "-c", sql],
                cwd=REPO_ROOT,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                text=True,
            )
        finally:
            subprocess.run(
                ["psql", "-v", "ON_ERROR_STOP=0", "-X", "-q", "-c", f"DROP SCHEMA IF EXISTS {schema_name} CASCADE;"],
                cwd=REPO_ROOT,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                text=True,
            )
        return (time.perf_counter() - start) * 1000.0

    for _ in range(WARMUP_COUNT):
        run_once(source_copy_sql)
        run_once(repaired_copy_sql)
    source_runs = [run_once(source_copy_sql) for _ in range(REPEAT_COUNT)]
    repaired_runs = [run_once(repaired_copy_sql) for _ in range(REPEAT_COUNT)]
    median_source = statistics.median(source_runs)
    median_repaired = statistics.median(repaired_runs)
    return {
        "source_runtime_ms": median_source,
        "rewrite_runtime_ms": median_repaired,
        "speedup_ratio": median_source / median_repaired if median_repaired > 0 else None,
        "notes": f"warmup={WARMUP_COUNT}; repeat={REPEAT_COUNT}",
    }


def time_mysql_row(paths: dict[str, Path]) -> dict[str, Any]:
    db_name = os.environ.get("MYSQL_DATABASE", "")
    if not db_name:
        raise RuntimeError("MYSQL_DATABASE is not set")
    mysql_base = mysql_args()
    ddl_text = paths["schema"].read_text(encoding="utf-8")
    table_names = extract_table_names(ddl_text)
    drop_sql = ""
    if table_names:
        drop_sql = "DROP TABLE IF EXISTS " + ", ".join(f"`{name}`" for name in table_names) + ";"

    def mysql_exec(sql: str) -> None:
        cmd = mysql_base + [db_name, "--batch", "--raw", "--skip-column-names", "-e", sql]
        subprocess.run(cmd, cwd=REPO_ROOT, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, text=True)

    source_query = normalize_query_text(paths["source"].read_text(encoding="utf-8"))
    repaired_query = normalize_query_text(paths["repaired"].read_text(encoding="utf-8"))

    def run_once(query: str) -> float:
        start = time.perf_counter()
        try:
            if drop_sql:
                mysql_exec(drop_sql)
            mysql_exec(f"source {paths['schema']};")
            mysql_exec(f"source {paths['witness']};")
            mysql_exec(query)
        finally:
            if drop_sql:
                try:
                    mysql_exec(drop_sql)
                except Exception:
                    pass
        return (time.perf_counter() - start) * 1000.0

    for _ in range(WARMUP_COUNT):
        run_once(source_query)
        run_once(repaired_query)
    source_runs = [run_once(source_query) for _ in range(REPEAT_COUNT)]
    repaired_runs = [run_once(repaired_query) for _ in range(REPEAT_COUNT)]
    median_source = statistics.median(source_runs)
    median_repaired = statistics.median(repaired_runs)
    return {
        "source_runtime_ms": median_source,
        "rewrite_runtime_ms": median_repaired,
        "speedup_ratio": median_source / median_repaired if median_repaired > 0 else None,
        "notes": f"warmup={WARMUP_COUNT}; repeat={REPEAT_COUNT}",
    }


def time_spark_row(paths: dict[str, Path], app_name: str) -> dict[str, Any]:
    from pyspark.sql import SparkSession
    warehouse_dir = paths["workspace"] / "timing_warehouse"
    warehouse_dir.mkdir(parents=True, exist_ok=True)

    def run_once(query_path: Path) -> float:
        spark = None
        try:
            spark = (
                SparkSession.builder
                .master("local[*]")
                .appName(app_name)
                .config("spark.ui.enabled", "false")
                .config("spark.sql.shuffle.partitions", "1")
                .config("spark.sql.warehouse.dir", str(warehouse_dir))
                .getOrCreate()
            )
            for artifact in [paths["schema"], paths["witness"]]:
                for stmt in spark_read_statements(artifact.read_text(encoding="utf-8")):
                    spark.sql(stmt).collect()
            start = time.perf_counter()
            spark.sql(normalize_query_text(query_path.read_text(encoding="utf-8"))).collect()
            return (time.perf_counter() - start) * 1000.0
        finally:
            if spark is not None:
                spark.stop()

    for _ in range(WARMUP_COUNT):
        run_once(paths["source"])
        run_once(paths["repaired"])
    source_runs = [run_once(paths["source"]) for _ in range(REPEAT_COUNT)]
    repaired_runs = [run_once(paths["repaired"]) for _ in range(REPEAT_COUNT)]
    median_source = statistics.median(source_runs)
    median_repaired = statistics.median(repaired_runs)
    return {
        "source_runtime_ms": median_source,
        "rewrite_runtime_ms": median_repaired,
        "speedup_ratio": median_source / median_repaired if median_repaired > 0 else None,
        "notes": f"warmup={WARMUP_COUNT}; repeat={REPEAT_COUNT}",
    }


def build_support_docs() -> None:
    write_text(
        REPAIR_PROMPT_TEMPLATE_MD,
        build_prompt(
            {
                "engine": "{engine}",
                "schema_or_ddl": "{schema_or_ddl}",
                "source_sql": "{source_sql}",
                "first_candidate_sql": "{first_candidate_sql}",
                "observed_failure": "{observed_failure}",
                "checker_or_execution_context": "{checker_or_execution_context}",
            }
        ),
    )
    write_text(
        REPAIR_POLICY_MD,
        "\n".join(
            [
                "# Repair Policy v1",
                "",
                "- Baseline: `Direct LLM + Execute-and-Repair-1`",
                "- Route id: `direct_llm_execute_repair_1shot`",
                "- Denominator: `common_core_v0_40_same_engine_120`",
                "- Repair scope: only the retained `21` `repair_ready` rows",
                "- Blocked rows: retained visible, unrepaired `5` rows",
                "- Model: `gpt-4o-mini`",
                "- Provider/runtime family: `api.gptsapi.net` / OpenAI-compatible API",
                "- Temperature: `0`",
                "- Top-p: `1`",
                "- Max tokens: `2048`",
                "- Candidate count: `1`",
                "- Repair attempts: `1`",
                "- Output acceptance: non-empty, no markdown fences, no prose prefix, SQL-like first line",
                "- Evaluation: execute repaired SQL, run retained exactness check, time only exact rows actually in timing scope",
                "- Boundary: extends Direct LLM; does not replace it; not a final ranked leaderboard",
                "",
            ]
        ),
    )
    write_text(
        README_PATH,
        "\n".join(
            [
                "# Direct LLM + Execute-and-Repair-1",
                "",
                "This run packet contains one repair attempt on the 21 repair-ready rows retained by the preflight manifest.",
                "",
                "- It does not modify the original Direct LLM first-pass run.",
                "- It does not repair the 5 blocked preflight rows.",
                "- It is a separately versioned feedback-aware protocol baseline.",
                "- It is not a final ranked leaderboard.",
                "",
            ]
        ),
    )


def main() -> int:
    build_support_docs()
    env = require_env()
    candidates = load_candidates()
    manifest = load_manifest()
    orig_gen_map = load_original_generation_map()
    orig_exec_map = original_execution_map()
    orig_triage_map = load_original_triage_map()
    orig_timing_rows = load_original_timing_rows()

    ready_ids = [row.repair_row_id for row in manifest.values() if row.ready_for_llm_call]
    blocked_ids = [row.repair_row_id for row in manifest.values() if not row.ready_for_llm_call]

    if len(ready_ids) != EXPECTED_READY_ROWS:
        raise RuntimeError(f"Expected {EXPECTED_READY_ROWS} repair-ready rows, found {len(ready_ids)}")
    if len(blocked_ids) != EXPECTED_BLOCKED_ROWS:
        raise RuntimeError(f"Expected {EXPECTED_BLOCKED_ROWS} blocked rows, found {len(blocked_ids)}")

    client = OpenAI(api_key=env["api_key"], base_url=env["base_url"])
    run_timestamp = utc_now()

    generation_rows: list[dict[str, Any]] = []
    execution_rows: list[dict[str, Any]] = []
    timing_rows: list[dict[str, Any]] = []
    failures_rows: list[dict[str, Any]] = []
    repaired_manifest_rows: list[dict[str, Any]] = []
    repair_exact_count = 0

    for repair_row_id in sorted(ready_ids):
        candidate = candidates[repair_row_id]
        manifest_row = manifest[repair_row_id]
        prompt_payload = load_json(REPO_ROOT / manifest_row.prompt_input_json)
        prompt = build_prompt(prompt_payload)
        prompt_path = PROMPTS_DIR / candidate.case_id / candidate.engine / f"{repair_row_id}.txt"
        raw_response_path = RAW_RESPONSES_DIR / candidate.case_id / candidate.engine / f"{repair_row_id}.txt"
        repaired_sql_path = REPAIRED_SQL_DIR / candidate.case_id / candidate.engine / f"{ROUTE_ID}.sql"
        stdout_log = LOGS_DIR / f"{repair_row_id}.stdout.log"
        stderr_log = LOGS_DIR / f"{repair_row_id}.stderr.log"
        ensure_parent(prompt_path)
        ensure_parent(raw_response_path)
        ensure_parent(repaired_sql_path)
        ensure_parent(stdout_log)
        ensure_parent(stderr_log)
        write_text(prompt_path, prompt)

        raw_text = ""
        api_error = ""
        usage_prompt_tokens = ""
        usage_completion_tokens = ""
        usage_total_tokens = ""
        llm_call_success = False
        output_accepted = False
        extraction_status = "extraction_failed"
        extraction_failure_reason = ""
        call_timestamp = utc_now()
        with stdout_log.open("w", encoding="utf-8") as stdout_handle, stderr_log.open("w", encoding="utf-8") as stderr_handle:
            try:
                response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=TEMPERATURE,
                    top_p=TOP_P,
                    max_tokens=MAX_TOKENS,
                )
                raw_text = extract_response_text(response).strip()
                usage = getattr(response, "usage", None)
                if usage is not None:
                    usage_prompt_tokens = str(getattr(usage, "prompt_tokens", "") or "")
                    usage_completion_tokens = str(getattr(usage, "completion_tokens", "") or "")
                    usage_total_tokens = str(getattr(usage, "total_tokens", "") or "")
                llm_call_success = True
                output_accepted, extraction_status, extraction_failure_reason = classify_output(raw_text)
            except Exception as exc:
                api_error = f"{type(exc).__name__}: {exc}"
                traceback.print_exc(file=stderr_handle)
                extraction_failure_reason = "api_error"
            write_text(raw_response_path, raw_text + ("\n" if raw_text else ""))

        if llm_call_success and output_accepted:
            write_text(repaired_sql_path, raw_text.strip() + "\n")
        else:
            repaired_sql_path = Path("NA_not_created")

        generation_rows.append(
            {
                "repair_row_id": repair_row_id,
                "case_id": candidate.case_id,
                "pool": candidate.pool,
                "engine": candidate.engine,
                "denominator_id": DENOMINATOR_ID,
                "route_id": ROUTE_ID,
                "model": MODEL_NAME,
                "provider": provider_from_base_url(env["base_url"]),
                "temperature": TEMPERATURE,
                "top_p": TOP_P,
                "max_tokens": MAX_TOKENS,
                "prompt_input_json": manifest_row.prompt_input_json,
                "prompt_artifact": str(prompt_path.relative_to(REPO_ROOT)),
                "raw_response_artifact": str(raw_response_path.relative_to(REPO_ROOT)),
                "repaired_sql_artifact": str(repaired_sql_path) if repaired_sql_path == Path("NA_not_created") else str(repaired_sql_path.relative_to(REPO_ROOT)),
                "llm_call_attempted": "true",
                "llm_call_success": str(llm_call_success).lower(),
                "output_accepted": str(output_accepted).lower(),
                "extraction_status": extraction_status,
                "extraction_failure_reason": extraction_failure_reason or api_error or "NA_not_applicable",
                "token_prompt": usage_prompt_tokens or "NA_not_found",
                "token_completion": usage_completion_tokens or "NA_not_found",
                "token_total": usage_total_tokens or "NA_not_found",
                "call_timestamp": call_timestamp,
                "notes": candidate.notes,
            }
        )

        execution_result = {
            "repair_row_id": repair_row_id,
            "case_id": candidate.case_id,
            "pool": candidate.pool,
            "engine": candidate.engine,
            "denominator_id": DENOMINATOR_ID,
            "route_id": ROUTE_ID,
            "repaired_sql_artifact": generation_rows[-1]["repaired_sql_artifact"],
            "execution_attempted": "false",
            "execution_success": "false",
            "exact_match": "false",
            "result_check_artifact": "NA_not_created",
            "execution_error_artifact": "NA_not_created",
            "failure_category": "extraction_failed",
            "failure_detail": extraction_failure_reason or api_error or "output_not_accepted",
            "notes": candidate.notes,
        }

        if llm_call_success and output_accepted and repaired_sql_path != Path("NA_not_created"):
            row_key = f"{candidate.case_id.lower()}__{candidate.engine}__{ORIGINAL_ROUTE_ID}"
            exec_paths = build_execution_paths(candidate, repaired_sql_path, row_key)
            stdout_log = LOGS_DIR / f"{repair_row_id}.execution.stdout.log"
            stderr_log = LOGS_DIR / f"{repair_row_id}.execution.stderr.log"
            if candidate.engine == "pg":
                observed = run_postgres_row(exec_paths, stdout_log, stderr_log, f"{candidate.case_id.lower()}_{candidate.engine}_{ROUTE_ID}")
            elif candidate.engine == "mysql":
                observed = run_mysql_row(exec_paths, stdout_log, stderr_log)
            elif candidate.engine == "spark":
                observed = run_spark_row(exec_paths, stdout_log, stderr_log, f"llm_repair_{candidate.case_id.lower()}_{candidate.engine}")
            else:
                observed = {
                    "execution_status_observed": "execution_failed",
                    "consistency_check_status": "not_checked_execution_failed",
                    "error_type": "UnknownEngine",
                    "error_message": candidate.engine,
                    "result_check_path": "NA_not_created",
                }
            exact_match = bool(observed.get("exact_match"))
            execution_result.update(
                {
                    "execution_attempted": "true",
                    "execution_success": str(observed.get("execution_status_observed") == "executed").lower(),
                    "exact_match": str(exact_match).lower(),
                    "result_check_artifact": observed.get("result_check_path", "NA_not_created"),
                    "execution_error_artifact": "NA_not_applicable" if observed.get("execution_status_observed") == "executed" else str(stderr_log.relative_to(REPO_ROOT)),
                    "failure_category": "exact_after_repair" if exact_match else (
                        "result_mismatch" if observed.get("consistency_check_status") == "mismatch" else "execution_failed"
                    ),
                    "failure_detail": observed.get("consistency_check_status", observed.get("error_message", "")) or "NA_not_applicable",
                }
            )
            if exact_match:
                repair_exact_count += 1
                try:
                    timing_payload = None
                    if candidate.engine == "pg":
                        timing_payload = time_postgres_row(exec_paths, f"{candidate.case_id.lower()}_{candidate.engine}_{ROUTE_ID}")
                    elif candidate.engine == "mysql":
                        timing_payload = time_mysql_row(exec_paths)
                    elif candidate.engine == "spark":
                        timing_payload = time_spark_row(exec_paths, f"llm_repair_timing_{candidate.case_id.lower()}_{candidate.engine}")
                    if timing_payload and timing_payload["speedup_ratio"]:
                        timing_rows.append(
                            {
                                "row_id": f"{candidate.case_id.lower()}__{candidate.engine}__{ROUTE_ID}",
                                "case_id": candidate.case_id,
                                "pool": candidate.pool,
                                "engine": candidate.engine,
                                "denominator_id": DENOMINATOR_ID,
                                "method_id": METHOD_ID,
                                "route_id": ROUTE_ID,
                                "timing_scope": "repair_exact_new_rows_timing",
                                "source_sql_artifact": candidate.source_sql_artifact,
                                "final_candidate_sql_artifact": str(repaired_sql_path.relative_to(REPO_ROOT)),
                                "final_exact": "true",
                                "timing_attempted": "true",
                                "timing_success": "true",
                                "source_runtime_ms": timing_payload["source_runtime_ms"],
                                "rewrite_runtime_ms": timing_payload["rewrite_runtime_ms"],
                                "speedup_ratio": timing_payload["speedup_ratio"],
                                "timing_failure_type": "NA_not_applicable",
                                "timing_failure_detail": "NA_not_applicable",
                                "source_artifacts": f"{candidate.source_artifacts}; {manifest_row.prompt_input_json}",
                                "notes": timing_payload["notes"],
                            }
                        )
                except Exception as exc:
                    failures_rows.append(
                        {
                            "repair_row_id": repair_row_id,
                            "case_id": candidate.case_id,
                            "engine": candidate.engine,
                            "failure_stage": "timing",
                            "failure_type": type(exc).__name__,
                            "failure_detail": str(exc),
                            "repaired_sql_artifact": str(repaired_sql_path.relative_to(REPO_ROOT)),
                            "notes": "newly repaired exact row timing failed",
                        }
                    )
        else:
            failures_rows.append(
                {
                    "repair_row_id": repair_row_id,
                    "case_id": candidate.case_id,
                    "engine": candidate.engine,
                    "failure_stage": "generation",
                    "failure_type": extraction_status,
                    "failure_detail": extraction_failure_reason or api_error or "output_not_accepted",
                    "repaired_sql_artifact": generation_rows[-1]["repaired_sql_artifact"],
                    "notes": "repair output not accepted",
                }
            )

        execution_rows.append(execution_result)
        repaired_manifest_rows.append(
            {
                "repair_row_id": repair_row_id,
                "case_id": candidate.case_id,
                "engine": candidate.engine,
                "repaired_sql_artifact": generation_rows[-1]["repaired_sql_artifact"],
                "llm_call_success": generation_rows[-1]["llm_call_success"],
                "output_accepted": generation_rows[-1]["output_accepted"],
                "execution_attempted": execution_result["execution_attempted"],
                "exact_match": execution_result["exact_match"],
                "notes": candidate.notes,
            }
        )
        if execution_result["failure_category"] not in {"exact_after_repair"} and not (
            not llm_call_success and failures_rows and failures_rows[-1]["failure_stage"] == "generation"
        ):
            if execution_result["failure_category"] != "exact_after_repair":
                failures_rows.append(
                    {
                        "repair_row_id": repair_row_id,
                        "case_id": candidate.case_id,
                        "engine": candidate.engine,
                        "failure_stage": "execution",
                        "failure_type": execution_result["failure_category"],
                        "failure_detail": execution_result["failure_detail"],
                        "repaired_sql_artifact": execution_result["repaired_sql_artifact"],
                        "notes": execution_result["notes"],
                    }
                )

    orig_exact_keys = {
        record["row_key"]
        for record in orig_exec_map.values()
        if record.get("execution_status_observed") == "executed" and bool(record.get("exact_match"))
    }
    if len(orig_exact_keys) != EXPECTED_ORIGINAL_EXACT_ROWS:
        raise RuntimeError(f"Expected {EXPECTED_ORIGINAL_EXACT_ROWS} original exact rows, found {len(orig_exact_keys)}")

    candidate_keys = {f"{c.case_id.lower()}__{c.engine}__{ORIGINAL_ROUTE_ID}" for c in candidates.values()}
    final_outcome_rows: list[dict[str, Any]] = []
    for row_key, orig_row in sorted(orig_exec_map.items()):
        candidate = next((c for c in candidates.values() if f"{c.case_id.lower()}__{c.engine}__{ORIGINAL_ROUTE_ID}" == row_key), None)
        if row_key in orig_exact_keys:
            final_outcome_rows.append(
                {
                    "row_id": row_key,
                    "case_id": orig_row["case_id"],
                    "pool": orig_row["pool"],
                    "engine": orig_row["engine"],
                    "denominator_id": DENOMINATOR_ID,
                    "method_id": METHOD_ID,
                    "route_id": ROUTE_ID,
                    "final_row_source": "original_direct_llm_exact",
                    "original_exact": "true",
                    "repair_attempted": "false",
                    "repair_blocked": "false",
                    "repair_generated": "false",
                    "repair_executed": "false",
                    "repair_exact": "false",
                    "final_exact": "true",
                    "final_failure_category": "NA_not_applicable",
                    "final_candidate_sql_artifact": orig_row["generated_sql_path"],
                    "notes": "original exact row preserved",
                }
            )
            continue
        if candidate is None:
            raise RuntimeError(f"Non-exact row missing from candidate frontier: {row_key}")
        if candidate.repair_row_id in ready_ids:
            repair_event = next(r for r in execution_rows if r["repair_row_id"] == candidate.repair_row_id)
            gen_event = next(r for r in generation_rows if r["repair_row_id"] == candidate.repair_row_id)
            final_outcome_rows.append(
                {
                    "row_id": row_key,
                    "case_id": orig_row["case_id"],
                    "pool": orig_row["pool"],
                    "engine": orig_row["engine"],
                    "denominator_id": DENOMINATOR_ID,
                    "method_id": METHOD_ID,
                    "route_id": ROUTE_ID,
                    "final_row_source": "repair_route",
                    "original_exact": "false",
                    "repair_attempted": "true",
                    "repair_blocked": "false",
                    "repair_generated": gen_event["output_accepted"],
                    "repair_executed": repair_event["execution_attempted"],
                    "repair_exact": repair_event["exact_match"],
                    "final_exact": repair_event["exact_match"],
                    "final_failure_category": "NA_not_applicable" if repair_event["exact_match"] == "true" else repair_event["failure_category"],
                    "final_candidate_sql_artifact": gen_event["repaired_sql_artifact"],
                    "notes": candidate.notes,
                }
            )
        else:
            final_outcome_rows.append(
                {
                    "row_id": row_key,
                    "case_id": orig_row["case_id"],
                    "pool": orig_row["pool"],
                    "engine": orig_row["engine"],
                    "denominator_id": DENOMINATOR_ID,
                    "method_id": METHOD_ID,
                    "route_id": ROUTE_ID,
                    "final_row_source": "repair_blocked_preflight_gap",
                    "original_exact": "false",
                    "repair_attempted": "false",
                    "repair_blocked": "true",
                    "repair_generated": "false",
                    "repair_executed": "false",
                    "repair_exact": "false",
                    "final_exact": "false",
                    "final_failure_category": "preflight_blocked_missing_feedback",
                    "final_candidate_sql_artifact": orig_row["generated_sql_path"],
                    "notes": candidate.repair_block_reason,
                }
            )

    if len(final_outcome_rows) != EXPECTED_PLANNED_ROWS:
        raise RuntimeError(f"Expected {EXPECTED_PLANNED_ROWS} final rows, found {len(final_outcome_rows)}")

    merged_timing_rows: list[dict[str, Any]] = []
    for row in orig_timing_rows:
        merged_timing_rows.append(
            {
                "row_id": f"{row['case_id'].lower()}__{row['engine']}__{ROUTE_ID}",
                "case_id": row["case_id"],
                "pool": row["pool"],
                "engine": row["engine"],
                "denominator_id": DENOMINATOR_ID,
                "method_id": METHOD_ID,
                "route_id": ROUTE_ID,
                "timing_scope": "retained_original_direct_llm_timing",
                "source_sql_artifact": "retained_original_direct_llm_timing",
                "final_candidate_sql_artifact": "retained_original_direct_llm_first_pass_candidate",
                "final_exact": "true",
                "timing_attempted": "true",
                "timing_success": row["timing_success"],
                "source_runtime_ms": row["source_runtime_ms"],
                "rewrite_runtime_ms": row["rewrite_runtime_ms"],
                "speedup_ratio": row["speedup_ratio"],
                "timing_failure_type": "NA_not_applicable",
                "timing_failure_detail": "NA_not_applicable",
                "source_artifacts": row["source_artifact"],
                "notes": row["notes"],
            }
        )
    merged_timing_rows.extend(timing_rows)

    final_exact_rows = sum(1 for row in final_outcome_rows if row["final_exact"] == "true")
    expected_merged_timing = EXPECTED_ORIGINAL_EXACT_ROWS + repair_exact_count
    timing_scope = (
        "mixed_source_timing_full_final_exact_rows"
        if len(merged_timing_rows) == expected_merged_timing
        else "mixed_source_timing_partial"
    )
    timing_summary_values = summarize_speedups(merged_timing_rows)
    final_timing_summary_row = {
        "method_id": METHOD_ID,
        "route_id": ROUTE_ID,
        "denominator_id": DENOMINATOR_ID,
        "planned_rows": EXPECTED_PLANNED_ROWS,
        "final_exact_rows": final_exact_rows,
        "timing_scope": timing_scope,
        "timing_attempted_rows": len(merged_timing_rows),
        "timing_success_rows": timing_summary_values["timing_success_rows"],
        "timing_failed_rows": len(merged_timing_rows) - timing_summary_values["timing_success_rows"],
        "median_speedup": timing_summary_values["median_speedup"],
        "gm_speedup": timing_summary_values["gm_speedup"],
        "win_count": timing_summary_values["win_count"],
        "tie_count": timing_summary_values["tie_count"],
        "loss_count": timing_summary_values["loss_count"],
        "regression_20pct_count": timing_summary_values["regression_20pct_count"],
        "regression_rate_20pct": timing_summary_values["regression_rate_20pct"],
        "best_case_id": timing_summary_values["best_case_id"],
        "best_case_engine": timing_summary_values["best_case_engine"],
        "best_case_speedup": timing_summary_values["best_case_speedup"],
        "worst_case_id": timing_summary_values["worst_case_id"],
        "worst_case_engine": timing_summary_values["worst_case_engine"],
        "worst_case_speedup": timing_summary_values["worst_case_speedup"],
        "claim_boundary": "Timing is mixed-source only if the retained 94 original exact timing rows are merged with newly repaired exact-row timing.",
        "notes": "GM speedup and Regression@20 are computed only on timing_success rows.",
    }

    repair_llm_call_success_rows = sum(1 for row in generation_rows if row["llm_call_success"] == "true")
    repair_output_accepted_rows = sum(1 for row in generation_rows if row["output_accepted"] == "true")
    repair_executed_rows = sum(1 for row in execution_rows if row["execution_attempted"] == "true")
    repair_exact_rows = sum(1 for row in execution_rows if row["exact_match"] == "true")
    final_execution_failed_rows = sum(1 for row in execution_rows if row["failure_category"] == "execution_failed")
    final_mismatch_rows = sum(1 for row in execution_rows if row["failure_category"] == "result_mismatch")
    final_extraction_failed_rows = sum(1 for row in execution_rows if row["failure_category"] == "extraction_failed")
    summary_row = {
        "method_id": METHOD_ID,
        "route_id": ROUTE_ID,
        "denominator_id": DENOMINATOR_ID,
        "planned_rows": EXPECTED_PLANNED_ROWS,
        "original_exact_rows": EXPECTED_ORIGINAL_EXACT_ROWS,
        "non_exact_frontier_rows": 26,
        "repair_ready_rows": EXPECTED_READY_ROWS,
        "repair_blocked_rows": EXPECTED_BLOCKED_ROWS,
        "repair_llm_call_success_rows": repair_llm_call_success_rows,
        "repair_output_accepted_rows": repair_output_accepted_rows,
        "repair_executed_rows": repair_executed_rows,
        "repair_exact_rows": repair_exact_rows,
        "exact_gain_over_original": repair_exact_rows,
        "final_exact_rows": EXPECTED_ORIGINAL_EXACT_ROWS + repair_exact_rows,
        "final_exact_rate": (EXPECTED_ORIGINAL_EXACT_ROWS + repair_exact_rows) / EXPECTED_PLANNED_ROWS,
        "final_non_exact_rows": EXPECTED_PLANNED_ROWS - (EXPECTED_ORIGINAL_EXACT_ROWS + repair_exact_rows),
        "final_execution_failed_rows": final_execution_failed_rows,
        "final_mismatch_rows": final_mismatch_rows,
        "final_extraction_failed_rows": final_extraction_failed_rows,
        "final_blocked_rows": EXPECTED_BLOCKED_ROWS,
        "claim_boundary": "Feedback-aware extension of Direct LLM only; not a replacement and not a final ranked leaderboard.",
        "notes": "Blocked rows remain visible and unrepaired.",
    }

    write_csv(
        REPAIR_GENERATION_CSV,
        [
            "repair_row_id","case_id","pool","engine","denominator_id","route_id","model","provider","temperature","top_p","max_tokens",
            "prompt_input_json","prompt_artifact","raw_response_artifact","repaired_sql_artifact","llm_call_attempted","llm_call_success",
            "output_accepted","extraction_status","extraction_failure_reason","token_prompt","token_completion","token_total","call_timestamp","notes"
        ],
        generation_rows,
    )
    write_csv(
        REPAIR_EXECUTION_CSV,
        [
            "repair_row_id","case_id","pool","engine","denominator_id","route_id","repaired_sql_artifact","execution_attempted",
            "execution_success","exact_match","result_check_artifact","execution_error_artifact","failure_category","failure_detail","notes"
        ],
        execution_rows,
    )
    write_csv(
        FINAL_OUTCOME_CSV,
        [
            "row_id","case_id","pool","engine","denominator_id","method_id","route_id","final_row_source","original_exact","repair_attempted",
            "repair_blocked","repair_generated","repair_executed","repair_exact","final_exact","final_failure_category","final_candidate_sql_artifact","notes"
        ],
        final_outcome_rows,
    )
    write_csv(
        REPAIR_TIMING_CSV,
        [
            "row_id","case_id","pool","engine","denominator_id","method_id","route_id","timing_scope","source_sql_artifact","final_candidate_sql_artifact",
            "final_exact","timing_attempted","timing_success","source_runtime_ms","rewrite_runtime_ms","speedup_ratio","timing_failure_type",
            "timing_failure_detail","source_artifacts","notes"
        ],
        timing_rows,
    )
    write_csv(
        FINAL_TIMING_SUMMARY_CSV,
        [
            "method_id","route_id","denominator_id","planned_rows","final_exact_rows","timing_scope","timing_attempted_rows","timing_success_rows",
            "timing_failed_rows","median_speedup","gm_speedup","win_count","tie_count","loss_count","regression_20pct_count","regression_rate_20pct",
            "best_case_id","best_case_engine","best_case_speedup","worst_case_id","worst_case_engine","worst_case_speedup","claim_boundary","notes"
        ],
        [final_timing_summary_row],
    )
    write_csv(
        REPAIR_RESULT_SUMMARY_CSV,
        [
            "method_id","route_id","denominator_id","planned_rows","original_exact_rows","non_exact_frontier_rows","repair_ready_rows","repair_blocked_rows",
            "repair_llm_call_success_rows","repair_output_accepted_rows","repair_executed_rows","repair_exact_rows","exact_gain_over_original","final_exact_rows",
            "final_exact_rate","final_non_exact_rows","final_execution_failed_rows","final_mismatch_rows","final_extraction_failed_rows","final_blocked_rows",
            "claim_boundary","notes"
        ],
        [summary_row],
    )
    write_csv(
        REPAIR_FAILURES_CSV,
        ["repair_row_id","case_id","engine","failure_stage","failure_type","failure_detail","repaired_sql_artifact","notes"],
        failures_rows,
    )
    write_csv(
        REPAIRED_SQL_MANIFEST_CSV,
        ["repair_row_id","case_id","engine","repaired_sql_artifact","llm_call_success","output_accepted","execution_attempted","exact_match","notes"],
        repaired_manifest_rows,
    )

    write_text(
        FINAL_TIMING_SUMMARY_MD,
        "# Final Timing Summary\n\n" + render_markdown_table(
            [
                "method_id","route_id","denominator_id","planned_rows","final_exact_rows","timing_scope","timing_attempted_rows","timing_success_rows",
                "timing_failed_rows","median_speedup","gm_speedup","win_count","tie_count","loss_count","regression_20pct_count","regression_rate_20pct",
                "best_case_id","best_case_engine","best_case_speedup","worst_case_id","worst_case_engine","worst_case_speedup","claim_boundary","notes"
            ],
            [final_timing_summary_row],
        ) + "\nTiming claims depend on the actual timing scope.\n"
    )
    write_text(
        REPAIR_RESULT_SUMMARY_MD,
        "# Repair Result Summary\n\n" + render_markdown_table(
            [
                "method_id","route_id","denominator_id","planned_rows","original_exact_rows","non_exact_frontier_rows","repair_ready_rows","repair_blocked_rows",
                "repair_llm_call_success_rows","repair_output_accepted_rows","repair_executed_rows","repair_exact_rows","exact_gain_over_original","final_exact_rows",
                "final_exact_rate","final_non_exact_rows","final_execution_failed_rows","final_mismatch_rows","final_extraction_failed_rows","final_blocked_rows",
                "claim_boundary","notes"
            ],
            [summary_row],
        ) + "\nThis run is a feedback-aware protocol baseline only.\n"
    )

    result_card_row = {
        "method_id": METHOD_ID,
        "route_id": ROUTE_ID,
        "denominator_id": DENOMINATOR_ID,
        "planned_rows": EXPECTED_PLANNED_ROWS,
        "original_exact_rows": EXPECTED_ORIGINAL_EXACT_ROWS,
        "repair_ready_rows": EXPECTED_READY_ROWS,
        "repair_blocked_rows": EXPECTED_BLOCKED_ROWS,
        "repair_exact_rows": repair_exact_rows,
        "final_exact_rows": EXPECTED_ORIGINAL_EXACT_ROWS + repair_exact_rows,
        "timing_scope": timing_scope,
        "gm_speedup": final_timing_summary_row["gm_speedup"],
        "median_speedup": final_timing_summary_row["median_speedup"],
        "regression_rate_20pct": final_timing_summary_row["regression_rate_20pct"],
        "notes": "Feedback-aware protocol baseline. Extends Direct LLM, does not replace it. Uses gpt-4o-mini, temperature 0, top_p 1, max_tokens 2048. Repairs only the 21 repair-ready rows. The 5 blocked rows remain visible and unrepaired. Not a final ranked leaderboard.",
    }
    write_csv(
        RESULT_CARD_CSV,
        [
            "method_id","route_id","denominator_id","planned_rows","original_exact_rows","repair_ready_rows","repair_blocked_rows","repair_exact_rows",
            "final_exact_rows","timing_scope","gm_speedup","median_speedup","regression_rate_20pct","notes"
        ],
        [result_card_row],
    )
    write_text(
        RESULT_CARD_MD,
        "# Direct LLM + Execute-and-Repair-1 Result Card\n\n"
        + render_markdown_table(
            [
                "method_id","route_id","denominator_id","planned_rows","original_exact_rows","repair_ready_rows","repair_blocked_rows","repair_exact_rows",
                "final_exact_rows","timing_scope","gm_speedup","median_speedup","regression_rate_20pct","notes"
            ],
            [result_card_row],
        )
        + "\n- Direct LLM + Execute-and-Repair-1 is a feedback-aware protocol baseline.\n"
        + "- It extends Direct LLM and does not replace it.\n"
        + "- It uses the same retained model family, `gpt-4o-mini`, with `temperature=0`, `top_p=1`, `max_tokens=2048`.\n"
        + "- It is separately versioned because the prompt task changes.\n"
        + "- Timing claims, if any, depend on the actual `timing_scope`.\n"
    )

    run_results_payload = {
        "run_id": RUN_ROOT.name,
        "run_timestamp": run_timestamp,
        "method_id": METHOD_ID,
        "route_id": ROUTE_ID,
        "denominator_id": DENOMINATOR_ID,
        "model_settings": {
            "provider": provider_from_base_url(env["base_url"]),
            "base_url": sanitize_base_url(env["base_url"]),
            "model": MODEL_NAME,
            "temperature": TEMPERATURE,
            "top_p": TOP_P,
            "max_tokens": MAX_TOKENS,
            "repair_attempts": REPAIR_ATTEMPTS,
        },
        "summary": summary_row,
        "timing_summary": final_timing_summary_row,
    }
    write_json(RUN_RESULTS_JSON, run_results_payload)
    write_json(
        VALIDATION_REPORT_JSON,
        {
            "expected_planned_rows": EXPECTED_PLANNED_ROWS,
            "original_exact_rows": EXPECTED_ORIGINAL_EXACT_ROWS,
            "expected_repair_ready_rows": EXPECTED_READY_ROWS,
            "repair_generation_event_rows": len(generation_rows),
            "repair_execution_event_rows": len(execution_rows),
            "final_outcome_rows": len(final_outcome_rows),
            "repair_blocked_rows": EXPECTED_BLOCKED_ROWS,
            "repair_exact_rows": repair_exact_rows,
            "final_exact_rows": EXPECTED_ORIGINAL_EXACT_ROWS + repair_exact_rows,
            "timing_scope": timing_scope,
            "timing_attempted_rows": len(merged_timing_rows),
            "timing_success_rows": final_timing_summary_row["timing_success_rows"],
            "timing_failed_rows": final_timing_summary_row["timing_failed_rows"],
            "unexpected_repair_rows": 0,
            "blocked_rows_repaired": 0,
            "status": "ok",
            "model": MODEL_NAME,
            "provider": provider_from_base_url(env["base_url"]),
            "temperature": TEMPERATURE,
            "top_p": TOP_P,
            "max_tokens": MAX_TOKENS,
            "run_timestamp": run_timestamp,
        },
    )
    print(
        json.dumps(
            {
                "repair_ready_rows": EXPECTED_READY_ROWS,
                "repair_exact_rows": repair_exact_rows,
                "final_exact_rows": EXPECTED_ORIGINAL_EXACT_ROWS + repair_exact_rows,
                "timing_scope": timing_scope,
                "result_summary_path": str(REPAIR_RESULT_SUMMARY_CSV.relative_to(REPO_ROOT)),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
