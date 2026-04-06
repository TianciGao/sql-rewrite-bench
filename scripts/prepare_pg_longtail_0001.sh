#!/usr/bin/env bash
set -euo pipefail

source "$PWD/scripts/env_postgres.sh"

psql -w -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" <<'SQL'
DROP TABLE IF EXISTS employees;
CREATE TABLE employees (
  emp_id BIGINT,
  dept TEXT,
  emp_name TEXT,
  salary BIGINT
);

INSERT INTO employees (emp_id, dept, emp_name, salary) VALUES
  (1, 'eng',   'alice', 120),
  (2, 'eng',   'bob',   115),
  (3, 'eng',   'carol', 115),
  (4, 'sales', 'dan',    95),
  (5, 'sales', 'emma',  110),
  (6, 'sales', 'frank',  90);

SELECT emp_id, dept, emp_name, salary
FROM employees
ORDER BY emp_id;
SQL
