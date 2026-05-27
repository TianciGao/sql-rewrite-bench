SELECT "name", COUNT(*) AS "c"
FROM "dept"
WHERE "name" = 'Charlie'
GROUP BY "name";
