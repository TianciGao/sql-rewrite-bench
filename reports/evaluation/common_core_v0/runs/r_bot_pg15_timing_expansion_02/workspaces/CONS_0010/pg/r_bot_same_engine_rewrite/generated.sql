SELECT "emp"."empno", "emp"."ename", "emp"."job", "emp"."mgr", "emp"."hiredate", "emp"."sal", "emp"."comm", "emp"."deptno"
FROM "emp"
    LEFT JOIN (SELECT "t0"."empno1", "t1"."job2", "t0"."sal1", TRUE AS "$f3"
        FROM "emp" AS "emp0" ("empno0", "ename0", "job0", "mgr0", "hiredate0", "sal0", "comm0", "deptno0")
            INNER JOIN (SELECT "empno1", "sal1"
                FROM "emp" AS "emp1" ("empno1", "ename1", "job1", "mgr1", "hiredate1", "sal1", "comm1", "deptno1")
                GROUP BY "empno1", "sal1") AS "t0" ON "emp0"."empno0" <> "t0"."empno1" AND "emp0"."sal0" = "t0"."sal1"
            CROSS JOIN (SELECT *
                FROM "bonus" AS "bonus" ("ename2", "job2", "sal2", "comm2")
                WHERE "job2" IS NOT NULL) AS "t1"
        GROUP BY "t0"."empno1", "t1"."job2", "t0"."sal1") AS "t4" ON "emp"."empno" = "t4"."empno1" AND "emp"."job" = "t4"."job2" AND "emp"."sal" = "t4"."sal1"
WHERE "t4"."$f3" IS NULL;
