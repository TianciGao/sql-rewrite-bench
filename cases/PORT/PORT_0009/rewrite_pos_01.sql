SELECT t1.account_id FROM loan AS t1 INNER JOIN account AS t2 ON t1.account_id = t2.account_id WHERE YEAR(CAST(t2.date AS DATE)) = 1993 AND t1.duration > 12 ORDER BY t1.amount DESC LIMIT 1
