SELECT "t6"."s_name", "t6"."s_address"
FROM (SELECT "supplier"."s_suppkey", "supplier"."s_name", "supplier"."s_address", "supplier"."s_nationkey"
        FROM "supplier"
            INNER JOIN (SELECT "partsupp"."ps_suppkey"
                FROM "partsupp"
                    INNER JOIN (SELECT "p_partkey"
                        FROM "part"
                        WHERE "p_name" LIKE 'pale%') AS "t0" ON "partsupp"."ps_partkey" = "t0"."p_partkey"
                    INNER JOIN (SELECT "l_partkey", "l_suppkey", SUM("l_quantity") AS "$f2"
                        FROM "lineitem"
                        WHERE "l_shipdate" >= DATE '1997-01-01' AND "l_shipdate" < (DATE '1997-01-01' + INTERVAL '1' YEAR) AND "l_partkey" IS NOT NULL AND "l_suppkey" IS NOT NULL
                        GROUP BY "l_partkey", "l_suppkey") AS "t3" ON "partsupp"."ps_partkey" = "t3"."l_partkey" AND "partsupp"."ps_suppkey" = "t3"."l_suppkey" AND "partsupp"."ps_availqty" > 0.5 * "t3"."$f2"
                GROUP BY "partsupp"."ps_suppkey") AS "t5" ON "supplier"."s_suppkey" = "t5"."ps_suppkey") AS "t6"
    INNER JOIN (SELECT *
        FROM "nation"
        WHERE "n_name" = 'BRAZIL') AS "t7" ON "t6"."s_nationkey" = "t7"."n_nationkey"
ORDER BY "t6"."s_name";
