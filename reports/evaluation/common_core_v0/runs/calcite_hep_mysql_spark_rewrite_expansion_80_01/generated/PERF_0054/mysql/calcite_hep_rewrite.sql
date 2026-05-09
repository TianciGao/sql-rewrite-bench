SELECT `date_dim`.`d_year`, `item`.`i_brand_id` AS `brand_id`, `item`.`i_brand` AS `brand`, CASE WHEN COUNT(`store_sales`.`ss_ext_sales_price`) = 0 THEN NULL ELSE COALESCE(SUM(`store_sales`.`ss_ext_sales_price`), 0) END AS `sum_agg`
FROM `date_dim`,
`store_sales`,
`item`
WHERE `date_dim`.`d_date_sk` = `store_sales`.`ss_sold_date_sk` AND `store_sales`.`ss_item_sk` = `item`.`i_item_sk` AND `item`.`i_manufact_id` = 436 AND `date_dim`.`d_moy` = 12
GROUP BY `date_dim`.`d_year`, `item`.`i_brand`, `item`.`i_brand_id`
ORDER BY `date_dim`.`d_year` IS NULL, `date_dim`.`d_year`, CASE WHEN COUNT(`store_sales`.`ss_ext_sales_price`) = 0 THEN NULL ELSE COALESCE(SUM(`store_sales`.`ss_ext_sales_price`), 0) END IS NULL DESC, 4 DESC, `item`.`i_brand_id` IS NULL, `item`.`i_brand_id`
LIMIT 100
