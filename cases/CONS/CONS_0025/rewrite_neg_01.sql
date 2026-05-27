SELECT d1.deptno
FROM dept d1
WHERE EXISTS (SELECT 1 FROM dept d2 WHERE d2.deptno = d1.deptno)
  AND EXISTS (SELECT 1 FROM dept d3 WHERE d3.loc = d1.loc AND d3.dname <> d1.dname);
