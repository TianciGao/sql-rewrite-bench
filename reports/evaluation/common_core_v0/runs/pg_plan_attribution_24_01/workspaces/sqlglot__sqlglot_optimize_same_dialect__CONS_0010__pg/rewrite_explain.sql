set search_path to attr24_sqlglot__sqlglot_optimize_same_dialect__cons_0010__pg;
begin read only;
set local statement_timeout = '60s';
explain (analyze, buffers, format json)
SELECT
  "e1".*
FROM "emp" AS "e1"
WHERE
  NOT EXISTS(
    SELECT
      1 AS "1"
    FROM "emp" AS "e2"
    JOIN "bonus" AS "b"
      ON "b"."job" = "e1"."job" AND "e1"."sal" = "e2"."sal"
    WHERE
      "e1"."empno" <> "e2"."empno"
  );
rollback;
