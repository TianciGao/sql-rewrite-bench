#!/usr/bin/env bash
set -euo pipefail

source "$PWD/scripts/env_mysql.sh"

mysql -h "$MYSQL_HOST" -P "$MYSQL_PORT" -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" "$MYSQL_DATABASE" <<'SQL'
DROP TABLE IF EXISTS employees;
CREATE TABLE employees (
  emp_id BIGINT,
  dept VARCHAR(20),
  emp_name VARCHAR(50),
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
