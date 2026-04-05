#!/usr/bin/env bash
set -euo pipefail

source "$PWD/scripts/env_mysql.sh"

mysql -h "$MYSQL_HOST" -P "$MYSQL_PORT" -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" "$MYSQL_DATABASE" <<'SQL'
DROP TABLE IF EXISTS t;
CREATE TABLE t (
  id BIGINT,
  val VARCHAR(20)
);
INSERT INTO t (id, val) VALUES
  (1, 'a'),
  (2, 'b'),
  (3, 'c');
SELECT id, val FROM t WHERE id >= 2 ORDER BY id;
SQL
