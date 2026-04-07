SELECT event_id, dept
FROM events_monthly
WHERE EXTRACT(YEAR FROM event_ts) = 2024
  AND EXTRACT(MONTH FROM event_ts) = 1
ORDER BY event_id;
