SELECT
  empid,
  EXISTS (
    SELECT 1
    FROM emps e2
    WHERE e1.commission = e2.commission
  ) AS exists_flag
FROM emps e1
ORDER BY empid;
