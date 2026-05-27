SELECT "$cor0"."t0a", "$cor0"."t0b"
FROM "t0" AS "$cor0",
    LATERAL (SELECT SUM("c") AS "EXPR$0"
        FROM (SELECT "t1c" AS "c"
                    FROM "t1"
                    WHERE "t1a" = "$cor0"."t0a"
                    UNION ALL
                    SELECT "t2c" AS "c"
                    FROM "t2"
                    WHERE "t2b" = "$cor0"."t0b") AS "t5") AS "t7"
WHERE "$cor0"."t0a" < "t7"."EXPR$0";
