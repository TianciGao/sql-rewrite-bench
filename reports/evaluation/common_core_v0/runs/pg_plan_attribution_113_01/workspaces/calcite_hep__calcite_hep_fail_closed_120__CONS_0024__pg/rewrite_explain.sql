set search_path to attr113_calcite_hep_calcite_hep_fail_closed_120_cons_0024_pg;
begin read only;
set local statement_timeout = '60s';
explain (analyze, buffers, format json)
SELECT "emp"."empno"
FROM "emp"
LEFT JOIN "dept" ON "emp"."deptno" = "dept"."deptno" AND EXISTS (SELECT "deptno", SUM("sal") AS "$f1"
FROM "emp"
WHERE "deptno" = "dept"."deptno"
GROUP BY "deptno"
HAVING SUM("sal") > 1000000.00);
rollback;
