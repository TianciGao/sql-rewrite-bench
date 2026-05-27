SELECT "customer_address"."ca_state" AS "state", COUNT(*) AS "cnt"
FROM "customer_address",
"customer",
"store_sales",
"date_dim",
"item"
WHERE "customer_address"."ca_address_sk" = "customer"."c_current_addr_sk" AND ("customer"."c_customer_sk" = "store_sales"."ss_customer_sk" AND "store_sales"."ss_sold_date_sk" = "date_dim"."d_date_sk") AND ("store_sales"."ss_item_sk" = "item"."i_item_sk" AND ("date_dim"."d_month_seq" = (SELECT "d_month_seq"
FROM "date_dim" AS "date_dim0"
WHERE "d_year" = 2000 AND "d_moy" = 2
GROUP BY "d_month_seq") AND "item"."i_current_price" > CAST(1.2 * (SELECT AVG("i_current_price")
FROM "item" AS "item0"
WHERE "i_category" = "item"."i_category") AS DECIMAL(19, 0))))
GROUP BY "customer_address"."ca_state"
HAVING COUNT(*) >= 10
ORDER BY 2, "customer_address"."ca_state"
FETCH NEXT 100 ROWS ONLY
