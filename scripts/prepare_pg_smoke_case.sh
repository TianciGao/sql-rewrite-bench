#!/usr/bin/env bash
set -euo pipefail

source "$PWD/scripts/env_postgres.sh"

psql -w -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" <<'SQL'
DROP TABLE IF EXISTS t;
CREATE TABLE t (
  id BIGINT,
  val TEXT
);
INSERT INTO t (id, val) VALUES
  (1, 'a'),
  (2, 'b'),
  (3, 'c');
SELECT id, val FROM t WHERE id >= 2 ORDER BY id;
SQL
