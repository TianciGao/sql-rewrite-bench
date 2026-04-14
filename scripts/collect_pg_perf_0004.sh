#!/usr/bin/env bash
set -euo pipefail

source "$PWD/scripts/env_postgres.sh"

mkdir -p runs/perf_0004/plans/pg

for sql_file in \
  cases/PERF/PERF_0004/source.sql \
  cases/PERF/PERF_0004/rewrite_pos_01.sql \
  cases/PERF/PERF_0004/rewrite_neg_01.sql
do
  base="$(basename "$sql_file" .sql)"
  SQL_TEXT="$(cat "$sql_file")"
  printf 'EXPLAIN (FORMAT JSON) %s\n' "$SQL_TEXT" | \
    psql -w -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" -At \
    > "runs/perf_0004/plans/pg/${base}.json"
done
