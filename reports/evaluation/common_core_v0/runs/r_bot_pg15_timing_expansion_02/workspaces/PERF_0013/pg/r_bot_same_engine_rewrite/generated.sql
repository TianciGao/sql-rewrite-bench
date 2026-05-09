SELECT "nation"."n_name", SUM("t1"."l_extendedprice" * (1 - "t1"."l_discount")) AS "revenue"
FROM "customer"
    INNER JOIN (SELECT *
        FROM (SELECT *
                FROM "orders"
                WHERE "o_orderdate" >= DATE '1997-01-01' AND "o_orderdate" < DATE '1998-01-01') AS "t"
        WHERE "o_custkey" IS NOT NULL) AS "t0" ON "customer"."c_custkey" = "t0"."o_custkey"
    INNER JOIN (SELECT *
        FROM "lineitem"
        WHERE "l_orderkey" IS NOT NULL) AS "t1" ON "t0"."o_orderkey" = "t1"."l_orderkey"
    INNER JOIN (SELECT *
        FROM "supplier"
        WHERE "s_nationkey" IS NOT NULL) AS "t2" ON "customer"."c_nationkey" = "t2"."s_nationkey" AND "t1"."l_suppkey" = "t2"."s_suppkey"
    INNER JOIN "nation" ON "t2"."s_nationkey" = "nation"."n_nationkey"
    INNER JOIN (SELECT *
        FROM "region"
        WHERE "r_name" = 'MIDDLE EAST') AS "t3" ON "nation"."n_regionkey" = "t3"."r_regionkey"
GROUP BY "nation"."n_name"
ORDER BY 2 DESC;
