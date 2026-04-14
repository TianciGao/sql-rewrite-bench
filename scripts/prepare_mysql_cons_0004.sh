#!/usr/bin/env bash
set -euo pipefail

source "$PWD/scripts/env_mysql.sh"

mysql -h "$MYSQL_HOST" -P "$MYSQL_PORT" -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" "$MYSQL_DATABASE" <<'SQL'
DROP TABLE IF EXISTS EMP;

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

SELECT 'emp' AS table_name, COUNT(*) AS row_count FROM EMP;
SQL
