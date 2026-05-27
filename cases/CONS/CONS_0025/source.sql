SELECT deptno
FROM dept d1
WHERE EXISTS (
  SELECT 1
  FROM dept d2, dept d3
  WHERE d2.deptno = d1.deptno
    AND d3.dname = d1.dname
);
