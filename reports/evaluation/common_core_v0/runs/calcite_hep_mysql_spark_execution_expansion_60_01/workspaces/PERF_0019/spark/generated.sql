SELECT `t1`.`c_count`, COUNT(*) `custdist`
FROM (SELECT COUNT(`orders`.`o_orderkey`) `c_count`
FROM `customer`
LEFT JOIN `orders` ON `customer`.`c_custkey` = `orders`.`o_custkey` AND `orders`.`o_comment` NOT LIKE '%express%deposits%'
GROUP BY `customer`.`c_custkey`) `t1`
GROUP BY `t1`.`c_count`
ORDER BY 2 DESC NULLS FIRST, `t1`.`c_count` DESC NULLS FIRST
