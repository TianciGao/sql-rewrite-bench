#!/usr/bin/env bash
set -euo pipefail

source "$PWD/scripts/env_postgres.sh"

mkdir -p runs/port_0002/pg

echo "=== PG :: PORT_0002 :: source ==="
psql -w -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" -At -F $'\t' \
  -f cases/PORT/PORT_0002/source.sql | tee runs/port_0002/pg/source.tsv
