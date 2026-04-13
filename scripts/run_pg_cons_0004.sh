#!/usr/bin/env bash
set -euo pipefail

source "$PWD/scripts/env_postgres.sh"

mkdir -p runs/cons_0004/pg

echo "=== PG :: CONS_0004 :: source ==="
psql -w -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" -At -F $'\t' \
  -f cases/CONS/CONS_0004/source.sql | sort | tee runs/cons_0004/pg/source.tsv

echo
echo "=== PG :: CONS_0004 :: rewrite_pos_01 ==="
psql -w -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" -At -F $'\t' \
  -f cases/CONS/CONS_0004/rewrite_pos_01.sql | sort | tee runs/cons_0004/pg/rewrite_pos_01.tsv

echo
echo "=== PG :: CONS_0004 :: rewrite_neg_01 ==="
psql -w -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" -At -F $'\t' \
  -f cases/CONS/CONS_0004/rewrite_neg_01.sql | sort | tee runs/cons_0004/pg/rewrite_neg_01.tsv
