SELECT
  "dept"."name" AS "name",
  COUNT(*) AS "c"
FROM "dept" AS "dept"
GROUP BY
  "dept"."name"
HAVING
  "name" = 'Charlie'
