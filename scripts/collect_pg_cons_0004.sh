#!/usr/bin/env bash
set -euo pipefail

source "$PWD/scripts/env_postgres.sh"

mkdir -p runs/cons_0004/plans/pg

for sql_file in \
  cases/CONS/CONS_0004/source.sql \
  cases/CONS/CONS_0004/rewrite_pos_01.sql \
  cases/CONS/CONS_0004/rewrite_neg_01.sql
do
  base="$(basename "$sql_file" .sql)"
  SQL_TEXT="$(cat "$sql_file")"
  printf 'EXPLAIN (FORMAT JSON) %s\n' "$SQL_TEXT" | \
    psql -w -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" -At \
    > "runs/cons_0004/plans/pg/${base}.json"
done
