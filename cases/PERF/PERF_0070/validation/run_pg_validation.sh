#!/usr/bin/env bash
set -euo pipefail

case_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
case_id="$(basename "${case_dir}")"
run_dir="${case_dir}/runs/pg"
schema_name="${case_id,,}_validation"
mkdir -p "${run_dir}"

psql_base=(psql -X -v ON_ERROR_STOP=1)
psql_query=(psql -X -q -v ON_ERROR_STOP=1 -A -t -F $'\t')

"${psql_base[@]}" -c "drop schema if exists ${schema_name} cascade;"
"${psql_base[@]}" -c "create schema ${schema_name};"
"${psql_base[@]}" -c "set search_path to ${schema_name};" -f "${case_dir}/schema/ddl_pg.sql"
"${psql_base[@]}" -c "set search_path to ${schema_name};" -f "${case_dir}/validation/pg_witness_data.sql"

run_query() {
  local sql_file="$1"
  local out_file="$2"
  "${psql_query[@]}" -c "set search_path to ${schema_name};" -f "${sql_file}" > "${out_file}"
}

run_query "${case_dir}/source.sql" "${run_dir}/source.tsv"
run_query "${case_dir}/rewrite_pos_01.sql" "${run_dir}/rewrite_pos_01.tsv"
run_query "${case_dir}/rewrite_neg_01.sql" "${run_dir}/rewrite_neg_01.tsv"

if cmp -s "${run_dir}/source.tsv" "${run_dir}/rewrite_pos_01.tsv"; then
  source_positive_equal=true
else
  source_positive_equal=false
fi

if cmp -s "${run_dir}/source.tsv" "${run_dir}/rewrite_neg_01.tsv"; then
  source_negative_different=false
else
  source_negative_different=true
fi

if [[ "${source_positive_equal}" == true && "${source_negative_different}" == true ]]; then
  status="ok"
else
  status="failed"
fi

cat > "${run_dir}/result_check.json" <<JSON
{
  "case_id": "${case_id}",
  "engine": "postgres",
  "status": "${status}",
  "source_positive_equal": ${source_positive_equal},
  "source_negative_different": ${source_negative_different},
  "artifacts": {
    "source": "runs/pg/source.tsv",
    "positive_rewrite": "runs/pg/rewrite_pos_01.tsv",
    "negative_rewrite": "runs/pg/rewrite_neg_01.tsv"
  },
  "notes": "PostgreSQL witness validation only; no PostgreSQL plan collection, MySQL, Spark, admission, promotion, common-core, or extended judgment is implied."
}
JSON

if [[ "${status}" != "ok" ]]; then
  exit 1
fi
