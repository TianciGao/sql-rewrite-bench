#!/usr/bin/env bash
set -euo pipefail

source "$PWD/scripts/env_postgres.sh"

mkdir -p runs/perf_0004/pg

echo "=== PG :: PERF_0004 :: source ==="
psql -w -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" -At -F $'\t' \
  -f cases/PERF/PERF_0004/source.sql | tee runs/perf_0004/pg/source.tsv
