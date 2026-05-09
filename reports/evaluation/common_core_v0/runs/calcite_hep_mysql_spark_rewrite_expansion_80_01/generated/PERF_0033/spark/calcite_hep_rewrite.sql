SELECT `item`.`i_brand_id` `brand_id`, `item`.`i_brand` `brand`, CASE WHEN COUNT(`store_sales`.`ss_ext_sales_price`) = 0 THEN NULL ELSE COALESCE(SUM(`store_sales`.`ss_ext_sales_price`), 0) END `ext_price`
FROM `date_dim`
CROSS JOIN `store_sales`
CROSS JOIN `item`
WHERE `date_dim`.`d_date_sk` = `store_sales`.`ss_sold_date_sk` AND `store_sales`.`ss_item_sk` = `item`.`i_item_sk` AND `item`.`i_manager_id` = 36 AND `date_dim`.`d_moy` = 12 AND `date_dim`.`d_year` = 2001
GROUP BY `item`.`i_brand`, `item`.`i_brand_id`
ORDER BY 3 DESC NULLS FIRST, `item`.`i_brand_id` NULLS LAST
LIMIT 100
