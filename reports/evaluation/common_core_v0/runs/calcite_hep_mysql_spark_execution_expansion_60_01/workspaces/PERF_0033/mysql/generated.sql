SELECT `item`.`i_brand_id` AS `brand_id`, `item`.`i_brand` AS `brand`, CASE WHEN COUNT(`store_sales`.`ss_ext_sales_price`) = 0 THEN NULL ELSE COALESCE(SUM(`store_sales`.`ss_ext_sales_price`), 0) END AS `ext_price`
FROM `date_dim`,
`store_sales`,
`item`
WHERE `date_dim`.`d_date_sk` = `store_sales`.`ss_sold_date_sk` AND `store_sales`.`ss_item_sk` = `item`.`i_item_sk` AND `item`.`i_manager_id` = 36 AND `date_dim`.`d_moy` = 12 AND `date_dim`.`d_year` = 2001
GROUP BY `item`.`i_brand`, `item`.`i_brand_id`
ORDER BY CASE WHEN COUNT(`store_sales`.`ss_ext_sales_price`) = 0 THEN NULL ELSE COALESCE(SUM(`store_sales`.`ss_ext_sales_price`), 0) END IS NULL DESC, 3 DESC, `item`.`i_brand_id` IS NULL, `item`.`i_brand_id`
LIMIT 100
