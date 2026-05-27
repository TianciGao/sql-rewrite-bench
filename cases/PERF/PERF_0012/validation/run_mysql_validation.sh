#!/usr/bin/env bash
set -euo pipefail

CASE_ID="PERF_0012"
SCHEMA="${MYSQL_DATABASE:-bench}"
CASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

MYSQL_BIN="${MYSQL_BIN:-mysql}"
MYSQL_DATABASE="${MYSQL_DATABASE:-bench}"
MYSQL_ARGS=()
if [[ -n "${MYSQL_HOST:-}" ]]; then MYSQL_ARGS+=(--host="$MYSQL_HOST"); fi
if [[ -n "${MYSQL_PORT:-}" ]]; then MYSQL_ARGS+=(--port="$MYSQL_PORT"); fi
if [[ -n "${MYSQL_USER:-}" ]]; then MYSQL_ARGS+=(--user="$MYSQL_USER"); fi
if [[ -n "${MYSQL_PASSWORD:-}" ]]; then MYSQL_ARGS+=(--password="$MYSQL_PASSWORD"); fi
mysql_cmd() {
  "$MYSQL_BIN" "${MYSQL_ARGS[@]}" "$@"
}

RUN_DIR="$CASE_DIR/runs/mysql"
mkdir -p "$RUN_DIR"

cleanup() {
  {
    printf 'use `%s`;\n' "$MYSQL_DATABASE"
  printf 'drop table if exists `region`;\n'
  printf 'drop table if exists `nation`;\n'
  printf 'drop table if exists `partsupp`;\n'
  printf 'drop table if exists `supplier`;\n'
  printf 'drop table if exists `part`;\n'
  } | mysql_cmd --batch --raw --skip-column-names >/dev/null 2>&1 || true
}
trap cleanup EXIT

{
  printf 'use `%s`;\n' "$MYSQL_DATABASE"
  printf 'drop table if exists `region`;\n'
  printf 'drop table if exists `nation`;\n'
  printf 'drop table if exists `partsupp`;\n'
  printf 'drop table if exists `supplier`;\n'
  printf 'drop table if exists `part`;\n'
  cat "$CASE_DIR/schema/ddl_mysql.sql"
  cat "$CASE_DIR/validation/mysql_witness_data.sql"
} | mysql_cmd --batch --raw --skip-column-names >/dev/null

run_query() {
  local sql_file="$1"
  local out_file="$2"
  {
    printf 'use `%s`;\n' "$MYSQL_DATABASE"
    cat "$sql_file"
  } | mysql_cmd --batch --raw --skip-column-names > "$out_file"
}

run_query "$CASE_DIR/source.sql" "$RUN_DIR/source.tsv"
run_query "$CASE_DIR/rewrite_pos_01.sql" "$RUN_DIR/rewrite_pos_01.tsv"
run_query "$CASE_DIR/rewrite_neg_01.sql" "$RUN_DIR/rewrite_neg_01.tsv"

source_positive_equal=false
source_negative_different=false
if cmp -s "$RUN_DIR/source.tsv" "$RUN_DIR/rewrite_pos_01.tsv"; then
  source_positive_equal=true
fi
if ! cmp -s "$RUN_DIR/source.tsv" "$RUN_DIR/rewrite_neg_01.tsv"; then
  source_negative_different=true
fi
ok=false
status="failed"
if $source_positive_equal && $source_negative_different; then
  ok=true
  status="validated"
fi

cat > "$RUN_DIR/result_check.json" <<JSON
{
  "case_id": "$CASE_ID",
  "engine": "mysql",
  "status": "$status",
  "ok": $ok,
  "schema": "$SCHEMA",
  "inputs": {
    "source": "source.sql",
    "positive_rewrite": "rewrite_pos_01.sql",
    "negative_rewrite": "rewrite_neg_01.sql",
    "witness_data": "validation/mysql_witness_data.sql"
  },
  "outputs": {
    "source": "runs/mysql/source.tsv",
    "positive_rewrite": "runs/mysql/rewrite_pos_01.tsv",
    "negative_rewrite": "runs/mysql/rewrite_neg_01.tsv"
  },
  "checks": {
    "source_positive_equal": $source_positive_equal,
    "source_negative_different": $source_negative_different
  },
  "notes": [
    "MySQL-only witness validation.",
    "Validation used the configured MYSQL_DATABASE and transient case-local tables.",
    "No PostgreSQL or Spark validation is implied.",
    "No admission, promotion, or common-core claim is made."
  ]
}
JSON

$ok
