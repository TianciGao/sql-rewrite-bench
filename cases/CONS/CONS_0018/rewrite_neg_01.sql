SELECT *
FROM dept AS d
WHERE EXISTS (SELECT 1 FROM emp e WHERE d.deptno = e.deptno);
