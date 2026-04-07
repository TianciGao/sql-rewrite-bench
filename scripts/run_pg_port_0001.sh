#!/usr/bin/env bash
set -euo pipefail

source "$PWD/scripts/env_postgres.sh"
mkdir -p runs/port_case/pg

for sql_file in \
  cases/PORT/PORT_0001/source.sql \
  cases/PORT/PORT_0001/rewrite_pos_01.sql \
  cases/PORT/PORT_0001/rewrite_neg_01.sql
do
  base="$(basename "$sql_file" .sql)"
  echo "=== PG :: $base ==="
  psql -w -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" -At -F $'\t' -f "$sql_file" | tee "runs/port_case/pg/${base}.tsv"
  echo
done
