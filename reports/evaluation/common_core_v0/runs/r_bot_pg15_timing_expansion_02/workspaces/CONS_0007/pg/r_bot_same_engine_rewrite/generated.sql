SELECT "tmp_emps"."empid", "tmp_emps"."deptno", "tmp_emps"."name", "tmp_emps"."salary", "tmp_emps"."commission"
FROM "tmp_emps"
    INNER JOIN (SELECT "t2"."deptno1", "t0"."commission0", TRUE AS "$f2"
        FROM (SELECT "deptno0", "commission0"
                FROM "tmp_emps" AS "tmp_emps0" ("empid0", "deptno0", "name0", "salary0", "commission0")
                WHERE "commission0" IS NOT NULL) AS "t0"
            INNER JOIN (SELECT "deptno1"
                FROM "tmp_emps" AS "tmp_emps1" ("empid1", "deptno1", "name1", "salary1", "commission1")
                GROUP BY "deptno1") AS "t2" ON "t0"."deptno0" <> "t2"."deptno1"
        GROUP BY "t2"."deptno1", "t0"."commission0") AS "t5" ON "tmp_emps"."deptno" = "t5"."deptno1" AND "tmp_emps"."commission" = "t5"."commission0";
