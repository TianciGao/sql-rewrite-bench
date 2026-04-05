#!/usr/bin/env bash
set -euo pipefail

source "$PWD/scripts/env_postgres.sh"
psql -w -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" -c "SELECT 1;"
