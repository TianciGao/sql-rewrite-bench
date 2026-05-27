SELECT b1.deptno
FROM b AS b1
WHERE b1.ename <> 'WARD'
   OR NOT EXISTS (
        SELECT 1
        FROM a
        WHERE a.deptno = b1.deptno
          AND a.ename = 'WARD'
      );
