SELECT 100.0 * SUM(CASE WHEN t2.language = 'Japanese' THEN 1 ELSE 0 END) / COUNT(t1.id) FROM cards AS t1 INNER JOIN foreign_data AS t2 ON t1.uuid = t2.uuid
