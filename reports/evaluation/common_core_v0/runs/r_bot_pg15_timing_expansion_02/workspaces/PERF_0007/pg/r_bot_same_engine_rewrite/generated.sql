SELECT SUM("l_extendedprice" * "l_discount") AS "revenue"
FROM "lineitem"
WHERE "l_shipdate" >= DATE '1995-01-01' AND "l_shipdate" < DATE '1996-01-01' AND ("l_discount" >= 0.08 AND "l_discount" <= 0.10) AND "l_quantity" < 25;
