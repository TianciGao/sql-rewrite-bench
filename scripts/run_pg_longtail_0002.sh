#!/usr/bin/env bash
set -euo pipefail

source "$PWD/scripts/env_postgres.sh"

mkdir -p runs/longtail_0002/pg

echo "=== PG :: LONGTAIL_0002 :: source ==="
psql -w -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" -At -F $'\t' \
  -f cases/LONGTAIL/LONGTAIL_0002/source.sql | tee runs/longtail_0002/pg/source.tsv
