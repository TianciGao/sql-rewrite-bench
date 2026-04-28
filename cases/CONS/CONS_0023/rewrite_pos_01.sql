SELECT e1.empno, e1.sal
FROM emp e1
WHERE e1.comm > (
  (SELECT COUNT(*) FROM bonus b WHERE b.sal > e1.sal)
  *
  (SELECT COUNT(*) FROM dept d WHERE d.deptno = 10)
);
