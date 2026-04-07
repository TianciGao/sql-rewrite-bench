#!/usr/bin/env bash
set -euo pipefail

source "$PWD/scripts/env_mysql.sh"

mysql -h "$MYSQL_HOST" -P "$MYSQL_PORT" -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" "$MYSQL_DATABASE" <<'SQL'
DROP TABLE IF EXISTS events_monthly;
CREATE TABLE events_monthly (
  event_id BIGINT,
  dept VARCHAR(20),
  event_ts DATETIME
);
INSERT INTO events_monthly (event_id, dept, event_ts) VALUES
  (1, 'eng',   '2024-01-01 09:00:00'),
  (2, 'eng',   '2024-01-31 23:59:59'),
  (3, 'eng',   '2024-02-01 00:00:00'),
  (4, 'sales', '2024-01-15 12:00:00'),
  (5, 'sales', '2023-01-20 08:00:00');
SELECT * FROM events_monthly ORDER BY event_id;
SQL
