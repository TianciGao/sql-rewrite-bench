#!/usr/bin/env bash
set -euo pipefail

source "$PWD/scripts/env_postgres.sh"

mkdir -p runs/perf_0003/pg

echo "=== PG :: PERF_0003 :: source ==="
psql -w -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" -At -F $'\t' \
  -f cases/PERF/PERF_0003/source.sql | tee runs/perf_0003/pg/source.tsv

echo
echo "=== PG :: PERF_0003 :: rewrite_pos_01 ==="
psql -w -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" -At -F $'\t' \
  -f cases/PERF/PERF_0003/rewrite_pos_01.sql | tee runs/perf_0003/pg/rewrite_pos_01.tsv

echo
echo "=== PG :: PERF_0003 :: rewrite_neg_01 ==="
psql -w -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" -At -F $'\t' \
  -f cases/PERF/PERF_0003/rewrite_neg_01.sql | tee runs/perf_0003/pg/rewrite_neg_01.tsv
