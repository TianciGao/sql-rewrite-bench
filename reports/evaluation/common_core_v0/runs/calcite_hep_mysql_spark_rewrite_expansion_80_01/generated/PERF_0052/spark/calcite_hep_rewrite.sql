SELECT `customer`.`c_customer_id`
FROM (SELECT `store_returns`.`sr_customer_sk` `ctr_customer_sk`, `store_returns`.`sr_store_sk` `ctr_store_sk`, CASE WHEN COUNT(`store_returns`.`sr_fee`) = 0 THEN NULL ELSE COALESCE(SUM(`store_returns`.`sr_fee`), 0) END `ctr_total_return`
FROM `store_returns`
CROSS JOIN `date_dim`
WHERE `store_returns`.`sr_returned_date_sk` = `date_dim`.`d_date_sk` AND `date_dim`.`d_year` = 2000
GROUP BY `store_returns`.`sr_customer_sk`, `store_returns`.`sr_store_sk`) `t2`
CROSS JOIN `store`
CROSS JOIN `customer`
WHERE `t2`.`ctr_total_return` > CAST((SELECT AVG(`t7`.`ctr_total_return`) * 1.2
FROM (SELECT SUM(`store_returns0`.`sr_fee`) `ctr_total_return`
FROM `store_returns` `store_returns0`
CROSS JOIN `date_dim` `date_dim0`
WHERE `store_returns0`.`sr_returned_date_sk` = `date_dim0`.`d_date_sk` AND `date_dim0`.`d_year` = 2000
GROUP BY `store_returns0`.`sr_customer_sk`, `store_returns0`.`sr_store_sk`
HAVING `t2`.`ctr_store_sk` = `store_returns0`.`sr_store_sk`) `t7`) AS DECIMAL(19, 0)) AND `store`.`s_store_sk` = `t2`.`ctr_store_sk` AND `store`.`s_state` = 'TN' AND `t2`.`ctr_customer_sk` = `customer`.`c_customer_sk`
ORDER BY `customer`.`c_customer_id` NULLS LAST
LIMIT 100
