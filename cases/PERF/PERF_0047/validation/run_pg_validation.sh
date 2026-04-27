#!/usr/bin/env bash
set -euo pipefail

case_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
run_dir="${case_dir}/runs/pg"
schema_name="perf_0047_validation"

mkdir -p "${run_dir}"

psql_base=(psql -X -v ON_ERROR_STOP=1)
psql_query=(psql -X -q -v ON_ERROR_STOP=1 -A -t -F $'	')

"${psql_base[@]}" -c "drop schema if exists ${schema_name} cascade;"
"${psql_base[@]}" -c "create schema ${schema_name};"
"${psql_base[@]}" -c "set search_path to ${schema_name};" -f "${case_dir}/schema/ddl_pg.sql"
"${psql_base[@]}" -c "set search_path to ${schema_name};" -f "${case_dir}/validation/pg_witness_data.sql"

run_query() {
  local query_file="$1"
  local output_file="$2"

  "${psql_query[@]}" -c "set search_path to ${schema_name};" -f "${case_dir}/${query_file}" > "${run_dir}/${output_file}"
}

run_query "source.sql" "source.tsv"
run_query "rewrite_pos_01.sql" "rewrite_pos_01.tsv"
run_query "rewrite_neg_01.sql" "rewrite_neg_01.tsv"

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

if [[ "${source_positive_equal}" == "true" && "${source_negative_different}" == "true" ]]; then
  ok=true
else
  ok=false
fi

cat > "${run_dir}/result_check.json" <<JSON
{
  "case_id": "PERF_0047",
  "engine": "postgres",
  "status": "validated",
  "ok": ${ok},
  "schema": "${schema_name}",
  "inputs": {
    "source": "source.sql",
    "positive_rewrite": "rewrite_pos_01.sql",
    "negative_rewrite": "rewrite_neg_01.sql",
    "witness_data": "validation/pg_witness_data.sql"
  },
  "outputs": {
    "source": "runs/pg/source.tsv",
    "positive_rewrite": "runs/pg/rewrite_pos_01.tsv",
    "negative_rewrite": "runs/pg/rewrite_neg_01.tsv"
  },
  "checks": {
    "source_positive_equal": ${source_positive_equal},
    "source_negative_different": ${source_negative_different}
  },
  "notes": [
    "PostgreSQL-only witness validation.",
    "No MySQL or Spark validation is implied.",
    "No plans were collected."
  ]
}
JSON

if [[ "${ok}" == "true" ]]; then
  exit 0
fi

exit 1
