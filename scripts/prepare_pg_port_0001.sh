#!/usr/bin/env bash
set -euo pipefail

source "$PWD/scripts/env_postgres.sh"

psql -w -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" <<'SQL'
DROP TABLE IF EXISTS events_monthly;
CREATE TABLE events_monthly (
  event_id BIGINT,
  dept TEXT,
  event_ts TIMESTAMP
);
INSERT INTO events_monthly (event_id, dept, event_ts) VALUES
  (1, 'eng',   '2024-01-01 09:00:00'),
  (2, 'eng',   '2024-01-31 23:59:59'),
  (3, 'eng',   '2024-02-01 00:00:00'),
  (4, 'sales', '2024-01-15 12:00:00'),
  (5, 'sales', '2023-01-20 08:00:00');
SELECT * FROM events_monthly ORDER BY event_id;
SQL
