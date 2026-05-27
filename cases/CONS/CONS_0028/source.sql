SELECT e1.empno, e1.sal
FROM emp e1
WHERE e1.comm > (
  SELECT COUNT(*)
  FROM bonus b
  LEFT JOIN dept d
    ON b.sal > e1.sal
   AND d.deptno = 10
);
