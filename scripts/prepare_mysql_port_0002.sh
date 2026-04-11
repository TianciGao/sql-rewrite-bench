#!/usr/bin/env bash
set -euo pipefail

source "$PWD/scripts/env_mysql.sh"

mysql -h "$MYSQL_HOST" -P "$MYSQL_PORT" -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" "$MYSQL_DATABASE" <<'SQL'
DROP TABLE IF EXISTS votes;

CREATE TABLE votes (
  id BIGINT PRIMARY KEY,
  creationdate DATETIME NOT NULL
);

INSERT INTO votes (id, creationdate) VALUES
  (1, '2010-01-05 10:00:00'),
  (2, '2010-06-12 09:30:00'),
  (3, '2010-12-31 23:59:59'),
  (4, '2011-02-01 08:00:00'),
  (5, '2011-09-09 14:15:00'),
  (6, '2012-01-01 00:00:00');

SELECT 'votes' AS table_name, COUNT(*) AS row_count FROM votes;
SQL
