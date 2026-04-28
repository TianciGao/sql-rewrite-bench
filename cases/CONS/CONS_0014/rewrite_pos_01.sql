SELECT a.deptno
FROM b AS a
WHERE a.ename <> 'WARD'
   OR NOT EXISTS (
        SELECT 1
        FROM a AS a2
        WHERE a2.deptno = a.deptno
          AND a2.ename = 'WARD'
      );
