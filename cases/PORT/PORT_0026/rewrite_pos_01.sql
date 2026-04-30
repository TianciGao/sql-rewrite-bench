SELECT 100.0 * COUNT(CASE WHEN t2.time IS NOT NULL THEN t2.driverid END) / COUNT(t2.driverid) FROM races AS t1 INNER JOIN results AS t2 ON t2.raceid = t1.raceid WHERE t1.date = '1983-07-16'
