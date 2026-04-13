#!/usr/bin/env bash
set -euo pipefail

source "$PWD/scripts/env_postgres.sh"

mkdir -p runs/perf_0003/pg

echo "=== PG :: PERF_0003 :: source ==="
psql -w -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" -At -F $'\t' \
  -f cases/PERF/PERF_0003/source.sql | tee runs/perf_0003/pg/source.tsv
