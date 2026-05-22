set search_path to attr113_sqlglot_sqlglot_optimize_same_dialect_cons_0036_pg;
begin read only;
set local statement_timeout = '60s';
explain (analyze, buffers, format json)
SELECT
  "dept"."name" AS "name",
  COUNT(*) AS "c"
FROM "dept" AS "dept"
GROUP BY
  "dept"."name"
HAVING
  "name" = 'Charlie';
rollback;
