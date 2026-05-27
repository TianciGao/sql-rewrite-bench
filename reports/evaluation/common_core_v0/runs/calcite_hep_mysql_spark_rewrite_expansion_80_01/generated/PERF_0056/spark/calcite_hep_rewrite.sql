SELECT `customer_address`.`ca_state` `state`, COUNT(*) `cnt`
FROM `customer_address`
CROSS JOIN `customer`
CROSS JOIN `store_sales`
CROSS JOIN `date_dim`
CROSS JOIN `item`
WHERE `customer_address`.`ca_address_sk` = `customer`.`c_current_addr_sk` AND (`customer`.`c_customer_sk` = `store_sales`.`ss_customer_sk` AND `store_sales`.`ss_sold_date_sk` = `date_dim`.`d_date_sk`) AND (`store_sales`.`ss_item_sk` = `item`.`i_item_sk` AND (`date_dim`.`d_month_seq` = (SELECT `d_month_seq`
FROM `date_dim` `date_dim0`
WHERE `d_year` = 2000 AND `d_moy` = 2
GROUP BY `d_month_seq`) AND CAST(`item`.`i_current_price` AS DECIMAL(11, 1)) > 1.2 * (SELECT AVG(`i_current_price`)
FROM `item` `item0`
WHERE `i_category` = `item`.`i_category`)))
GROUP BY `customer_address`.`ca_state`
HAVING COUNT(*) >= 10
ORDER BY 2 NULLS LAST, `customer_address`.`ca_state` NULLS LAST
LIMIT 100
