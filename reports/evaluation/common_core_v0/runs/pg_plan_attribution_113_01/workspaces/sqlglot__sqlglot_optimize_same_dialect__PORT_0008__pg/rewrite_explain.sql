set search_path to attr113_sqlglot_sqlglot_optimize_same_dialect_port_0008_pg;
begin read only;
set local statement_timeout = '60s';
explain (analyze, buffers, format json)
SELECT
  "t2"."admemail1" AS "admemail1",
  "t2"."admemail2" AS "admemail2"
FROM "frpm" AS "t1"
JOIN "schools" AS "t2"
  ON "t1"."cdscode" = "t2"."cdscode"
  AND "t2"."city" = 'San Bernardino'
  AND "t2"."county" = 'San Bernardino'
  AND CAST("t2"."doc" AS INT) = 54
  AND CAST("t2"."soc" AS INT) = 62
  AND EXTRACT(YEAR FROM CAST("t2"."opendate" AS TIMESTAMP)) <= 2010
  AND EXTRACT(YEAR FROM CAST("t2"."opendate" AS TIMESTAMP)) >= 2009;
rollback;
