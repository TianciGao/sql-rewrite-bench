SELECT event_id, dept
FROM events_monthly
WHERE event_ts >= '2024-01-01 00:00:00'
  AND event_ts <= '2024-01-31 00:00:00'
ORDER BY event_id;
