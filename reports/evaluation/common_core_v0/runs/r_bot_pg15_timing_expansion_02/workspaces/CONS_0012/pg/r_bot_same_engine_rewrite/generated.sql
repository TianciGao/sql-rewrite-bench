SELECT "$cor0"."deptno", "$cor0"."dname", "$cor0"."loc"
FROM "dept" AS "$cor0",
    LATERAL (SELECT TRUE AS "i"
        FROM "emp" AS "emp" ("empno", "ename", "job", "mgr", "hiredate", "sal", "comm", "deptno0")
        WHERE "deptno0" = "$cor0"."deptno"
        OFFSET 2 ROWS
        FETCH NEXT 1 ROWS ONLY) AS "t2";
