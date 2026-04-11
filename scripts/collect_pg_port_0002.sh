#!/usr/bin/env bash
set -euo pipefail

source "$PWD/scripts/env_postgres.sh"

mkdir -p runs/port_0002/plans/pg

SQL_TEXT="$(cat cases/PORT/PORT_0002/source.sql)"

printf 'EXPLAIN (FORMAT JSON) %s\n' "$SQL_TEXT" | \
  psql -w -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" -At \
  > runs/port_0002/plans/pg/source.json
