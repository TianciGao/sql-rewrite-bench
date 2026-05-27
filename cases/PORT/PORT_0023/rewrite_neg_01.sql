SELECT 1.0 * SUM(t2.long_shots) / COUNT(t2.attr_date) FROM player AS t1 INNER JOIN player_attributes AS t2 ON t1.player_api_id = t2.player_api_id WHERE t1.player_name = 'Other Player'
