SELECT "table1"."i", "table1"."j"
FROM "table1"
    LEFT JOIN (SELECT "j0", COUNT(*) AS "c", COUNT("i0") AS "ck"
        FROM "table2" AS "table2" ("i0", "j0")
        WHERE "j0" IS NOT NULL
        GROUP BY "j0") AS "t1" ON "table1"."i" = "t1"."j0"
    LEFT JOIN (SELECT "i1", "j1", TRUE AS "i"
        FROM "table2" AS "table20" ("i1", "j1")
        WHERE "j1" IS NOT NULL
        GROUP BY "i1", "j1"
        HAVING "i1" IS NOT NULL) AS "t4" ON "table1"."i" = "t4"."j1" AND "table1"."j" = "t4"."i1"
WHERE "t1"."c" = 0 OR ("table1"."j" IS NULL OR "t4"."i" IS NOT NULL OR "t1"."ck" < "t1"."c") IS NOT TRUE;
