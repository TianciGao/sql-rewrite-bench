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
  )
