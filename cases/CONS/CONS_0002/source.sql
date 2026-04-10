SELECT
  empid,
  EXISTS (
    SELECT *
    FROM (
      SELECT e2.deptno
      FROM emps e2
      WHERE e1.commission = e2.commission
    ) AS table3
    WHERE table3.deptno <> e1.deptno
  ) AS exists_flag
FROM emps e1
ORDER BY empid;
