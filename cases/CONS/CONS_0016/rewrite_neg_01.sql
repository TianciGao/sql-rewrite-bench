SELECT t1.*
FROM table1 AS t1
WHERE t1.j = 3
   OR NOT EXISTS (
        SELECT 1
        FROM table2 AS t2
        WHERE t2.i = t1.j OR t2.i IS NULL
      );
