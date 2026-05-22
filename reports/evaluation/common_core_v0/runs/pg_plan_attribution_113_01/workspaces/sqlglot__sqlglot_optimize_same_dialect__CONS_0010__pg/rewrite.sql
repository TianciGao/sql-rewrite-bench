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
  )
