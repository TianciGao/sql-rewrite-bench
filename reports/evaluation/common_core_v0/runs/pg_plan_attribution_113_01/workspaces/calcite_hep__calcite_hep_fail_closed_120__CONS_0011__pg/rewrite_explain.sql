set search_path to attr113_calcite_hep_calcite_hep_fail_closed_120_cons_0011_pg;
begin read only;
set local statement_timeout = '60s';
explain (analyze, buffers, format json)
SELECT "ename" AS "ENAME"
FROM "emp"
WHERE EXISTS (SELECT *
FROM "dept"
LEFT JOIN "bonus" ON "dept"."dname" = "bonus"."ename" AND "bonus"."job" = "emp"."job"
WHERE "bonus"."ename" IS NULL);
rollback;
