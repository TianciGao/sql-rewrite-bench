#!/usr/bin/env bash
set -euo pipefail

source "$PWD/scripts/env_postgres.sh"

psql -w -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" -v ON_ERROR_STOP=1 <<'SQL'
DROP TABLE IF EXISTS EMP CASCADE;

CREATE TABLE EMP (
  EMPNO INT NOT NULL PRIMARY KEY,
  MGR INT,
  JOB TEXT NOT NULL
);

INSERT INTO EMP (EMPNO, MGR, JOB) VALUES
  (1, NULL, 'Clerk'),
  (2, NULL, 'Clerk'),
  (3, NULL, 'Clerk'),
  (4, NULL, 'Clerk'),
  (5, NULL, 'Analyst'),
  (6, 100, 'Clerk');

SELECT 'emp', COUNT(*) FROM EMP;
SQL
