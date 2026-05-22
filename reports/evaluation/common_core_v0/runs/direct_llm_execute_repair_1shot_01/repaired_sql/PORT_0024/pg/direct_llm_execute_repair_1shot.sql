SELECT CAST(SUM(CASE WHEN istextless = 0 AND isstoryspotlight = 1 THEN 1 ELSE 0 END) AS DOUBLE PRECISION) * 100 / COUNT(id) FROM cards;
