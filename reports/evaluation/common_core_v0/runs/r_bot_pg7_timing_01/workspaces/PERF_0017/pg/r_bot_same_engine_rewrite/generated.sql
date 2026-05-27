SELECT "customer"."c_custkey", "customer"."c_name", SUM("t0"."l_extendedprice" * (1 - "t0"."l_discount")) AS "revenue", "customer"."c_acctbal", "nation"."n_name", "customer"."c_address", "customer"."c_phone", "customer"."c_comment"
FROM "customer"
    INNER JOIN (SELECT *
        FROM "orders"
        WHERE "o_orderdate" >= DATE '1993-11-01' AND "o_orderdate" < DATE '1994-02-01') AS "t" ON "customer"."c_custkey" = "t"."o_custkey"
    INNER JOIN (SELECT *
        FROM "lineitem"
        WHERE "l_returnflag" = 'R') AS "t0" ON "t"."o_orderkey" = "t0"."l_orderkey"
    INNER JOIN "nation" ON "customer"."c_nationkey" = "nation"."n_nationkey"
GROUP BY "customer"."c_custkey", "customer"."c_name", "customer"."c_acctbal", "customer"."c_phone", "nation"."n_name", "customer"."c_address", "customer"."c_comment"
ORDER BY 3 DESC
FETCH NEXT 20 ROWS ONLY;
