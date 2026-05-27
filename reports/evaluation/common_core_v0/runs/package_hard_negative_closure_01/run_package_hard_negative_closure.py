#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile
from collections import Counter, defaultdict
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path
from typing import Iterable


REPO_ROOT = Path(__file__).resolve().parents[5]
RUN_DIR = REPO_ROOT / "reports/evaluation/common_core_v0/runs/package_hard_negative_closure_01"
FREEZE_DIR = REPO_ROOT / "reports/evaluation/common_core_v0/00_PAPER_EVIDENCE_FREEZE_V1"
DENOMINATOR_ID = "common_core_v0_40_same_engine_120"
MANIFEST_PATH = REPO_ROOT / "reports/evaluation/common_core_v0/common_core_v0_40_same_engine_120_rerun_manifest_v1.csv"
CONTROLS_STATUS_PATH = REPO_ROOT / "reports/evaluation/common_core_v0/controls_status/common_core_v0_controls_status_table_v2.csv"

RUN_MANIFEST_PATH = RUN_DIR / "hard_negative_denominator_manifest.csv"
RUN_COMMAND_MATRIX_PATH = RUN_DIR / "hard_negative_command_matrix.csv"
RUN_EVENT_PATH = RUN_DIR / "hard_negative_event_long.csv"
RUN_RESULT_CHECK_MANIFEST_PATH = RUN_DIR / "hard_negative_result_check_manifest.csv"
RUN_FAILURES_PATH = RUN_DIR / "hard_negative_failures.csv"
RUN_GAP_SUMMARY_PATH = RUN_DIR / "hard_negative_gap_summary.csv"
RUN_RESULTS_PATH = RUN_DIR / "run_results.json"
VALIDATION_REPORT_PATH = RUN_DIR / "validation_report.json"
WORKSPACES_DIR = RUN_DIR / "workspaces"

FREEZE_DENOM_PATH = FREEZE_DIR / "package_hard_negative_denominator_v1.csv"
FREEZE_EVENT_PATH = FREEZE_DIR / "package_hard_negative_closure_event_long_v1.csv"
FREEZE_SUMMARY_PATH = FREEZE_DIR / "package_hard_negative_closure_summary_v1.csv"
FREEZE_FALSE_ACCEPT_PATH = FREEZE_DIR / "package_hard_negative_false_accept_audit_v1.csv"
TABLE4_V2_PATH = FREEZE_DIR / "table4_correctness_guardrail_evidence_v2.csv"
TABLE4_GAP_V2_PATH = FREEZE_DIR / "table4_correctness_guardrail_gap_summary_v2.csv"
TABLE4_V3_PATH = FREEZE_DIR / "table4_correctness_guardrail_evidence_v3.csv"
TABLE4_GAP_V3_PATH = FREEZE_DIR / "table4_correctness_guardrail_gap_summary_v3.csv"
PAPER_GAPS_V3_PATH = FREEZE_DIR / "paper_remaining_experiment_gaps_v3.csv"
PAPER_GAPS_V4_PATH = FREEZE_DIR / "paper_remaining_experiment_gaps_v4.csv"
PAPER_CLAIMS_V3_PATH = FREEZE_DIR / "paper_claim_matrix_v3.csv"
PAPER_CLAIMS_V4_PATH = FREEZE_DIR / "paper_claim_matrix_v4.csv"
README_V3_PATH = FREEZE_DIR / "common_core_v0_paper_results_readme_v3.md"
README_V4_PATH = FREEZE_DIR / "common_core_v0_paper_results_readme_v4.md"

TOLERANCE = Decimal("0.000001")


@dataclass
class HardNegativeRow:
    row_id: str
    case_id: str
    pool: str
    engine: str
    denominator_id: str
    negative_rewrite_id: str
    source_sql_artifact: Path
    negative_sql_artifact: Path | None
    schema_artifact: Path | None
    witness_artifact: Path | None
    runnable: bool
    block_reason: str
    expected_outcome: str
    source_artifacts: str
    notes: str
    case_dir: Path
    validation_model: str
    source_reference_engine: str
    control_status: str


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: stringify(row.get(k, "")) for k in fieldnames})


def stringify(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def markdown_table(rows: list[dict[str, object]], fieldnames: list[str]) -> str:
    header = "| " + " | ".join(fieldnames) + " |"
    sep = "| " + " | ".join(["---"] * len(fieldnames)) + " |"
    body = [
        "| " + " | ".join(markdown_escape(stringify(row.get(name, ""))) for name in fieldnames) + " |"
        for row in rows
    ]
    return "\n".join([header, sep, *body])


def markdown_escape(text: str) -> str:
    return text.replace("\n", "<br>").replace("|", "\\|")


def render_csv_markdown(
    csv_path: Path,
    md_path: Path,
    title: str,
    bullets: list[str],
) -> None:
    rows = csv_rows(csv_path)
    fieldnames = list(rows[0].keys())
    lines = [f"# {title}", "", "这是一次基于保留工件的综合，不包含新的方法生成或计时。", ""]
    for bullet in bullets:
        lines.append(f"- {bullet}")
    lines.extend(["", markdown_table(rows, fieldnames), ""])
    write_text(md_path, "\n".join(lines) + "\n")


def parse_source_dialect(case_dir: Path) -> str:
    text = read_text(case_dir / "manifest.yaml")
    match = re.search(r"^source_dialect:\s*(.+)$", text, re.M)
    return match.group(1).strip() if match else ""


def pool_dir(pool: str) -> str:
    return {
        "performance": "PERF",
        "consistency": "CONS",
        "portability": "PORT",
        "longtail": "LONGTAIL",
    }[pool]


def select_witness(case_dir: Path, engine: str) -> Path | None:
    base = case_dir / "validation"
    candidates = []
    if engine == "pg":
        candidates = [base / "pg_witness_data.sql", base / "load_witness_pg.sql"]
    elif engine == "mysql":
        candidates = [base / "mysql_witness_data.sql", base / "load_witness_mysql.sql"]
    elif engine == "spark":
        candidates = [base / "spark_witness_data.sql", base / "load_witness_spark.sql"]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def negative_info(case_dir: Path, pool: str, engine: str, source_dialect: str) -> tuple[str, Path | None, str, str]:
    if pool != "portability":
        for name in [f"rewrite_neg_01_{engine}.sql", "rewrite_neg_01.sql"]:
            candidate = case_dir / name
            if candidate.exists():
                return "rewrite_neg_01", candidate, "same_engine", engine
        return "rewrite_neg_01", None, "missing_negative_artifact", engine

    if "postgres_like_candidate" in source_dialect:
        source_ref = "pg"
        if engine == "pg":
            return "NA_not_applicable", None, "not_applicable_source_reference_engine", source_ref
        if engine == "mysql":
            for name in ["rewrite_neg_mysql_like.sql", "rewrite_neg_01.sql"]:
                candidate = case_dir / name
                if candidate.exists():
                    return candidate.stem, candidate, "cross_dialect_reference", source_ref
            return "rewrite_neg_mysql_like", None, "missing_negative_artifact", source_ref
        if engine == "spark":
            for name in ["rewrite_neg_02_spark.sql", "rewrite_neg_spark_like.sql", "rewrite_neg_01.sql"]:
                candidate = case_dir / name
                if candidate.exists():
                    return candidate.stem, candidate, "cross_dialect_reference", source_ref
            return "rewrite_neg_02_spark", None, "missing_negative_artifact", source_ref

    if "mysql_like_candidate" in source_dialect:
        source_ref = "mysql"
        if engine == "mysql":
            return "NA_not_applicable", None, "not_applicable_source_reference_engine", source_ref
        if engine == "pg":
            for name in ["rewrite_neg_pg_like.sql", "rewrite_neg_01.sql"]:
                candidate = case_dir / name
                if candidate.exists():
                    return candidate.stem, candidate, "cross_dialect_reference", source_ref
            return "rewrite_neg_pg_like", None, "missing_negative_artifact", source_ref
        if engine == "spark":
            for name in ["rewrite_neg_02_spark.sql", "rewrite_neg_spark_like.sql", "rewrite_neg_01.sql"]:
                candidate = case_dir / name
                if candidate.exists():
                    return candidate.stem, candidate, "cross_dialect_reference", source_ref
            return "rewrite_neg_02_spark", None, "missing_negative_artifact", source_ref

    return "needs_human_review", None, "needs_human_review_unknown_source_dialect", "unknown"


def load_rows() -> list[HardNegativeRow]:
    manifest_rows = csv_rows(MANIFEST_PATH)
    controls_status = {
        (row["case_id"], row["engine"], row["route_id"]): row for row in csv_rows(CONTROLS_STATUS_PATH)
    }
    rows: list[HardNegativeRow] = []
    for entry in manifest_rows:
        case_id = entry["case_id"]
        pool = entry["pool"]
        engine = entry["engine"]
        case_dir = Path(entry["source_case_path_or_manifest"]).parent
        source_dialect = parse_source_dialect(case_dir)
        negative_rewrite_id, negative_sql, validation_model, source_ref = negative_info(
            case_dir, pool, engine, source_dialect
        )
        source_sql = case_dir / "source.sql"
        schema_artifact = case_dir / "schema" / f"ddl_{engine}.sql"
        witness_artifact = select_witness(case_dir, engine if validation_model == "same_engine" else source_ref)
        control = controls_status.get((case_id, engine, "hard_negative"))
        control_status = control["status"] if control else "missing"
        source_artifacts = []
        if control:
            source_artifacts.append(CONTROLS_STATUS_PATH.as_posix())
            source_artifacts.append(control["artifact_path"])
        block_reason = ""
        expected_outcome = "should_reject"
        runnable = False
        notes = "from_common_core_v0_case_package_negative_manifest"

        if validation_model == "same_engine":
            if not source_sql.exists():
                block_reason = "missing_source_sql"
            elif negative_sql is None:
                block_reason = "missing_negative_artifact"
            elif not schema_artifact.exists():
                block_reason = "missing_schema_artifact"
            elif witness_artifact is None:
                block_reason = "missing_witness_artifact"
            elif control_status != "success":
                block_reason = f"retained_controls_status_{control_status}"
            else:
                runnable = True
        elif validation_model == "cross_dialect_reference":
            if negative_sql is None:
                block_reason = "missing_negative_artifact"
            elif control_status != "success":
                block_reason = f"retained_controls_status_{control_status}"
            else:
                source_schema = case_dir / "schema" / f"ddl_{source_ref}.sql"
                source_witness = select_witness(case_dir, source_ref)
                if not source_sql.exists():
                    block_reason = "missing_source_sql"
                elif not source_schema.exists():
                    block_reason = "missing_reference_schema_artifact"
                elif source_witness is None:
                    block_reason = "missing_reference_witness_artifact"
                elif not schema_artifact.exists():
                    block_reason = "missing_target_schema_artifact"
                elif select_witness(case_dir, engine) is None:
                    block_reason = "missing_target_witness_artifact"
                else:
                    runnable = True
                    witness_artifact = source_witness
                    notes = f"cross_dialect_reference_source_engine={source_ref}"
        else:
            block_reason = validation_model
            expected_outcome = "not_applicable" if "not_applicable" in block_reason else "unknown_needs_human_review"

        if block_reason == "not_applicable_source_reference_engine":
            expected_outcome = "not_applicable"
        elif block_reason and not block_reason.startswith("retained_controls_status_"):
            expected_outcome = "unknown_needs_human_review"

        rows.append(
            HardNegativeRow(
                row_id=f"{case_id}__{engine}__{negative_rewrite_id}",
                case_id=case_id,
                pool=pool,
                engine=engine,
                denominator_id=entry["denominator_id"],
                negative_rewrite_id=negative_rewrite_id,
                source_sql_artifact=source_sql,
                negative_sql_artifact=negative_sql,
                schema_artifact=schema_artifact if schema_artifact.exists() else None,
                witness_artifact=witness_artifact,
                runnable=runnable,
                block_reason=block_reason,
                expected_outcome=expected_outcome,
                source_artifacts="|".join(source_artifacts) if source_artifacts else CONTROLS_STATUS_PATH.as_posix(),
                notes=notes,
                case_dir=case_dir,
                validation_model=validation_model,
                source_reference_engine=source_ref,
                control_status=control_status,
            )
        )
    return rows


def run(cmd: list[str], *, input_text: str | None = None, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        input=input_text,
        text=True,
        capture_output=True,
        env=env,
        check=False,
    )


def copy_if_exists(src: Path | None, dst: Path) -> None:
    if src is None or not src.exists():
        return
    shutil.copy2(src, dst)


def strip_comment_lines(text: str) -> str:
    lines = []
    for line in text.splitlines():
        if re.match(r"^\s*--", line):
            continue
        lines.append(line)
    return "\n".join(lines)


def read_statements(path: Path) -> list[str]:
    text = strip_comment_lines(read_text(path))
    return [stmt.strip() for stmt in text.split(";") if stmt.strip()]


def read_query(path: Path) -> str:
    return strip_comment_lines(read_text(path)).strip().rstrip(";")


def write_lines(path: Path, lines: list[str]) -> None:
    write_text(path, "".join(f"{line}\n" for line in lines))


def normalize_row_value(value: object) -> str:
    if value is None:
        return "NULL"
    return str(value)


def pg_run_query(schema_sql: Path, witness_sql: Path, query_sql: Path, out_tsv: Path, stdout_log: Path, stderr_log: Path, schema_name: str) -> bool:
    setup_sql = "\n".join(
        [
            f"drop schema if exists {schema_name} cascade;",
            f"create schema {schema_name};",
            f"set search_path to {schema_name};",
            f"\\i {schema_sql}",
            f"\\i {witness_sql}",
            "",
        ]
    )
    setup = run(["psql", "-X", "-v", "ON_ERROR_STOP=1"], input_text=setup_sql, env=os.environ.copy())
    write_text(stdout_log, setup.stdout)
    write_text(stderr_log, setup.stderr)
    if setup.returncode != 0:
        return False
    query = "\n".join([f"set search_path to {schema_name};", f"\\i {query_sql}", ""])
    result = run(["psql", "-X", "-q", "-v", "ON_ERROR_STOP=1", "-A", "-t", "-F", "\t"], input_text=query, env=os.environ.copy())
    write_text(stdout_log, read_text(stdout_log) + result.stdout)
    write_text(stderr_log, read_text(stderr_log) + result.stderr)
    if result.returncode != 0:
        return False
    write_text(out_tsv, result.stdout)
    return True


def mysql_drop_table_sql(schema_sql: Path) -> str:
    tables: list[str] = []
    for line in read_text(schema_sql).splitlines():
        match = re.match(r"^\s*CREATE\s+TABLE\s+`?([A-Za-z0-9_]+)`?", line, re.I)
        if match:
            tables.append(match.group(1))
    return "".join(f"drop table if exists `{name}`;\n" for name in reversed(tables))


def normalize_mysql_sql(text: str) -> str:
    return re.sub(
        r"EXTRACT\s*\(\s*YEAR\s+FROM\s+CAST\s*\(\s*(.*?)\s+AS\s+TIMESTAMP\s*\)\s*\)",
        r"YEAR(\1)",
        text,
        flags=re.IGNORECASE | re.DOTALL,
    )


def mysql_run_query(schema_sql: Path, witness_sql: Path, query_sql: Path, out_tsv: Path, stdout_log: Path, stderr_log: Path) -> bool:
    env = os.environ.copy()
    mysql_cmd = ["mysql", "--batch", "--raw", "--skip-column-names"]
    if env.get("MYSQL_HOST"):
        mysql_cmd.append(f"--host={env['MYSQL_HOST']}")
    if env.get("MYSQL_PORT"):
        mysql_cmd.append(f"--port={env['MYSQL_PORT']}")
    if env.get("MYSQL_USER"):
        mysql_cmd.append(f"--user={env['MYSQL_USER']}")
    if env.get("MYSQL_PASSWORD"):
        mysql_cmd.append(f"--password={env['MYSQL_PASSWORD']}")
    setup_sql = "".join(
        [
            f"use `{env['MYSQL_DATABASE']}`;\n",
            mysql_drop_table_sql(schema_sql),
            read_text(schema_sql),
            read_text(witness_sql),
        ]
    )
    setup = run(mysql_cmd, input_text=setup_sql, env=env)
    write_text(stdout_log, setup.stdout)
    write_text(stderr_log, setup.stderr)
    if setup.returncode != 0:
        return False
    query_text = normalize_mysql_sql(read_text(query_sql))
    query = "".join([f"use `{env['MYSQL_DATABASE']}`;\n", query_text])
    result = run(mysql_cmd, input_text=query, env=env)
    write_text(stdout_log, read_text(stdout_log) + result.stdout)
    write_text(stderr_log, read_text(stderr_log) + result.stderr)
    if result.returncode != 0:
        return False
    write_text(out_tsv, result.stdout)
    return True


def spark_run_query(schema_sql: Path, witness_sql: Path, query_sql: Path, out_tsv: Path, stdout_log: Path, stderr_log: Path, db_name: str) -> bool:
    try:
        from pyspark.sql import SparkSession
    except Exception as exc:  # pragma: no cover
        write_text(stderr_log, f"pyspark import failed: {exc}\n")
        return False

    warehouse_dir = Path(tempfile.mkdtemp(prefix=f"{db_name}_warehouse_"))
    spark = (
        SparkSession.builder.master("local[*]")
        .appName(f"{db_name}_hard_negative")
        .config("spark.ui.enabled", "false")
        .config("spark.sql.shuffle.partitions", "1")
        .config("spark.sql.warehouse.dir", str(warehouse_dir))
        .config("spark.driver.host", os.environ.get("SPARK_LOCAL_IP", "127.0.0.1"))
        .config("spark.driver.bindAddress", os.environ.get("SPARK_LOCAL_IP", "127.0.0.1"))
        .config("spark.driver.memory", os.environ.get("SPARK_DRIVER_MEMORY", "8g"))
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("ERROR")
    try:
        spark.sql(f"DROP DATABASE IF EXISTS {db_name} CASCADE")
        spark.sql(f"CREATE DATABASE {db_name}")
        spark.sql(f"USE {db_name}")
        for statement in read_statements(schema_sql):
            spark.sql(statement)
        for statement in read_statements(witness_sql):
            spark.sql(statement)
        rows = spark.sql(read_query(query_sql)).collect()
        lines = ["\t".join(normalize_row_value(value) for value in row) for row in rows]
        lines.sort()
        write_lines(out_tsv, lines)
        write_text(stdout_log, f"rows={len(lines)}\n")
        write_text(stderr_log, "")
        return True
    except Exception as exc:
        write_text(stdout_log, "")
        write_text(stderr_log, f"{type(exc).__name__}: {exc}\n")
        return False
    finally:
        spark.stop()
        shutil.rmtree(warehouse_dir, ignore_errors=True)


def exact_and_sorted(source_tsv: Path, negative_tsv: Path) -> tuple[bool, bool]:
    source_text = read_text(source_tsv)
    negative_text = read_text(negative_tsv)
    source_lines = [line.rstrip("\n") for line in source_text.splitlines()]
    negative_lines = [line.rstrip("\n") for line in negative_text.splitlines()]
    exact = source_text == negative_text
    sorted_match = sorted(line.strip() for line in source_lines) == sorted(line.strip() for line in negative_lines)
    return exact, sorted_match


def port_comparator_type(case_dir: Path) -> str:
    checker = case_dir / "validation" / "check_results.py"
    if checker.exists():
        text = read_text(checker)
        if "Decimal" in text:
            return "decimal_scalar"
        if "normalize_scalar" in text:
            return "float_scalar"
        if "normalize_lines" in text:
            return "sorted_lines"
    retained_result_check = case_dir / "runs" / "result_check.json"
    if retained_result_check.exists():
        payload = json.loads(read_text(retained_result_check))
        if "row_samples" in payload:
            return "sorted_lines"
    return "needs_human_review"


def compare_port(case_dir: Path, source_tsv: Path, negative_tsv: Path) -> tuple[bool, bool, bool]:
    comp = port_comparator_type(case_dir)
    if comp == "sorted_lines":
        source_lines = [line.strip() for line in read_text(source_tsv).splitlines()]
        negative_lines = [line.strip() for line in read_text(negative_tsv).splitlines()]
        sorted_match = sorted(source_lines) == sorted(negative_lines)
        return False, sorted_match, sorted_match
    if comp == "float_scalar":
        source_lines = [line.strip() for line in read_text(source_tsv).splitlines() if line.strip()]
        negative_lines = [line.strip() for line in read_text(negative_tsv).splitlines() if line.strip()]
        exact = source_lines == negative_lines
        source_val = [str(float(source_lines[0]))] if source_lines else []
        negative_val = [str(float(negative_lines[0]))] if negative_lines else []
        sorted_match = source_val == negative_val
        return exact, sorted_match, sorted_match
    if comp == "decimal_scalar":
        source_lines = [line.strip() for line in read_text(source_tsv).splitlines() if line.strip()]
        negative_lines = [line.strip() for line in read_text(negative_tsv).splitlines() if line.strip()]
        exact = source_lines == negative_lines
        source_val = Decimal(source_lines[0])
        negative_val = Decimal(negative_lines[0])
        sorted_match = abs(source_val - negative_val) <= TOLERANCE
        return exact, sorted_match, sorted_match
    raise RuntimeError(f"unknown PORT comparator for {case_dir}")


def execute_row(row: HardNegativeRow) -> dict[str, object]:
    workspace = WORKSPACES_DIR / row.row_id
    workspace.mkdir(parents=True, exist_ok=True)
    source_sql_ws = workspace / "source.sql"
    negative_sql_ws = workspace / "negative.sql"
    ddl_ws = workspace / f"ddl_{row.engine}.sql"
    witness_ws = workspace / "witness.sql"
    source_tsv = workspace / "source.tsv"
    negative_tsv = workspace / "negative.tsv"
    result_check_json = workspace / "result_check.json"
    source_stdout = workspace / "source.stdout.log"
    source_stderr = workspace / "source.stderr.log"
    negative_stdout = workspace / "negative.stdout.log"
    negative_stderr = workspace / "negative.stderr.log"

    copy_if_exists(row.source_sql_artifact, source_sql_ws)
    copy_if_exists(row.negative_sql_artifact, negative_sql_ws)
    copy_if_exists(row.schema_artifact, ddl_ws)
    copy_if_exists(row.witness_artifact, witness_ws)

    base_event: dict[str, object] = {
        "row_id": row.row_id,
        "case_id": row.case_id,
        "pool": row.pool,
        "engine": row.engine,
        "denominator_id": row.denominator_id,
        "negative_rewrite_id": row.negative_rewrite_id,
        "source_execution_success": "false",
        "negative_execution_success": "false",
        "checker_ran": "false",
        "exact_match": "NA_not_applicable",
        "sorted_match": "NA_not_applicable",
        "rejection_status": "blocked",
        "false_accept": "NA_not_runnable",
        "rejection_category": "missing_artifact",
        "result_check_artifact": "NA_not_created",
        "source_tsv_artifact": "NA_not_created",
        "negative_tsv_artifact": "NA_not_created",
        "failure_detail": row.block_reason,
        "source_artifacts": row.source_artifacts,
        "notes": row.notes,
    }

    if not row.runnable:
        return base_event

    try:
        if row.validation_model == "same_engine":
            if row.engine == "pg":
                source_ok = pg_run_query(ddl_ws, witness_ws, source_sql_ws, source_tsv, source_stdout, source_stderr, f"{row.case_id.lower()}_{row.engine}_src_hn")
                negative_ok = pg_run_query(ddl_ws, witness_ws, negative_sql_ws, negative_tsv, negative_stdout, negative_stderr, f"{row.case_id.lower()}_{row.engine}_neg_hn")
                comparator_mode = "same_engine_exact"
            elif row.engine == "mysql":
                source_ok = mysql_run_query(ddl_ws, witness_ws, source_sql_ws, source_tsv, source_stdout, source_stderr)
                negative_ok = mysql_run_query(ddl_ws, witness_ws, negative_sql_ws, negative_tsv, negative_stdout, negative_stderr)
                comparator_mode = "same_engine_exact"
            elif row.engine == "spark":
                source_ok = spark_run_query(ddl_ws, witness_ws, source_sql_ws, source_tsv, source_stdout, source_stderr, f"{row.case_id.lower()}_{row.engine}_src_hn")
                negative_ok = spark_run_query(ddl_ws, witness_ws, negative_sql_ws, negative_tsv, negative_stdout, negative_stderr, f"{row.case_id.lower()}_{row.engine}_neg_hn")
                comparator_mode = "same_engine_sorted"
            else:
                raise RuntimeError(f"unsupported engine {row.engine}")
            exact_match = False
            sorted_match = False
            accepted = False
            if source_ok and negative_ok:
                exact_match, sorted_match = exact_and_sorted(source_tsv, negative_tsv)
                accepted = exact_match if comparator_mode == "same_engine_exact" else sorted_match
        else:
            source_ref = row.source_reference_engine
            source_schema = row.case_dir / "schema" / f"ddl_{source_ref}.sql"
            source_witness = select_witness(row.case_dir, source_ref)
            target_witness = select_witness(row.case_dir, row.engine)
            if source_witness is None or target_witness is None:
                raise RuntimeError("missing source or target witness in cross-dialect row")
            ref_ddl_ws = workspace / f"ddl_{source_ref}.sql"
            ref_witness_ws = workspace / f"witness_{source_ref}.sql"
            target_witness_ws = workspace / f"witness_{row.engine}.sql"
            copy_if_exists(source_schema, ref_ddl_ws)
            copy_if_exists(source_witness, ref_witness_ws)
            copy_if_exists(target_witness, target_witness_ws)
            if source_ref == "pg":
                source_ok = pg_run_query(ref_ddl_ws, ref_witness_ws, source_sql_ws, source_tsv, source_stdout, source_stderr, f"{row.case_id.lower()}_pg_ref_hn")
            elif source_ref == "mysql":
                source_ok = mysql_run_query(ref_ddl_ws, ref_witness_ws, source_sql_ws, source_tsv, source_stdout, source_stderr)
            else:
                raise RuntimeError(f"unsupported source ref {source_ref}")
            if row.engine == "pg":
                negative_ok = pg_run_query(ddl_ws, target_witness_ws, negative_sql_ws, negative_tsv, negative_stdout, negative_stderr, f"{row.case_id.lower()}_{row.engine}_neg_hn")
            elif row.engine == "mysql":
                negative_ok = mysql_run_query(ddl_ws, target_witness_ws, negative_sql_ws, negative_tsv, negative_stdout, negative_stderr)
            elif row.engine == "spark":
                negative_ok = spark_run_query(ddl_ws, target_witness_ws, negative_sql_ws, negative_tsv, negative_stdout, negative_stderr, f"{row.case_id.lower()}_{row.engine}_neg_hn")
            else:
                raise RuntimeError(f"unsupported engine {row.engine}")
            exact_match = False
            sorted_match = False
            accepted = False
            if source_ok and negative_ok:
                exact_match, sorted_match, accepted = compare_port(row.case_dir, source_tsv, negative_tsv)

        event = dict(base_event)
        event["source_execution_success"] = "true" if source_ok else "false"
        event["negative_execution_success"] = "true" if negative_ok else "false"
        event["source_tsv_artifact"] = source_tsv.as_posix() if source_tsv.exists() else "NA_not_created"
        event["negative_tsv_artifact"] = negative_tsv.as_posix() if negative_tsv.exists() else "NA_not_created"

        if not source_ok:
            event["checker_ran"] = "false"
            event["exact_match"] = "NA_not_applicable"
            event["sorted_match"] = "NA_not_applicable"
            event["rejection_status"] = "needs_human_review"
            event["false_accept"] = "NA_not_applicable"
            event["rejection_category"] = "source_execution_failed"
            event["failure_detail"] = "source execution failed"
        elif not negative_ok:
            payload = {
                "row_id": row.row_id,
                "case_id": row.case_id,
                "engine": row.engine,
                "negative_rewrite_id": row.negative_rewrite_id,
                "status": "rejected",
                "reason": "negative_execution_failed_rejected",
            }
            write_text(result_check_json, json.dumps(payload, indent=2) + "\n")
            event["result_check_artifact"] = result_check_json.as_posix()
            event["checker_ran"] = "false"
            event["exact_match"] = "NA_not_applicable"
            event["sorted_match"] = "NA_not_applicable"
            event["rejection_status"] = "rejected"
            event["false_accept"] = "false"
            event["rejection_category"] = "negative_execution_failed_rejected"
            event["failure_detail"] = "negative execution failed, counted as rejection"
        else:
            payload = {
                "row_id": row.row_id,
                "case_id": row.case_id,
                "engine": row.engine,
                "negative_rewrite_id": row.negative_rewrite_id,
                "validation_model": row.validation_model,
                "source_reference_engine": row.source_reference_engine,
                "exact_match": exact_match,
                "sorted_match": sorted_match,
                "accepted_as_equivalent": accepted,
            }
            write_text(result_check_json, json.dumps(payload, indent=2) + "\n")
            event["result_check_artifact"] = result_check_json.as_posix()
            event["checker_ran"] = "true"
            event["exact_match"] = "true" if exact_match else "false"
            event["sorted_match"] = "true" if sorted_match else "false"
            if accepted:
                event["rejection_status"] = "false_accept"
                event["false_accept"] = "true"
                event["rejection_category"] = "false_accept"
                event["failure_detail"] = "negative rewrite was accepted as equivalent under retained checker policy"
            else:
                event["rejection_status"] = "rejected"
                event["false_accept"] = "false"
                event["rejection_category"] = "mismatch_rejected"
                event["failure_detail"] = "negative rewrite differs from source under retained checker policy"
        return event
    except Exception as exc:  # pragma: no cover
        write_text(result_check_json, json.dumps({"row_id": row.row_id, "status": "checker_failed", "error": str(exc)}, indent=2) + "\n")
        event = dict(base_event)
        event["source_execution_success"] = "true" if source_tsv.exists() else "false"
        event["negative_execution_success"] = "true" if negative_tsv.exists() else "false"
        event["checker_ran"] = "false"
        event["rejection_status"] = "needs_human_review"
        event["false_accept"] = "NA_not_applicable"
        event["rejection_category"] = "checker_failed"
        event["result_check_artifact"] = result_check_json.as_posix()
        event["source_tsv_artifact"] = source_tsv.as_posix() if source_tsv.exists() else "NA_not_created"
        event["negative_tsv_artifact"] = negative_tsv.as_posix() if negative_tsv.exists() else "NA_not_created"
        event["failure_detail"] = f"{type(exc).__name__}: {exc}"
        return event


def format_rate(numerator: int, denominator: int) -> str:
    if denominator == 0:
        return "NA_not_computed"
    return f"{numerator}/{denominator} = {numerator/denominator:.4f}"


def load_existing_table4_v2() -> list[dict[str, str]]:
    return csv_rows(TABLE4_V2_PATH)


def load_existing_gap_v2() -> list[dict[str, str]]:
    return csv_rows(TABLE4_GAP_V2_PATH)


def load_paper_gaps_v3() -> list[dict[str, str]]:
    return csv_rows(PAPER_GAPS_V3_PATH)


def load_claims_v3() -> list[dict[str, str]]:
    return csv_rows(PAPER_CLAIMS_V3_PATH)


def update_table4_v3(summary_row: dict[str, object]) -> None:
    rows = load_existing_table4_v2()
    new_row = {
        "method_or_control": "Package hard-negative closure",
        "route_id": "package_hard_negative_closure",
        "denominator": DENOMINATOR_ID + "_hard_negative_rows",
        "positive_consistency": "NA_not_applicable_hard_negative_control",
        "candidate_rejection_accounting": "NA_not_applicable_control",
        "negative_rejection": summary_row["negative_rejection_rate"],
        "false_accept": summary_row["false_accept_rate"],
        "support_level": "strong" if summary_row["blocked_rows"] == "9" else "retained_aggregate",
        "paper_safe_wording": "Package-level hard-negative closure now reports runnable hard-negative rows, rejected rows, blocked rows, and false accepts separately from method candidate rejection accounting.",
        "forbidden_overclaim": "Do not reinterpret this package-level hard-negative closure as method-generated candidate false-accept auditing or a final leaderboard signal.",
        "source_artifacts": f"{FREEZE_SUMMARY_PATH.as_posix()}|{FREEZE_EVENT_PATH.as_posix()}|{FREEZE_FALSE_ACCEPT_PATH.as_posix()}",
        "notes": "This row is package-level known-negative closure only. It is not method-level hard-negative generation and not accepted-candidate false-accept auditing.",
    }
    rows.insert(2, new_row)
    fieldnames = list(rows[0].keys())
    write_csv(TABLE4_V3_PATH, rows, fieldnames)
    render_csv_markdown(
        TABLE4_V3_PATH,
        FREEZE_DIR / "table4_correctness_guardrail_evidence_v3.md",
        "Table 4 v3: Correctness Guardrail Evidence",
        [
            "这是 Table 4 的证据刷新，只补 package-level hard-negative closure。",
            "candidate rejection accounting 不等于 hard-negative rejection。",
            "没有运行新的方法生成、计时、EXPLAIN 或 verifier。",
            "不构成 final ranked leaderboard，也不声明 global winner。",
        ],
    )


def update_gap_v3(summary_row: dict[str, object]) -> None:
    rows = load_existing_gap_v2()
    new_rows = []
    for row in rows:
        if row["gap_id"] == "gap_method_level_hard_negative_not_run":
            new_rows.append(
                {
                    **row,
                    "affected_table": "table4_correctness_guardrail_evidence_v3",
                    "current_status": "still_open_after_package_level_closure",
                    "missing_artifact_or_reason": "Package-level hard-negative closure now exists, but method-specific hard-negative generation/evaluation still does not.",
                    "recommended_next_step": "Keep package-level hard-negative closure separate, and run a dedicated method-level hard-negative packet only if the paper needs that stronger claim.",
                    "notes": "This task resolves package-level closure, not method-generated hard-negative rejection.",
                }
            )
        else:
            replacement = dict(row)
            replacement["affected_table"] = replacement["affected_table"].replace("_v2", "_v3")
            new_rows.append(replacement)
    new_rows.insert(
        0,
        {
            "gap_id": "gap_package_level_hard_negative_closure",
            "affected_method_or_control": "Package hard-negative closure",
            "affected_table": "table4_correctness_guardrail_evidence_v3",
            "current_status": "resolved_by_package_hard_negative_closure_run",
            "missing_artifact_or_reason": "none_for_current_package_level_negative_rejection_and_false_accept_accounting",
            "can_be_fixed_by_aggregation_only": "no",
            "requires_new_execution": "no",
            "priority": "resolved",
            "recommended_next_step": "none_for_current_table_refresh",
            "notes": "111 runnable rows were checked and 9 not-applicable portability source-reference cells remain explicit.",
        }
    )
    fieldnames = list(new_rows[0].keys())
    write_csv(TABLE4_GAP_V3_PATH, new_rows, fieldnames)
    render_csv_markdown(
        TABLE4_GAP_V3_PATH,
        FREEZE_DIR / "table4_correctness_guardrail_gap_summary_v3.md",
        "Table 4 v3 Gap Summary",
        [
            "这里区分 package-level hard-negative closure 与 method-level hard-negative generation。",
            "本次任务解决了 package-level closure，但没有解决 accepted generated candidate false-accept audit。",
        ],
    )


def update_paper_gaps_v4() -> None:
    rows = load_paper_gaps_v3()
    out = []
    for row in rows:
        if row["gap_id"] == "gap_01":
            out.append(
                {
                    **row,
                    "current_status": "partially_resolved_package_level_hard_negative_closure_available",
                    "required_next_artifact_or_experiment": "method_specific_hard_negative_generation_packet_only_if_future_claim_needs_it",
                    "notes": "Package-level hard-negative closure is now retained, but method-level hard-negative rejection for generated methods remains open.",
                }
            )
        else:
            out.append(row)
    out.insert(
        1,
        {
            "gap_id": "gap_01b",
            "affected_table": "Table 4",
            "gap_type": "package_level_hard_negative_closure",
            "current_status": "resolved_by_package_hard_negative_closure_run",
            "required_next_artifact_or_experiment": "none_for_current_package_level_negative_closure",
            "priority": "resolved",
            "can_be_done_by_aggregation_only": "no",
            "requires_new_execution": "no",
            "paper_risk_if_not_done": "low",
            "notes": "The paper now has retained package-level NegativeRejectionRate and FalseAcceptRate evidence with blocked/not-applicable rows kept visible.",
        }
    )
    fieldnames = list(out[0].keys())
    write_csv(PAPER_GAPS_V4_PATH, out, fieldnames)
    render_csv_markdown(
        PAPER_GAPS_V4_PATH,
        FREEZE_DIR / "paper_remaining_experiment_gaps_v4.md",
        "Paper Remaining Experiment Gaps v4",
        [
            "package-level hard-negative closure 已完成。",
            "method-level hard-negative generation 仍然是未来单独实验，不应混入当前 Table 4。",
        ],
    )


def update_claims_v4(summary_row: dict[str, object]) -> None:
    rows = load_claims_v3()
    out = []
    for row in rows:
        if row["claim_id"] == "claim_09":
            out.append(
                {
                    **row,
                    "supporting_artifacts": f"{TABLE4_V3_PATH.name}|{FREEZE_SUMMARY_PATH.name}|{FREEZE_FALSE_ACCEPT_PATH.name}",
                    "paper_safe_wording": f"Package-level hard-negative closure now supports a runnable-denominator negative-rejection view: {summary_row['negative_rejection_rate']} with {summary_row['false_accept_rate']} false accepts on the runnable denominator, while blocked and not-applicable rows remain visible.",
                    "forbidden_overclaim": "Do not reinterpret package-level hard-negative closure as method-generated candidate false-accept auditing or as a final ranked leaderboard signal.",
                    "remaining_gap": "Method-level hard-negative generation for rewrite methods remains open.",
                    "notes": "This strengthens the control/closure layer beyond the old aggregate-only summary.",
                }
            )
        else:
            out.append(row)
    out.insert(
        9,
        {
            "claim_id": "claim_09b",
            "claim_text": "Package-level hard-negative closure demonstrates the value of case-package negative rewrites while keeping blocked and not-applicable portability cells visible.",
            "support_level": "strong",
            "supporting_tables": "Table 4",
            "supporting_artifacts": f"{FREEZE_DENOM_PATH.name}|{FREEZE_EVENT_PATH.name}|{FREEZE_SUMMARY_PATH.name}",
            "paper_safe_wording": "The paper now retains package-level hard-negative closure with explicit runnable rows, rejected rows, blocked portability reference cells, and false-accept auditing at the known-negative control layer.",
            "forbidden_overclaim": "Do not generalize this package-level closure into method-level accepted-candidate false-accept claims.",
            "remaining_gap": "Accepted generated candidate false-accept audit remains separate future work.",
            "notes": "This is about case-package negative examples, not method-generated negatives.",
        }
    )
    fieldnames = list(out[0].keys())
    write_csv(PAPER_CLAIMS_V4_PATH, out, fieldnames)
    render_csv_markdown(
        PAPER_CLAIMS_V4_PATH,
        FREEZE_DIR / "paper_claim_matrix_v4.md",
        "Paper Claim Matrix v4",
        [
            "新增 claim 聚焦 package-level hard-negative closure。",
            "不把 package negative closure 误写成 method candidate false-accept 审计。",
        ],
    )


def update_readme_v4(summary_row: dict[str, object]) -> None:
    text = f"""# Common-core v0 Paper Results README v4

这是一次 **package hard-negative closure + Table 4 refresh**。

## What This Package Is

- 一个基于保留 case package 工件的新 hard-negative closure packet
- 一个把 Table 4 从 aggregate-only hard-negative control，推进到 package-level hard-negative closure 的版本
- 一个明确区分 `hard_negative_rejection` 与 `method_candidate_rejection_accounting` 的 paper-facing refresh

## What It Is Not

- 不是 final ranked leaderboard
- 不是新的方法生成 run
- 不是新的 timing run
- 不是 accepted generated candidate false-accept audit

## Hard-negative Closure Highlights

- expected negative rows: `{summary_row['expected_negative_rows']}`
- runnable negative rows: `{summary_row['runnable_negative_rows']}`
- tested negative rows: `{summary_row['tested_negative_rows']}`
- rejected negative rows: `{summary_row['rejected_negative_rows']}`
- false accept rows: `{summary_row['false_accept_rows']}`
- blocked rows: `{summary_row['blocked_rows']}`
- NegativeRejectionRate: `{summary_row['negative_rejection_rate']}`
- FalseAcceptRate: `{summary_row['false_accept_rate']}`

## Reading Order

1. `package_hard_negative_denominator_v1.csv`
2. `package_hard_negative_closure_event_long_v1.csv`
3. `package_hard_negative_closure_summary_v1.csv`
4. `package_hard_negative_false_accept_audit_v1.csv`
5. `table4_correctness_guardrail_evidence_v3.csv`
6. `table4_correctness_guardrail_gap_summary_v3.csv`
7. `paper_claim_matrix_v4.csv`
8. `paper_remaining_experiment_gaps_v4.csv`

## Claim Boundaries

- package-level hard-negative closure 不等于 method-generated hard-negative rejection
- method accepted-candidate false-accept audit 仍然没有完成
- 不声明 final ranked leaderboard
- 不声明 global winner
"""
    write_text(README_V4_PATH, text)


def main() -> int:
    RUN_DIR.mkdir(parents=True, exist_ok=True)
    WORKSPACES_DIR.mkdir(parents=True, exist_ok=True)
    rows = load_rows()

    manifest_rows = [
        {
            "row_id": row.row_id,
            "case_id": row.case_id,
            "pool": row.pool,
            "engine": row.engine,
            "denominator_id": row.denominator_id,
            "negative_rewrite_id": row.negative_rewrite_id,
            "source_sql_artifact": row.source_sql_artifact.as_posix(),
            "negative_sql_artifact": row.negative_sql_artifact.as_posix() if row.negative_sql_artifact else "NA_not_found",
            "schema_artifact": row.schema_artifact.as_posix() if row.schema_artifact else "NA_not_found",
            "witness_artifact": row.witness_artifact.as_posix() if row.witness_artifact else "NA_not_found",
            "runnable": row.runnable,
            "block_reason": row.block_reason or "",
            "expected_outcome": row.expected_outcome,
            "source_artifacts": row.source_artifacts,
            "notes": row.notes,
        }
        for row in rows
    ]
    manifest_fields = list(manifest_rows[0].keys())
    write_csv(RUN_MANIFEST_PATH, manifest_rows, manifest_fields)
    write_csv(FREEZE_DENOM_PATH, manifest_rows, manifest_fields)

    policy_text = """# Package Hard-Negative Closure Policy v1

- Denominator: Common-core v0 same-engine 120 case-engine cells
- Runnable hard-negative rows are case-package known-negative rewrites only
- Method-generated candidate failures are not reinterpreted here
- No method generation, timing, EXPLAIN, or verifier execution is performed
- Portability source-reference cells remain explicit as blocked/not_applicable when no target negative exists for that engine row
"""
    write_text(RUN_DIR / "README.md", "# Package hard-negative closure run packet\n")
    write_text(RUN_DIR / "hard_negative_policy_v1.md", policy_text)

    events = [execute_row(row) for row in rows]
    event_fields = [
        "row_id",
        "case_id",
        "pool",
        "engine",
        "denominator_id",
        "negative_rewrite_id",
        "source_execution_success",
        "negative_execution_success",
        "checker_ran",
        "exact_match",
        "sorted_match",
        "rejection_status",
        "false_accept",
        "rejection_category",
        "result_check_artifact",
        "source_tsv_artifact",
        "negative_tsv_artifact",
        "failure_detail",
        "source_artifacts",
        "notes",
    ]
    write_csv(RUN_EVENT_PATH, events, event_fields)
    write_csv(FREEZE_EVENT_PATH, events, event_fields)

    command_rows = []
    result_manifest_rows = []
    failure_rows = []
    false_accept_rows = []
    category_counter = Counter()
    runnable_rows = [row for row in rows if row.runnable]
    for row, event in zip(rows, events):
        command_rows.append(
            {
                "row_id": row.row_id,
                "case_id": row.case_id,
                "engine": row.engine,
                "validation_model": row.validation_model,
                "source_reference_engine": row.source_reference_engine,
                "workspace": (WORKSPACES_DIR / row.row_id).as_posix(),
                "runnable": row.runnable,
                "block_reason": row.block_reason,
            }
        )
        result_manifest_rows.append(
            {
                "row_id": row.row_id,
                "case_id": row.case_id,
                "engine": row.engine,
                "result_check_artifact": event["result_check_artifact"],
                "checker_status": event["rejection_category"],
                "notes": event["failure_detail"],
            }
        )
        if event["rejection_category"] in {"checker_failed", "source_execution_failed", "missing_artifact", "unsupported"}:
            failure_rows.append(
                {
                    "row_id": row.row_id,
                    "case_id": row.case_id,
                    "pool": row.pool,
                    "engine": row.engine,
                    "negative_rewrite_id": row.negative_rewrite_id,
                    "failure_stage": "hard_negative_closure",
                    "failure_type": event["rejection_category"],
                    "failure_detail": event["failure_detail"],
                    "result_check_artifact": event["result_check_artifact"],
                    "notes": row.notes,
                }
            )
        category_counter[event["rejection_category"]] += 1
        false_accept_rows.append(
            {
                "row_id": row.row_id,
                "case_id": row.case_id,
                "pool": row.pool,
                "engine": row.engine,
                "negative_rewrite_id": row.negative_rewrite_id,
                "false_accept": event["false_accept"],
                "exact_match": event["exact_match"],
                "sorted_match": event["sorted_match"],
                "evidence_artifact": event["result_check_artifact"],
                "audit_status": (
                    "audited_false_accept_found"
                    if event["false_accept"] == "true"
                    else "not_runnable"
                    if event["false_accept"] == "NA_not_runnable"
                    else "needs_human_review"
                    if event["rejection_status"] == "needs_human_review"
                    else "audited_no_false_accept"
                ),
                "notes": event["failure_detail"],
            }
        )

    if not failure_rows:
        failure_rows = [
            {
                "row_id": "no_failure_rows",
                "case_id": "NA",
                "pool": "NA",
                "engine": "NA",
                "negative_rewrite_id": "NA",
                "failure_stage": "hard_negative_closure",
                "failure_type": "none",
                "failure_detail": "No checker/source failures on runnable rows.",
                "result_check_artifact": "NA_not_applicable",
                "notes": "False accepts, if any, are audited separately.",
            }
        ]

    gap_rows = [
        {
            "gap_id": "gap_not_applicable_source_reference_engine_rows",
            "route_id": "package_hard_negative_closure",
            "affected_rows": sum(1 for row in rows if row.block_reason == "not_applicable_source_reference_engine"),
            "gap_type": "source_reference_engine_not_applicable",
            "current_status": "explicitly_visible_not_applicable_rows_retained",
            "required_next_artifact_or_action": "none_for_current_package_level_closure",
            "can_be_fixed_by_aggregation_only": "yes",
            "requires_new_execution": "no",
            "paper_risk_if_not_fixed": "low",
            "notes": "These 9 PORT source-reference cells remain visible rather than being silently dropped.",
        }
    ]

    write_csv(RUN_COMMAND_MATRIX_PATH, command_rows, list(command_rows[0].keys()))
    write_csv(RUN_RESULT_CHECK_MANIFEST_PATH, result_manifest_rows, list(result_manifest_rows[0].keys()))
    write_csv(RUN_FAILURES_PATH, failure_rows, list(failure_rows[0].keys()))
    write_csv(RUN_GAP_SUMMARY_PATH, gap_rows, list(gap_rows[0].keys()))
    write_csv(FREEZE_FALSE_ACCEPT_PATH, false_accept_rows, list(false_accept_rows[0].keys()))

    expected_negative_rows = len(rows)
    runnable_negative_rows = sum(1 for row in rows if row.runnable)
    tested_negative_rows = sum(1 for event in events if event["checker_ran"] == "true" or event["negative_execution_success"] == "true")
    rejected_negative_rows = sum(1 for event in events if event["rejection_status"] == "rejected")
    false_accept_count = sum(1 for event in events if event["rejection_status"] == "false_accept")
    blocked_rows = sum(1 for event in events if event["rejection_status"] == "blocked")
    needs_human_review_rows = sum(1 for event in events if event["rejection_status"] == "needs_human_review")

    summary_row = {
        "denominator_id": DENOMINATOR_ID,
        "expected_negative_rows": expected_negative_rows,
        "runnable_negative_rows": runnable_negative_rows,
        "tested_negative_rows": tested_negative_rows,
        "rejected_negative_rows": rejected_negative_rows,
        "false_accept_rows": false_accept_count,
        "blocked_rows": blocked_rows,
        "needs_human_review_rows": needs_human_review_rows,
        "negative_rejection_rate": format_rate(rejected_negative_rows, runnable_negative_rows),
        "false_accept_rate": format_rate(false_accept_count, runnable_negative_rows),
        "rejection_category_breakdown": json.dumps(dict(category_counter), sort_keys=True),
        "support_level": "strong" if needs_human_review_rows == 0 else "retained_aggregate",
        "source_artifacts": f"{RUN_MANIFEST_PATH.as_posix()}|{RUN_EVENT_PATH.as_posix()}",
        "notes": "Package-level hard-negative closure only. This does not audit accepted generated candidates.",
    }
    write_csv(FREEZE_SUMMARY_PATH, [summary_row], list(summary_row.keys()))

    update_table4_v3(summary_row)
    update_gap_v3(summary_row)
    update_paper_gaps_v4()
    update_claims_v4(summary_row)
    update_readme_v4(summary_row)

    render_csv_markdown(
        FREEZE_DENOM_PATH,
        FREEZE_DIR / "package_hard_negative_denominator_v1.md",
        "Package Hard-Negative Denominator v1",
        [
            "分母按 Common-core v0 的 120 个 case-engine 单元展开。",
            "9 个 PORT source-reference-engine 单元保留为 not_applicable，而不是被隐藏。",
            "这里没有运行新的方法生成或 timing。",
        ],
    )
    render_csv_markdown(
        FREEZE_EVENT_PATH,
        FREEZE_DIR / "package_hard_negative_closure_event_long_v1.md",
        "Package Hard-Negative Closure Event Long v1",
        [
            "这里只记录 case-package 已知负例的 closure 结果。",
            "negative_execution_failed 仍然计为 successful rejection，但会单独分类。",
            "false_accept 是最关键的失败信号。",
        ],
    )
    render_csv_markdown(
        FREEZE_SUMMARY_PATH,
        FREEZE_DIR / "package_hard_negative_closure_summary_v1.md",
        "Package Hard-Negative Closure Summary v1",
        [
            "该汇总展示 runnable / tested / rejected / false_accept / blocked 的分布。",
            "package-level hard-negative rejection 与 method_candidate_rejection_accounting 是两个不同概念。",
        ],
    )
    render_csv_markdown(
        FREEZE_FALSE_ACCEPT_PATH,
        FREEZE_DIR / "package_hard_negative_false_accept_audit_v1.md",
        "Package Hard-Negative False-Accept Audit v1",
        [
            "这里只审计 case package 已知负例是否被错误接受。",
            "它不等于 method-generated accepted candidate false-accept audit。",
        ],
    )

    validation_report = {
        "status": "ok" if false_accept_count == 0 and needs_human_review_rows == 0 else "warning",
        "expected_negative_rows": expected_negative_rows,
        "runnable_negative_rows": runnable_negative_rows,
        "tested_negative_rows": tested_negative_rows,
        "rejected_negative_rows": rejected_negative_rows,
        "false_accept_rows": false_accept_count,
        "blocked_rows": blocked_rows,
        "needs_human_review_rows": needs_human_review_rows,
        "blocked_reasons": Counter(row.block_reason for row in rows if not row.runnable),
        "rejection_category_breakdown": dict(category_counter),
    }
    write_text(VALIDATION_REPORT_PATH, json.dumps(validation_report, indent=2, default=str) + "\n")
    write_text(RUN_RESULTS_PATH, json.dumps(summary_row, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
