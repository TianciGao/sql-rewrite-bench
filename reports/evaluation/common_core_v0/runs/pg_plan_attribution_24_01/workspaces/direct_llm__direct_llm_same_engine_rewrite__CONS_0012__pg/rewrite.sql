SELECT *
FROM dept d
WHERE EXISTS (
  SELECT 1
  FROM emp e
  WHERE e.deptno = d.deptno
  LIMIT 1 OFFSET 2
);
