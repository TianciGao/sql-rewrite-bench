SELECT "t0"."s_name", "t0"."s_address"
FROM (SELECT *
        FROM "supplier"
            INNER JOIN (SELECT *
                FROM "nation"
                WHERE "n_name" = 'BRAZIL') AS "t" ON "supplier"."s_nationkey" = "t"."n_nationkey"
        WHERE "supplier"."s_suppkey" IS NOT NULL) AS "t0"
    INNER JOIN (SELECT "t3"."ps_suppkey"
        FROM (SELECT *
                FROM "partsupp"
                    INNER JOIN (SELECT "p_partkey"
                        FROM "part"
                        WHERE "p_name" LIKE 'pale%') AS "t2" ON "partsupp"."ps_partkey" = "t2"."p_partkey"
                WHERE "partsupp"."ps_partkey" IS NOT NULL AND "partsupp"."ps_suppkey" IS NOT NULL) AS "t3"
            INNER JOIN (SELECT "l_partkey", "l_suppkey", SUM("l_quantity") AS "$f2"
                FROM "lineitem"
                WHERE "l_shipdate" >= DATE '1997-01-01' AND "l_shipdate" < (DATE '1997-01-01' + INTERVAL '1' YEAR) AND "l_partkey" IS NOT NULL AND "l_suppkey" IS NOT NULL
                GROUP BY "l_partkey", "l_suppkey") AS "t6" ON "t3"."ps_partkey" = "t6"."l_partkey" AND "t3"."ps_suppkey" = "t6"."l_suppkey" AND "t3"."ps_availqty" > 0.5 * "t6"."$f2"
        GROUP BY "t3"."ps_suppkey") AS "t8" ON "t0"."s_suppkey" = "t8"."ps_suppkey"
ORDER BY "t0"."s_name";
