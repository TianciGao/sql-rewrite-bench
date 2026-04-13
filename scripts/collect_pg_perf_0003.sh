#!/usr/bin/env bash
set -euo pipefail

source "$PWD/scripts/env_postgres.sh"

mkdir -p runs/perf_0003/plans/pg

SQL_TEXT="$(cat cases/PERF/PERF_0003/source.sql)"

printf 'EXPLAIN (FORMAT JSON) %s\n' "$SQL_TEXT" | \
  psql -w -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" -At \
  > runs/perf_0003/plans/pg/source.json
