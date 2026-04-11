#!/usr/bin/env bash
set -euo pipefail

source "$PWD/scripts/env_postgres.sh"

psql -w -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" -v ON_ERROR_STOP=1 <<'SQL'
DROP TABLE IF EXISTS votes CASCADE;

CREATE TABLE votes (
  id BIGINT PRIMARY KEY,
  creationdate TIMESTAMP NOT NULL
);

INSERT INTO votes (id, creationdate) VALUES
  (1, '2010-01-05 10:00:00'),
  (2, '2010-06-12 09:30:00'),
  (3, '2010-12-31 23:59:59'),
  (4, '2011-02-01 08:00:00'),
  (5, '2011-09-09 14:15:00'),
  (6, '2012-01-01 00:00:00');

SELECT 'votes', COUNT(*) FROM votes;
SQL
