SELECT *
FROM "dept"
WHERE EXISTS (SELECT "empno", "ename", "job", "mgr", "hiredate", "sal", "comm", "deptno"
FROM "emp"
WHERE "deptno" = "dept"."deptno"
OFFSET 2 ROWS
FETCH NEXT 1 ROWS ONLY)
