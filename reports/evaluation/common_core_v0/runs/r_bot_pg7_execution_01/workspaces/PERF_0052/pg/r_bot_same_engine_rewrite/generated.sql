SELECT "customer"."c_customer_id"
FROM (SELECT "store_returns"."sr_customer_sk", "store_returns"."sr_store_sk", SUM("store_returns"."sr_fee") AS "ctr_total_return"
        FROM "store_returns"
            INNER JOIN (SELECT *
                FROM "date_dim"
                WHERE "d_year" = 2000) AS "t" ON "store_returns"."sr_returned_date_sk" = "t"."d_date_sk"
        GROUP BY "store_returns"."sr_customer_sk", "store_returns"."sr_store_sk") AS "t1"
    INNER JOIN (SELECT *
        FROM "store"
        WHERE "s_state" = 'TN') AS "t2" ON "t1"."sr_store_sk" = "t2"."s_store_sk"
    INNER JOIN "customer" ON "t1"."sr_customer_sk" = "customer"."c_customer_sk"
    INNER JOIN (SELECT "t7"."sr_store_sk0", AVG("t7"."ctr_total_return") AS "$f1"
        FROM (SELECT "store_returns0"."sr_store_sk0", SUM("store_returns0"."sr_fee0") AS "ctr_total_return"
                FROM "store_returns" AS "store_returns0" ("sr_customer_sk0", "sr_store_sk0", "sr_returned_date_sk0", "sr_fee0")
                    INNER JOIN (SELECT *
                        FROM "date_dim" AS "date_dim0" ("d_date_sk0", "d_year0")
                        WHERE "d_year0" = 2000) AS "t3" ON "store_returns0"."sr_returned_date_sk0" = "t3"."d_date_sk0"
                GROUP BY "store_returns0"."sr_customer_sk0", "store_returns0"."sr_store_sk0"
                HAVING "store_returns0"."sr_store_sk0" IS NOT NULL) AS "t7"
        GROUP BY "t7"."sr_store_sk0") AS "t8" ON "t1"."sr_store_sk" = "t8"."sr_store_sk0" AND "t1"."ctr_total_return" > "t8"."$f1" * 1.2
ORDER BY "customer"."c_customer_id"
FETCH NEXT 100 ROWS ONLY;
