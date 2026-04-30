SELECT 1.0 * COUNT(DISTINCT t2.id) / COUNT(DISTINCT t1.id) FROM votes AS t1 INNER JOIN posts AS t2 ON t1.userid = t2.owneruserid WHERE t1.userid = 25
