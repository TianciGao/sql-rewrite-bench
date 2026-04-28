SELECT *
FROM dept AS d
WHERE EXISTS (SELECT COUNT(*) FROM emp e WHERE d.deptno = e.deptno);
