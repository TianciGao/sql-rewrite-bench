SELECT deptno
FROM b AS a
WHERE deptno NOT IN (
  SELECT deptno
  FROM a
  WHERE deptno = a.deptno
    AND ename = 'WARD'
    AND a.ename = 'WARD'
);
