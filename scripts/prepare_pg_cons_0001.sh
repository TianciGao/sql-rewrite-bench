#!/usr/bin/env bash
set -euo pipefail

source "$PWD/scripts/env_postgres.sh"

psql -w -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" <<'SQL'
DROP TABLE IF EXISTS employees_nulls;
CREATE TABLE employees_nulls (
  emp_id BIGINT,
  dept TEXT,
  emp_name TEXT,
  manager_id BIGINT
);
INSERT INTO employees_nulls (emp_id, dept, emp_name, manager_id) VALUES
  (1, 'eng',   'alice', 10),
  (2, 'eng',   'bob',   NULL),
  (3, 'eng',   'carol', 10),
  (4, 'sales', 'dan',   NULL),
  (5, 'sales', 'emma',  20),
  (6, 'hr',    'frank', NULL);
SELECT * FROM employees_nulls ORDER BY emp_id;
SQL
