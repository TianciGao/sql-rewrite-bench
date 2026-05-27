SELECT `t1`.`c_count`, COUNT(*) AS `custdist`
FROM (SELECT COUNT(`orders`.`o_orderkey`) AS `c_count`
FROM `customer`
LEFT JOIN `orders` ON `customer`.`c_custkey` = `orders`.`o_custkey` AND `orders`.`o_comment` NOT LIKE '%express%deposits%'
GROUP BY `customer`.`c_custkey`) AS `t1`
GROUP BY `t1`.`c_count`
ORDER BY COUNT(*) IS NULL DESC, 2 DESC, `t1`.`c_count` IS NULL DESC, `t1`.`c_count` DESC
