set search_path to attr24_sqlglot__sqlglot_optimize_same_dialect__cons_0037__pg;
begin read only;
set local statement_timeout = '60s';
explain (analyze, buffers, format json)
SELECT
  "emp"."deptno" AS "deptno",
  COUNT(DISTINCT "dept"."name") AS "_col_1"
FROM "emp" AS "emp"
LEFT JOIN "dept" AS "dept"
  ON "dept"."deptno" = "emp"."deptno"
GROUP BY
  "emp"."deptno";
rollback;
