set search_path to attr113_calcite_hep_calcite_hep_fail_closed_120_cons_0037_pg;
begin read only;
set local statement_timeout = '60s';
explain (analyze, buffers, format json)
SELECT "emp"."deptno", COUNT(DISTINCT "dept"."name")
FROM "emp"
LEFT JOIN "dept" ON "emp"."deptno" = "dept"."deptno"
GROUP BY "emp"."deptno";
rollback;
