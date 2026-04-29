#!/usr/bin/env bash
set -euo pipefail

CASE_ID="PORT_0009"
CASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPO_ROOT="$(cd "${CASE_DIR}/../../.." && pwd)"
RUN_DIR="${CASE_DIR}/runs/spark"
PYTHON_BIN="${PYTHON_BIN:-python}"

# DRAFT-ONLY validation scaffold. Do not treat this as executed evidence.
# Spark runs target rewrites only for this portability case.
# shellcheck disable=SC1091
source "${REPO_ROOT}/scripts/env_spark.sh"

mkdir -p "${RUN_DIR}"

CASE_DIR="${CASE_DIR}" RUN_DIR="${RUN_DIR}" CASE_ID="${CASE_ID}" "${PYTHON_BIN}" - <<'PY2'
import os
import pathlib
import re
from pyspark.sql import SparkSession


def strip_comments(text: str) -> str:
    return "
".join(line for line in text.splitlines() if not re.match(r"^\s*--", line))


def read_statements(path: pathlib.Path):
    text = strip_comments(path.read_text())
    return [stmt.strip() for stmt in text.split(';') if stmt.strip()]


def read_query(path: pathlib.Path) -> str:
    return strip_comments(path.read_text()).strip().rstrip(';')


def write_rows(path: pathlib.Path, rows) -> None:
    lines = ["	".join("NULL" if value is None else str(value) for value in row) for row in rows]
    lines.sort()
    path.write_text("".join(f"{line}
" for line in lines))

case_dir = pathlib.Path(os.environ['CASE_DIR'])
run_dir = pathlib.Path(os.environ['RUN_DIR'])
case_id = os.environ['CASE_ID']

spark = (
    SparkSession.builder.master('local[*]')
    .appName(f"{case_id}_draft_validation")
    .config('spark.ui.enabled', 'false')
    .config('spark.sql.shuffle.partitions', '1')
    .getOrCreate()
)
spark.sparkContext.setLogLevel('ERROR')

try:
    for stmt in read_statements(case_dir / 'schema/ddl_spark.sql'):
        spark.sql(stmt)
    for stmt in read_statements(case_dir / 'validation/spark_witness_data.sql'):
        spark.sql(stmt)

    positive = spark.sql(read_query(case_dir / 'rewrite_pos_01.sql')).collect()
    negative = spark.sql(read_query(case_dir / 'rewrite_neg_01.sql')).collect()

    write_rows(run_dir / 'rewrite_pos_01.tsv', positive)
    write_rows(run_dir / 'rewrite_neg_01.tsv', negative)
finally:
    spark.stop()
PY2
