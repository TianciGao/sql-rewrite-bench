#!/usr/bin/env bash
set -euo pipefail

source "$PWD/scripts/env_mysql.sh"

mysql -h "$MYSQL_HOST" -P "$MYSQL_PORT" -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" "$MYSQL_DATABASE" <<'SQL'
DROP TABLE IF EXISTS employees_nulls;
CREATE TABLE employees_nulls (
  emp_id BIGINT,
  dept VARCHAR(20),
  emp_name VARCHAR(50),
  manager_id BIGINT NULL
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
