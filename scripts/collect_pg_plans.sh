#!/usr/bin/env bash
set -euo pipefail

source "$PWD/scripts/env_postgres.sh"
mkdir -p runs/plans/pg

for sql_file in \
  cases/PERF/PERF_0001/source.sql \
  cases/PERF/PERF_0001/rewrite_pos_01.sql \
  cases/PERF/PERF_0001/rewrite_neg_01.sql
do
  base="$(basename "$sql_file" .sql)"
  sql_text="$(cat "$sql_file")"
  echo "EXPLAIN (FORMAT JSON) $sql_text" | \
    psql -w -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" -At \
    > "runs/plans/pg/${base}.json"
done
