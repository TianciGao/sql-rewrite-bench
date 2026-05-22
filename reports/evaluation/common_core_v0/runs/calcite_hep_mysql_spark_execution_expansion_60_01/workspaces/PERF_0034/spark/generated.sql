SELECT `i_item_id`, CASE WHEN COUNT(`total_sales`) = 0 THEN NULL ELSE COALESCE(SUM(`total_sales`), 0) END `total_sales`
FROM (SELECT *
FROM (SELECT `item`.`i_item_id`, CASE WHEN COUNT(`store_sales`.`ss_ext_sales_price`) = 0 THEN NULL ELSE COALESCE(SUM(`store_sales`.`ss_ext_sales_price`), 0) END `total_sales`
FROM `store_sales`
CROSS JOIN `date_dim`
CROSS JOIN `customer_address`
CROSS JOIN `item`
WHERE `item`.`i_item_id` IN (SELECT `i_item_id`
FROM `item`
WHERE `i_color` = 'orchid' OR `i_color` = 'chiffon' OR `i_color` = 'lace') AND (`store_sales`.`ss_item_sk` = `item`.`i_item_sk` AND `store_sales`.`ss_sold_date_sk` = `date_dim`.`d_date_sk`) AND (`date_dim`.`d_year` = 2000 AND `date_dim`.`d_moy` = 1 AND (`store_sales`.`ss_addr_sk` = `customer_address`.`ca_address_sk` AND `customer_address`.`ca_gmt_offset` = -8))
GROUP BY `item`.`i_item_id`
UNION ALL
SELECT `item1`.`i_item_id`, CASE WHEN COUNT(`catalog_sales`.`cs_ext_sales_price`) = 0 THEN NULL ELSE COALESCE(SUM(`catalog_sales`.`cs_ext_sales_price`), 0) END `total_sales`
FROM `catalog_sales`
CROSS JOIN `date_dim` `date_dim0`
CROSS JOIN `customer_address` `customer_address0`
CROSS JOIN `item` `item1`
WHERE `item1`.`i_item_id` IN (SELECT `i_item_id`
FROM `item`
WHERE `i_color` = 'orchid' OR `i_color` = 'chiffon' OR `i_color` = 'lace') AND (`catalog_sales`.`cs_item_sk` = `item1`.`i_item_sk` AND `catalog_sales`.`cs_sold_date_sk` = `date_dim0`.`d_date_sk`) AND (`date_dim0`.`d_year` = 2000 AND `date_dim0`.`d_moy` = 1 AND (`catalog_sales`.`cs_bill_addr_sk` = `customer_address0`.`ca_address_sk` AND `customer_address0`.`ca_gmt_offset` = -8))
GROUP BY `item1`.`i_item_id`)
UNION ALL
SELECT `item3`.`i_item_id`, CASE WHEN COUNT(`web_sales`.`ws_ext_sales_price`) = 0 THEN NULL ELSE COALESCE(SUM(`web_sales`.`ws_ext_sales_price`), 0) END `total_sales`
FROM `web_sales`
CROSS JOIN `date_dim` `date_dim1`
CROSS JOIN `customer_address` `customer_address1`
CROSS JOIN `item` `item3`
WHERE `item3`.`i_item_id` IN (SELECT `i_item_id`
FROM `item`
WHERE `i_color` = 'orchid' OR `i_color` = 'chiffon' OR `i_color` = 'lace') AND (`web_sales`.`ws_item_sk` = `item3`.`i_item_sk` AND `web_sales`.`ws_sold_date_sk` = `date_dim1`.`d_date_sk`) AND (`date_dim1`.`d_year` = 2000 AND `date_dim1`.`d_moy` = 1 AND (`web_sales`.`ws_bill_addr_sk` = `customer_address1`.`ca_address_sk` AND `customer_address1`.`ca_gmt_offset` = -8))
GROUP BY `item3`.`i_item_id`) `t21`
GROUP BY `i_item_id`
ORDER BY 2 NULLS LAST, `i_item_id` NULLS LAST
LIMIT 100
