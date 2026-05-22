SELECT "emp"."deptno", COUNT(DISTINCT "dept"."name")
FROM "emp"
LEFT JOIN "dept" ON "emp"."deptno" = "dept"."deptno"
GROUP BY "emp"."deptno"
