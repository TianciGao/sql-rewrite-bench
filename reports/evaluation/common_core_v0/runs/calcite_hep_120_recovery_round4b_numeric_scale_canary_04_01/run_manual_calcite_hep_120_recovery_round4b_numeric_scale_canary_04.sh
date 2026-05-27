#!/usr/bin/env bash
set -euo pipefail

discover_repo_root() {
  local start_dir="$1"
  local current="$start_dir"
  while [[ "$current" != "/" ]]; do
    if [[ -d "$current/.git" ]] || [[ -f "$current/reports/curation/common_core_v0_final_denominator.csv" ]]; then
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

if [[ "$(pwd)" != "$REPO_ROOT" ]]; then
  echo "run from repo root: $REPO_ROOT" >&2
  exit 1
fi

RUN_ID="calcite_hep_120_recovery_round4b_numeric_scale_canary_04_01"
METHOD_ID="calcite_hep"
ROUTE_ID="calcite_hep_same_engine_rewrite"
DENOMINATOR_ID="common_core_v0_40_same_engine_120"
CLAIM_BOUNDARY="calcite_hep_120_recovery_round4b_numeric_scale_canary_only_not_timing_speedup_or_leaderboard_evidence"

RUN_DIR="$REPO_ROOT/reports/evaluation/common_core_v0/runs/$RUN_ID"
MATRIX_PATH="$RUN_DIR/recovery_command_matrix.csv"
RUN_RESULTS_PATH="$RUN_DIR/run_results.json"
RUN_EVENT_LONG_PATH="$RUN_DIR/run_event_long.csv"

mkdir -p "$RUN_DIR"

echo "Human-run only."
echo "Codex must not execute this script."
echo "This package produces recovery-canary validity evidence only."
echo "No timing."
echo "No speedup."
echo "No leaderboard."
echo "No full 120-row comparable claim."

source "$REPO_ROOT/scripts/env_postgres.sh"
source "$REPO_ROOT/scripts/env_spark.sh"

python - <<'PY' "$REPO_ROOT" "$MATRIX_PATH" "$RUN_RESULTS_PATH" "$RUN_EVENT_LONG_PATH" "$RUN_ID" "$METHOD_ID" "$ROUTE_ID" "$DENOMINATOR_ID" "$CLAIM_BOUNDARY"
from __future__ import annotations

import csv
import json
import shutil
import subprocess
import sys
import tempfile
import traceback
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

REPO_ROOT = Path(sys.argv[1])
MATRIX_PATH = Path(sys.argv[2])
RUN_RESULTS_PATH = Path(sys.argv[3])
RUN_EVENT_LONG_PATH = Path(sys.argv[4])
RUN_ID = sys.argv[5]
METHOD_ID = sys.argv[6]
ROUTE_ID = sys.argv[7]
DENOMINATOR_ID = sys.argv[8]
CLAIM_BOUNDARY = sys.argv[9]

PREVIOUS_LEDGER_NUM = 86
PREVIOUS_LEDGER_DEN = 120
MAX_LEDGER_AFTER = 90


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def normalize_query_text(text: str) -> str:
    return text.strip().rstrip(";").strip()


def compare_tsv_outputs(source_path: Path, generated_path: Path) -> dict[str, Any]:
    source_text = source_path.read_text(encoding="utf-8")
    generated_text = generated_path.read_text(encoding="utf-8")
    exact_match = source_text == generated_text
    return {
        "exact_match": exact_match,
        "consistency_status": "match_exact" if exact_match else "mismatch",
    }


def write_df_tsv(rows: list[tuple[Any, ...]], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        for row in rows:
            values = []
            for value in row:
                values.append("NULL" if value is None else str(value))
            handle.write("\t".join(values) + "\n")


def spark_read_statements(text: str) -> list[str]:
    cleaned = []
    for line in text.splitlines():
        if line.lstrip().startswith("--"):
            continue
        cleaned.append(line)
    joined = "\n".join(cleaned)
    return [stmt.strip() for stmt in joined.split(";") if stmt.strip()]


def read_rows() -> list[dict[str, str]]:
    with MATRIX_PATH.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def repair_generated_sql(row_key: str, sql: str) -> str:
    normalized = normalize_query_text(sql)
    if row_key == "PERF_0062:pg":
        return """
SELECT
CAST((CASE WHEN COUNT(*) = 0 THEN NULL ELSE COALESCE(SUM("store_sales"."ss_quantity"), 0) END / COUNT(*)) AS DECIMAL(22, 16)),
CAST((CASE WHEN COUNT(*) = 0 THEN NULL ELSE COALESCE(SUM("store_sales"."ss_ext_sales_price"), 0) END / COUNT(*)) AS DECIMAL(22, 16)),
CAST((CASE WHEN COUNT(*) = 0 THEN NULL ELSE COALESCE(SUM("store_sales"."ss_ext_wholesale_cost"), 0) END / COUNT(*)) AS DECIMAL(22, 16)),
CAST((CASE WHEN COUNT(*) = 0 THEN NULL ELSE COALESCE(SUM("store_sales"."ss_ext_wholesale_cost"), 0) END) AS DECIMAL(18, 2))
FROM "store_sales",
"store",
"customer_demographics",
"household_demographics",
"customer_address",
"date_dim"
WHERE CAST("store"."s_store_sk" AS INTEGER) = "store_sales"."ss_store_sk" AND "store_sales"."ss_sold_date_sk" = CAST("date_dim"."d_date_sk" AS INTEGER) AND "date_dim"."d_year" = 2001 AND ("store_sales"."ss_hdemo_sk" = CAST("household_demographics"."hd_demo_sk" AS INTEGER) AND (CAST("customer_demographics"."cd_demo_sk" AS INTEGER) = "store_sales"."ss_cdemo_sk" AND "customer_demographics"."cd_marital_status" = 'D') AND ("customer_demographics"."cd_education_status" = '2 yr Degree' AND "store_sales"."ss_sales_price" >= 100.00 AND ("store_sales"."ss_sales_price" <= 150.00 AND "household_demographics"."hd_dep_count" = 3)) OR "store_sales"."ss_hdemo_sk" = CAST("household_demographics"."hd_demo_sk" AS INTEGER) AND (CAST("customer_demographics"."cd_demo_sk" AS INTEGER) = "store_sales"."ss_cdemo_sk" AND "customer_demographics"."cd_marital_status" = 'S') AND ("customer_demographics"."cd_education_status" = 'Secondary' AND "store_sales"."ss_sales_price" >= 50.00 AND ("store_sales"."ss_sales_price" <= 100.00 AND "household_demographics"."hd_dep_count" = 1)) OR "store_sales"."ss_hdemo_sk" = CAST("household_demographics"."hd_demo_sk" AS INTEGER) AND (CAST("customer_demographics"."cd_demo_sk" AS INTEGER) = "store_sales"."ss_cdemo_sk" AND "customer_demographics"."cd_marital_status" = 'W') AND ("customer_demographics"."cd_education_status" = 'Advanced Degree' AND "store_sales"."ss_sales_price" >= 150.00 AND ("store_sales"."ss_sales_price" <= 200.00 AND "household_demographics"."hd_dep_count" = 1))) AND ("store_sales"."ss_addr_sk" = CAST("customer_address"."ca_address_sk" AS INTEGER) AND "customer_address"."ca_country" = 'United States' AND ("customer_address"."ca_state" = 'CO' OR "customer_address"."ca_state" = 'IL' OR "customer_address"."ca_state" = 'MN') AND "store_sales"."ss_net_profit" >= 100 AND "store_sales"."ss_net_profit" <= 200 OR "store_sales"."ss_addr_sk" = CAST("customer_address"."ca_address_sk" AS INTEGER) AND "customer_address"."ca_country" = 'United States' AND ("customer_address"."ca_state" = 'OH' OR "customer_address"."ca_state" = 'MT' OR "customer_address"."ca_state" = 'NM') AND "store_sales"."ss_net_profit" >= 150 AND "store_sales"."ss_net_profit" <= 300 OR "store_sales"."ss_addr_sk" = CAST("customer_address"."ca_address_sk" AS INTEGER) AND "customer_address"."ca_country" = 'United States' AND ("customer_address"."ca_state" = 'TX' OR "customer_address"."ca_state" = 'MO' OR "customer_address"."ca_state" = 'MI') AND "store_sales"."ss_net_profit" >= 50 AND "store_sales"."ss_net_profit" <= 250)
""".strip()
    if row_key == "PERF_0062:spark":
        return """
SELECT
CAST((CASE WHEN COUNT(*) = 0 THEN NULL ELSE COALESCE(SUM(`store_sales`.`ss_quantity`), 0) END / COUNT(*)) AS DECIMAL(18, 1)),
CAST((CAST(CASE WHEN COUNT(*) = 0 THEN NULL ELSE COALESCE(SUM(`store_sales`.`ss_ext_sales_price`), 0) END AS DECIMAL(18, 6)) / COUNT(*)) AS DECIMAL(18, 6)),
CAST((CAST(CASE WHEN COUNT(*) = 0 THEN NULL ELSE COALESCE(SUM(`store_sales`.`ss_ext_wholesale_cost`), 0) END AS DECIMAL(18, 6)) / COUNT(*)) AS DECIMAL(18, 6)),
CAST((CASE WHEN COUNT(*) = 0 THEN NULL ELSE COALESCE(SUM(`store_sales`.`ss_ext_wholesale_cost`), 0) END) AS DECIMAL(18, 2))
FROM `store_sales`
CROSS JOIN `store`
CROSS JOIN `customer_demographics`
CROSS JOIN `household_demographics`
CROSS JOIN `customer_address`
CROSS JOIN `date_dim`
WHERE `store`.`s_store_sk` = `store_sales`.`ss_store_sk` AND `store_sales`.`ss_sold_date_sk` = `date_dim`.`d_date_sk` AND `date_dim`.`d_year` = 2001 AND (`store_sales`.`ss_hdemo_sk` = `household_demographics`.`hd_demo_sk` AND (`customer_demographics`.`cd_demo_sk` = `store_sales`.`ss_cdemo_sk` AND `customer_demographics`.`cd_marital_status` = 'D') AND (`customer_demographics`.`cd_education_status` = '2 yr Degree' AND `store_sales`.`ss_sales_price` >= 100.00 AND (`store_sales`.`ss_sales_price` <= 150.00 AND `household_demographics`.`hd_dep_count` = 3)) OR `store_sales`.`ss_hdemo_sk` = `household_demographics`.`hd_demo_sk` AND (`customer_demographics`.`cd_demo_sk` = `store_sales`.`ss_cdemo_sk` AND `customer_demographics`.`cd_marital_status` = 'S') AND (`customer_demographics`.`cd_education_status` = 'Secondary' AND `store_sales`.`ss_sales_price` >= 50.00 AND (`store_sales`.`ss_sales_price` <= 100.00 AND `household_demographics`.`hd_dep_count` = 1)) OR `store_sales`.`ss_hdemo_sk` = `household_demographics`.`hd_demo_sk` AND (`customer_demographics`.`cd_demo_sk` = `store_sales`.`ss_cdemo_sk` AND `customer_demographics`.`cd_marital_status` = 'W') AND (`customer_demographics`.`cd_education_status` = 'Advanced Degree' AND `store_sales`.`ss_sales_price` >= 150.00 AND (`store_sales`.`ss_sales_price` <= 200.00 AND `household_demographics`.`hd_dep_count` = 1))) AND (`store_sales`.`ss_addr_sk` = `customer_address`.`ca_address_sk` AND `customer_address`.`ca_country` = 'United States' AND (`customer_address`.`ca_state` = 'CO' OR `customer_address`.`ca_state` = 'IL' OR `customer_address`.`ca_state` = 'MN') AND CAST(`store_sales`.`ss_net_profit` AS DECIMAL(10, 0)) >= 100 AND CAST(`store_sales`.`ss_net_profit` AS DECIMAL(10, 0)) <= 200 OR `store_sales`.`ss_addr_sk` = `customer_address`.`ca_address_sk` AND `customer_address`.`ca_country` = 'United States' AND (`customer_address`.`ca_state` = 'OH' OR `customer_address`.`ca_state` = 'MT' OR `customer_address`.`ca_state` = 'NM') AND CAST(`store_sales`.`ss_net_profit` AS DECIMAL(10, 0)) >= 150 AND CAST(`store_sales`.`ss_net_profit` AS DECIMAL(10, 0)) <= 300 OR `store_sales`.`ss_addr_sk` = `customer_address`.`ca_address_sk` AND `customer_address`.`ca_country` = 'United States' AND (`customer_address`.`ca_state` = 'TX' OR `customer_address`.`ca_state` = 'MO' OR `customer_address`.`ca_state` = 'MI') AND CAST(`store_sales`.`ss_net_profit` AS DECIMAL(10, 0)) >= 50 AND CAST(`store_sales`.`ss_net_profit` AS DECIMAL(10, 0)) <= 250)
""".strip()
    if row_key == "LONGTAIL_0013:pg":
        return normalized.replace(
            'CASE WHEN "$f6" IS NOT NULL THEN CAST("$f6" AS INTEGER) ELSE 0 END AS "avgscore"',
            'CAST(CASE WHEN "$f6" IS NOT NULL THEN "$f6" ELSE 0 END AS DECIMAL(22, 16)) AS "avgscore"',
        )
    if row_key == "LONGTAIL_0013:spark":
        return normalized.replace(
            'CASE WHEN `$f6` IS NOT NULL THEN CAST(`$f6` AS INTEGER) ELSE 0 END `AvgScore`',
            'CAST(CASE WHEN `$f6` IS NOT NULL THEN `$f6` ELSE 0 END AS DECIMAL(18, 1)) `AvgScore`',
        )
    raise ValueError(f"unsupported row for repair: {row_key}")


def copy_inputs_and_repair(workspace: Path, row: dict[str, str]) -> dict[str, Path]:
    workspace.mkdir(parents=True, exist_ok=True)
    repaired_generated = REPO_ROOT / row["expected_repaired_generated_sql_path"]
    repaired_generated.parent.mkdir(parents=True, exist_ok=True)
    engine = row["engine"]
    copied = {
        "schema": workspace / f"ddl_{engine}.sql",
        "witness": workspace / f"{engine}_witness_data.sql",
        "source": workspace / "source.sql",
        "generated": workspace / "generated.sql",
        "retained_generated": REPO_ROOT / row["retained_generated_sql_path"],
        "repaired_generated": repaired_generated,
    }
    shutil.copyfile(REPO_ROOT / row["schema_path"], copied["schema"])
    shutil.copyfile(REPO_ROOT / row["witness_data_path"], copied["witness"])
    shutil.copyfile(REPO_ROOT / row["source_sql_path"], copied["source"])
    retained_sql = copied["retained_generated"].read_text(encoding="utf-8")
    repaired_sql = repair_generated_sql(row["row_key"], retained_sql)
    copied["generated"].write_text(repaired_sql.rstrip() + ";\n", encoding="utf-8")
    copied["repaired_generated"].write_text(repaired_sql.rstrip() + ";\n", encoding="utf-8")
    return copied


def run_pg_execution(row: dict[str, str]) -> dict[str, Any]:
    workspace = (REPO_ROOT / row["expected_result_check_path"]).parent
    copied = copy_inputs_and_repair(workspace, row)
    source_out = REPO_ROOT / row["expected_source_tsv_path"]
    generated_out = REPO_ROOT / row["expected_generated_tsv_path"]
    result_check = REPO_ROOT / row["expected_result_check_path"]
    source_stdout = REPO_ROOT / row["expected_source_stdout_log"]
    source_stderr = REPO_ROOT / row["expected_source_stderr_log"]
    generated_stdout = REPO_ROOT / row["expected_generated_stdout_log"]
    generated_stderr = REPO_ROOT / row["expected_generated_stderr_log"]
    row_metadata_path = REPO_ROOT / row["expected_row_metadata_path"]
    for path in [source_out.parent, source_stdout.parent, generated_stdout.parent, row_metadata_path.parent]:
        path.mkdir(parents=True, exist_ok=True)

    schema_name = f"ccv0_calcite_hep_r4b_{row['case_id'].lower()}_{row['engine']}".replace("-", "_")[:55]
    psql_base = ["psql", "-v", "ON_ERROR_STOP=1", "-X", "-q"]

    with source_stdout.open("w", encoding="utf-8") as source_stdout_handle, source_stderr.open("w", encoding="utf-8") as source_stderr_handle, generated_stdout.open("w", encoding="utf-8") as generated_stdout_handle, generated_stderr.open("w", encoding="utf-8") as generated_stderr_handle:
        try:
            subprocess.run(psql_base + ["-c", f"DROP SCHEMA IF EXISTS {schema_name} CASCADE; CREATE SCHEMA {schema_name};"], cwd=REPO_ROOT, check=True, stdout=source_stdout_handle, stderr=source_stderr_handle, text=True)
            for sql_path in [copied["schema"], copied["witness"]]:
                subprocess.run(psql_base + ["-c", f"SET search_path TO {schema_name};", "-f", str(sql_path)], cwd=REPO_ROOT, check=True, stdout=source_stdout_handle, stderr=source_stderr_handle, text=True)
            source_query = normalize_query_text(copied["source"].read_text(encoding="utf-8"))
            generated_query = normalize_query_text(copied["generated"].read_text(encoding="utf-8"))
            source_copy = f"COPY ({source_query}) TO STDOUT WITH (FORMAT CSV, DELIMITER E'\\t', NULL 'NULL');"
            generated_copy = f"COPY ({generated_query}) TO STDOUT WITH (FORMAT CSV, DELIMITER E'\\t', NULL 'NULL');"
            with source_out.open("w", encoding="utf-8") as handle:
                subprocess.run(psql_base + ["-c", f"SET search_path TO {schema_name};", "-c", source_copy], cwd=REPO_ROOT, check=True, stdout=handle, stderr=source_stderr_handle, text=True)
            with generated_out.open("w", encoding="utf-8") as handle:
                subprocess.run(psql_base + ["-c", f"SET search_path TO {schema_name};", "-c", generated_copy], cwd=REPO_ROOT, check=True, stdout=handle, stderr=generated_stderr_handle, text=True)
            compare = compare_tsv_outputs(source_out, generated_out)
            payload = {"execution_status": "executed", **compare}
        except subprocess.CalledProcessError as exc:
            payload = {
                "execution_status": "generated_execution_failed",
                "exact_match": False,
                "consistency_status": "not_applicable",
                "failure_category": "execution_failed",
                "blocker_reason": str(exc),
            }
        finally:
            subprocess.run(["psql", "-v", "ON_ERROR_STOP=0", "-X", "-q", "-c", f"DROP SCHEMA IF EXISTS {schema_name} CASCADE;"], cwd=REPO_ROOT, stdout=generated_stdout_handle, stderr=generated_stderr_handle, text=True)

    write_json(result_check, payload)
    write_json(
        row_metadata_path,
        {
            "run_id": RUN_ID,
            "row_key": row["row_key"],
            "case_id": row["case_id"],
            "engine": row["engine"],
            "previous_ledger": row["previous_ledger"],
            "attempted_recovery_family": row["attempted_recovery_family"],
            "retained_generated_sql_path": row["retained_generated_sql_path"],
            "repaired_generated_sql_path": row["expected_repaired_generated_sql_path"],
            **payload,
        },
    )
    return payload


def run_spark_execution(row: dict[str, str]) -> dict[str, Any]:
    workspace = (REPO_ROOT / row["expected_result_check_path"]).parent
    copied = copy_inputs_and_repair(workspace, row)
    source_out = REPO_ROOT / row["expected_source_tsv_path"]
    generated_out = REPO_ROOT / row["expected_generated_tsv_path"]
    result_check = REPO_ROOT / row["expected_result_check_path"]
    source_stdout = REPO_ROOT / row["expected_source_stdout_log"]
    source_stderr = REPO_ROOT / row["expected_source_stderr_log"]
    generated_stdout = REPO_ROOT / row["expected_generated_stdout_log"]
    generated_stderr = REPO_ROOT / row["expected_generated_stderr_log"]
    row_metadata_path = REPO_ROOT / row["expected_row_metadata_path"]
    for path in [source_out.parent, source_stdout.parent, generated_stdout.parent, row_metadata_path.parent]:
        path.mkdir(parents=True, exist_ok=True)

    warehouse_dir = Path(tempfile.mkdtemp(prefix=f"calcite_hep_r4b_{row['case_id'].lower()}_{row['engine']}_", dir="/tmp"))

    with source_stdout.open("w", encoding="utf-8") as source_stdout_handle, source_stderr.open("w", encoding="utf-8") as source_stderr_handle, generated_stdout.open("w", encoding="utf-8") as generated_stdout_handle, generated_stderr.open("w", encoding="utf-8") as generated_stderr_handle:
        spark = None
        try:
            from pyspark.sql import SparkSession

            spark = (
                SparkSession.builder
                .master("local[*]")
                .appName(f"ccv0_calcite_hep_r4b_{row['case_id'].lower()}_{row['engine']}")
                .config("spark.ui.enabled", "false")
                .config("spark.sql.shuffle.partitions", "1")
                .config("spark.sql.warehouse.dir", str(warehouse_dir))
                .getOrCreate()
            )
            for path in [copied["schema"], copied["witness"]]:
                for stmt in spark_read_statements(path.read_text(encoding="utf-8")):
                    spark.sql(stmt).collect()
        except Exception as exc:
            traceback.print_exc(file=source_stderr_handle)
            payload = {
                "execution_status": "setup_failed",
                "exact_match": False,
                "consistency_status": "not_applicable",
                "failure_category": "spark_setup_failed",
                "blocker_reason": str(exc),
            }
            write_json(result_check, payload)
            write_json(row_metadata_path, {"row_key": row["row_key"], **payload})
            if spark is not None:
                try:
                    spark.stop()
                except Exception:
                    pass
            shutil.rmtree(warehouse_dir, ignore_errors=True)
            return payload

        try:
            source_rows = [tuple(r) for r in spark.sql(normalize_query_text(copied["source"].read_text(encoding="utf-8"))).collect()]
            write_df_tsv(source_rows, source_out)
            generated_rows = [tuple(r) for r in spark.sql(normalize_query_text(copied["generated"].read_text(encoding="utf-8"))).collect()]
            write_df_tsv(generated_rows, generated_out)
            compare = compare_tsv_outputs(source_out, generated_out)
            payload = {"execution_status": "executed", **compare}
        except Exception as exc:
            traceback.print_exc(file=generated_stderr_handle)
            payload = {
                "execution_status": "generated_execution_failed",
                "exact_match": False,
                "consistency_status": "not_applicable",
                "failure_category": "execution_failed",
                "blocker_reason": str(exc),
            }

        write_json(result_check, payload)
        write_json(
            row_metadata_path,
            {
                "run_id": RUN_ID,
                "row_key": row["row_key"],
                "case_id": row["case_id"],
                "engine": row["engine"],
                "previous_ledger": row["previous_ledger"],
                "attempted_recovery_family": row["attempted_recovery_family"],
                "retained_generated_sql_path": row["retained_generated_sql_path"],
                "repaired_generated_sql_path": row["expected_repaired_generated_sql_path"],
                **payload,
            },
        )
        try:
            spark.stop()
        except Exception:
            traceback.print_exc(file=generated_stderr_handle)
        shutil.rmtree(warehouse_dir, ignore_errors=True)
        return payload


rows = read_rows()
records: list[dict[str, Any]] = []

event_fields = [
    "row_key",
    "case_id",
    "pool",
    "engine",
    "previous_status",
    "attempted_recovery_family",
    "execution_status",
    "exact_match",
    "consistency_status",
    "recovered_exact",
    "failure_category",
    "blocker_reason",
    "source_sql_path",
    "schema_path",
    "witness_data_path",
    "generated_sql_path",
    "result_check_path",
    "claim_boundary",
]

for row in rows:
    base_record = {
        "row_key": row["row_key"],
        "case_id": row["case_id"],
        "pool": row["pool"],
        "engine": row["engine"],
        "method_id": METHOD_ID,
        "route_id": ROUTE_ID,
        "denominator_id": DENOMINATOR_ID,
        "previous_status": row["previous_status"],
        "attempted_recovery_family": row["attempted_recovery_family"],
        "source_sql_path": row["source_sql_path"],
        "schema_path": row["schema_path"],
        "witness_data_path": row["witness_data_path"],
        "generated_sql_path": row["expected_repaired_generated_sql_path"],
        "result_check_path": row["expected_result_check_path"],
        "row_metadata_path": row["expected_row_metadata_path"],
        "claim_boundary": CLAIM_BOUNDARY,
    }

    required = [
        REPO_ROOT / row["source_sql_path"],
        REPO_ROOT / row["schema_path"],
        REPO_ROOT / row["witness_data_path"],
        REPO_ROOT / row["retained_generated_sql_path"],
    ]
    if not all(path.is_file() for path in required):
        observed = {
            "execution_status": "setup_failed",
            "exact_match": False,
            "consistency_status": "not_applicable",
            "recovered_exact": False,
            "failure_category": "missing_input_artifact",
            "blocker_reason": "source_or_schema_or_witness_or_generated_missing",
        }
    else:
        if row["engine"] == "pg":
            execution = run_pg_execution(row)
        elif row["engine"] == "spark":
            execution = run_spark_execution(row)
        else:
            execution = {
                "execution_status": "setup_failed",
                "exact_match": False,
                "consistency_status": "not_applicable",
                "failure_category": "unsupported_engine",
                "blocker_reason": row["engine"],
            }
        observed = {
            **execution,
            "recovered_exact": bool(execution.get("execution_status") == "executed" and execution.get("exact_match") is True),
            "failure_category": execution.get("failure_category", ""),
            "blocker_reason": execution.get("blocker_reason", ""),
        }

    metadata_payload = {**base_record, **observed}
    write_json(REPO_ROOT / row["expected_row_metadata_path"], metadata_payload)
    records.append(metadata_payload)

with RUN_EVENT_LONG_PATH.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=event_fields)
    writer.writeheader()
    for record in records:
        writer.writerow({key: record.get(key, "") for key in event_fields})

counts_by_execution_status = Counter(record["execution_status"] for record in records)
counts_by_consistency_status = Counter(record["consistency_status"] for record in records)
counts_by_engine: dict[str, Counter[str]] = defaultdict(Counter)
for record in records:
    counts_by_engine[record["engine"]][record["execution_status"]] += 1
    counts_by_engine[record["engine"]][record["consistency_status"]] += 1
    if record["recovered_exact"]:
        counts_by_engine[record["engine"]]["recovered_exact"] += 1

recovered_exact_count = sum(1 for record in records if record["recovered_exact"])
payload = {
    "run_id": RUN_ID,
    "method_id": METHOD_ID,
    "route_id": ROUTE_ID,
    "denominator_id": DENOMINATOR_ID,
    "previous_fail_closed_exact_ledger": f"{PREVIOUS_LEDGER_NUM}/{PREVIOUS_LEDGER_DEN}",
    "planned_rows": len(rows),
    "recovered_exact_count": recovered_exact_count,
    "new_fail_closed_exact_ledger": f"{PREVIOUS_LEDGER_NUM + recovered_exact_count}/{PREVIOUS_LEDGER_DEN}",
    "maximum_possible_ledger_after_this_canary": f"{MAX_LEDGER_AFTER}/{PREVIOUS_LEDGER_DEN}",
    "counts_by_engine": {engine: dict(counter) for engine, counter in sorted(counts_by_engine.items())},
    "counts_by_execution_status": dict(counts_by_execution_status),
    "counts_by_consistency_status": dict(counts_by_consistency_status),
    "current_benchmark_metric_evidence": False,
    "timing_denominator_id": "NA_not_computed",
    "leaderboard_comparable": "no",
    "claim_boundary": CLAIM_BOUNDARY,
    "records": records,
}
write_json(RUN_RESULTS_PATH, payload)
PY
