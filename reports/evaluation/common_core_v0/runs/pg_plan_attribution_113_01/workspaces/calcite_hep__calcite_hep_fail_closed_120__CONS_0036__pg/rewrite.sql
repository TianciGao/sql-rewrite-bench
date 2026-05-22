SELECT "name", COUNT(*) AS "c"
FROM "dept"
GROUP BY "name"
HAVING "name" = 'Charlie'
