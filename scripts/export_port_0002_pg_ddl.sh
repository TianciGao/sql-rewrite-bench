#!/usr/bin/env bash
set -euo pipefail

: "${PGPASSWORD:?PGPASSWORD must be set}"
: "${PGHOST:?PGHOST must be set}"
: "${PGPORT:?PGPORT must be set}"
: "${PGDATABASE:?PGDATABASE must be set}"
: "${PGUSER:?PGUSER must be set}"

OUT="cases/PORT/PORT_0002/schema/ddl_pg.sql"
mkdir -p "$(dirname "$OUT")"

psql -w -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" -At <<'SQL' > "$OUT"
WITH cols AS (
  SELECT
    ordinal_position,
    column_name,
    data_type,
    udt_name,
    character_maximum_length,
    numeric_precision,
    numeric_scale,
    is_nullable
  FROM information_schema.columns
  WHERE table_schema = 'public'
    AND table_name = 'votes'
)
SELECT
  'CREATE TABLE votes (' || E'\n' ||
  string_agg(
    '  ' || quote_ident(column_name) || ' ' ||
    CASE
      WHEN data_type = 'character varying' THEN 'VARCHAR(' || character_maximum_length || ')'
      WHEN data_type = 'character' THEN 'CHAR(' || character_maximum_length || ')'
      WHEN data_type = 'timestamp without time zone' THEN 'TIMESTAMP'
      WHEN data_type = 'timestamp with time zone' THEN 'TIMESTAMPTZ'
      WHEN data_type = 'date' THEN 'DATE'
      WHEN data_type = 'integer' THEN 'INTEGER'
      WHEN data_type = 'bigint' THEN 'BIGINT'
      WHEN data_type = 'smallint' THEN 'SMALLINT'
      WHEN data_type = 'boolean' THEN 'BOOLEAN'
      WHEN data_type = 'numeric' THEN 'NUMERIC(' || numeric_precision || ',' || numeric_scale || ')'
      WHEN data_type = 'double precision' THEN 'DOUBLE PRECISION'
      WHEN data_type = 'real' THEN 'REAL'
      WHEN data_type = 'text' THEN 'TEXT'
      ELSE upper(udt_name)
    END ||
    CASE WHEN is_nullable = 'NO' THEN ' NOT NULL' ELSE '' END,
    E',\n'
    ORDER BY ordinal_position
  ) || E'\n);'
FROM cols;
SQL

echo "[OK] wrote $OUT"
