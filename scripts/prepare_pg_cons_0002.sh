#!/usr/bin/env bash
set -euo pipefail

source "$PWD/scripts/env_postgres.sh"

psql -w -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" -v ON_ERROR_STOP=1 <<'SQL'
DROP TABLE IF EXISTS emps CASCADE;

CREATE TABLE emps (
  empid BIGINT NOT NULL,
  deptno BIGINT NOT NULL,
  name TEXT NOT NULL,
  salary NUMERIC(10,2) NOT NULL,
  commission BIGINT
);

INSERT INTO emps (empid, deptno, name, salary, commission) VALUES
  (100, 10, 'Bill',      10000.00, 1000),
  (200, 20, 'Eric',       8000.00,  500),
  (150, 10, 'Sebastian',  7000.00, NULL),
  (110, 10, 'Theodore',  11500.00,  250),
  (170, 30, 'Theodore',  11500.00,  250),
  (140, 10, 'Sebastian',  7000.00, NULL);

SELECT 'emps', COUNT(*) FROM emps;
SQL
