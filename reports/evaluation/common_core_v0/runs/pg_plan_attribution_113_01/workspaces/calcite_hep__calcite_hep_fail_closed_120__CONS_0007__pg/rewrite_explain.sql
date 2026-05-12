set search_path to attr113_calcite_hep_calcite_hep_fail_closed_120_cons_0007_pg;
begin read only;
set local statement_timeout = '60s';
explain (analyze, buffers, format json)
SELECT *
FROM "tmp_emps"
WHERE EXISTS (SELECT *
FROM (SELECT "deptno"
FROM "tmp_emps" AS "tmp_emps0"
WHERE "commission" = "tmp_emps"."commission") AS "t0"
WHERE "deptno" <> "tmp_emps"."deptno");
rollback;
