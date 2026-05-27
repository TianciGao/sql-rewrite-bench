SELECT *
FROM tmp_emps e1
WHERE EXISTS (
  SELECT *
  FROM tmp_emps e2
  WHERE e2.commission = e1.commission
  AND e2.deptno <> e1.deptno
);
