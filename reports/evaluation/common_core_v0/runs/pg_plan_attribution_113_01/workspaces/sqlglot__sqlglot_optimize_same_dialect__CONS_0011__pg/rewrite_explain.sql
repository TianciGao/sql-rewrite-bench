set search_path to attr113_sqlglot_sqlglot_optimize_same_dialect_cons_0011_pg;
begin read only;
set local statement_timeout = '60s';
explain (analyze, buffers, format json)
SELECT
  "e1"."ename" AS "ename"
FROM "emp" AS "e1"
WHERE
  EXISTS(
    SELECT
      1 AS "1"
    FROM "dept" AS "d"
    LEFT JOIN "bonus" AS "b"
      ON "b"."ename" = "d"."dname" AND "b"."job" = "e1"."job"
    WHERE
      "b"."ename" IS NULL
  );
rollback;
