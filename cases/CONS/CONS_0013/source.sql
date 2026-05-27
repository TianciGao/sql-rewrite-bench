SELECT deptno
FROM b AS b1
WHERE deptno NOT IN (
  SELECT deptno
  FROM a
  WHERE deptno = b1.deptno
    AND ename = 'WARD'
    AND b1.ename = 'WARD'
);
