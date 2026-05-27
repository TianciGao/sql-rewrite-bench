SELECT t2.driverid, t2.code FROM results AS t1 INNER JOIN drivers AS t2 ON t1.driverid = t2.driverid WHERE YEAR(CAST(t2.dob AS DATE)) = 1972 AND t1.fastestlaptime IS NOT NULL
