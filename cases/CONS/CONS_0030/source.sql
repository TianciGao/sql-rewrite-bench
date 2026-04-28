SELECT empno
FROM emp AS e
LEFT JOIN dept AS d
  ON d.dname = e.ename
 AND EXISTS (
   SELECT e2.deptno
   FROM emp AS e2
   WHERE e2.deptno = e.deptno
   GROUP BY e2.deptno
   HAVING SUM(e2.sal) > 1000000
 );
